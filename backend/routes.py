"""
Flask Routes for EduSolve AI - Enhanced
Defines all API endpoints with improved features and response formatting
"""

import os
import json
import sys
from datetime import datetime
from flask import Blueprint, request, jsonify
from config import Config

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from ml_model import classify_question, subject_classifier, difficulty_classifier
from groq_client import get_ai_explanation
from preprocess import preprocess_input

# Create Blueprint for routes
api = Blueprint('api', __name__)

# Data storage paths - use config paths
DATA_DIR = os.path.dirname(Config.TRAINING_DATA_PATH)
TRAINING_DATA_FILE = Config.TRAINING_DATA_PATH
FEEDBACK_FILE = os.path.join(DATA_DIR, 'feedback.json')

def load_json_file(filepath, default=[]):
    """Load data from JSON file with error handling"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {str(e)}")
    return default

def save_json_file(filepath, data):
    """Save data to JSON file with error handling"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to {filepath}: {str(e)}")
        return False

def load_training_data():
    """Load existing training data from JSON file"""
    return load_json_file(TRAINING_DATA_FILE, [])

def save_training_data(data):
    """Save training data to JSON file"""
    save_json_file(TRAINING_DATA_FILE, data)

def load_feedback():
    """Load feedback data from JSON file"""
    return load_json_file(FEEDBACK_FILE, [])

def save_feedback(data):
    """Save feedback data to JSON file"""
    save_json_file(FEEDBACK_FILE, data)

# =====================================================
# Health & Status Endpoints
# =====================================================

@api.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    training_data = load_training_data()
    return jsonify({
        'status': 'success',
        'message': 'EduSolve AI Backend is operational',
        'timestamp': datetime.now().isoformat(),
        'database_records': len(training_data),
        'version': '2.0'
    }), 200

# =====================================================
# Main Question Answering Endpoints
# =====================================================

@api.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Main endpoint to submit a question and get explanation
    Enhanced with better error handling and response formatting
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: question',
                'code': 'MISSING_QUESTION'
            }), 400
        
        question = data['question'].strip()
        
        if len(question) < 3:
            return jsonify({
                'status': 'error',
                'message': 'Question must be at least 3 characters long',
                'code': 'QUESTION_TOO_SHORT'
            }), 400
        
        if len(question) > 5000:
            return jsonify({
                'status': 'error',
                'message': 'Question must be less than 5000 characters',
                'code': 'QUESTION_TOO_LONG'
            }), 400
        
        # Preprocess the question
        try:
            processed_text, tokens = preprocess_input(question)
        except Exception as e:
            print(f"Preprocessing error: {str(e)}")
            processed_text = question
            tokens = question.split()
        
        # Classify by subject and difficulty
        classification = classify_question(question)
        subject = classification.get('subject', 'Unknown')
        difficulty = classification.get('difficulty', 'Unknown')
        subject_confidence = classification.get('subject_confidence', 0.0)
        difficulty_confidence = classification.get('difficulty_confidence', 0.0)
        
        # Get explanation from Groq API
        groq_response = get_ai_explanation(question, subject, difficulty)
        
        if groq_response.get('status') != 'success':
            return jsonify({
                'status': 'error',
                'message': 'Failed to generate explanation',
                'code': 'API_ERROR',
                'details': groq_response.get('error_message', 'Unknown error')
            }), 500
        
        explanation = groq_response.get('explanation', '')
        
        # Store interaction data
        interaction_data = {
            'id': datetime.now().isoformat(),
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'processed_text': processed_text,
            'tokens': tokens if tokens else [],
            'subject': subject,
            'subject_confidence': float(subject_confidence),
            'difficulty': difficulty,
            'difficulty_confidence': float(difficulty_confidence),
            'explanation': explanation,
            'model_used': groq_response.get('model_used'),
            'tokens_used': groq_response.get('tokens_used', 0)
        }
        
        # Save to database
        training_data = load_training_data()
        training_data.append(interaction_data)
        save_training_data(training_data)
        
        # Return formatted response
        return jsonify({
            'status': 'success',
            'code': 'QUESTION_PROCESSED',
            'data': {
                'id': interaction_data['id'],
                'question': question,
                'subject': subject,
                'subject_confidence': float(subject_confidence),
                'difficulty': difficulty,
                'difficulty_confidence': float(difficulty_confidence),
                'explanation': explanation,
                'timestamp': interaction_data['timestamp']
            },
            'message': 'Question processed successfully'
        }), 200
    
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e) if os.getenv('FLASK_ENV') == 'development' else None
        }), 500

# =====================================================
# Information Endpoints
# =====================================================

@api.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get list of available subjects"""
    return jsonify({
        'status': 'success',
        'data': {
            'subjects': subject_classifier.subjects,
            'count': len(subject_classifier.subjects)
        }
    }), 200

@api.route('/api/difficulties', methods=['GET'])
def get_difficulties():
    """Get list of available difficulty levels"""
    return jsonify({
        'status': 'success',
        'data': {
            'difficulties': difficulty_classifier.difficulties,
            'count': len(difficulty_classifier.difficulties)
        }
    }), 200

# =====================================================
# Data History & Analytics Endpoints
# =====================================================

@api.route('/api/history', methods=['GET'])
def get_history():
    """Get all stored questions and explanations with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        subject_filter = request.args.get('subject', None)
        difficulty_filter = request.args.get('difficulty', None)
        
        training_data = load_training_data()
        
        # Apply filters
        if subject_filter:
            training_data = [d for d in training_data if d.get('subject') == subject_filter]
        
        if difficulty_filter:
            training_data = [d for d in training_data if d.get('difficulty') == difficulty_filter]
        
        # Paginate
        total = len(training_data)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = training_data[start:end]
        
        return jsonify({
            'status': 'success',
            'data': paginated_data,
            'pagination': {
                'total_records': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve history',
            'code': 'HISTORY_ERROR',
            'details': str(e)
        }), 500

@api.route('/api/stats', methods=['GET'])
def get_stats():
    """Get comprehensive statistics about stored data"""
    try:
        training_data = load_training_data()
        
        subjects = {}
        difficulties = {}
        total_words = 0
        
        for record in training_data:
            subject = record.get('subject', 'Unknown')
            difficulty = record.get('difficulty', 'Unknown')
            question = record.get('question', '')
            
            subjects[subject] = subjects.get(subject, 0) + 1
            difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
            total_words += len(question.split())
        
        avg_words = total_words / len(training_data) if training_data else 0
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_questions': len(training_data),
                'subjects': subjects,
                'difficulties': difficulties,
                'statistics': {
                    'total_words': total_words,
                    'average_question_length': round(avg_words, 2),
                    'timestamp': datetime.now().isoformat()
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve statistics',
            'code': 'STATS_ERROR'
        }), 500

# =====================================================
# Search & Filter Endpoints
# =====================================================

@api.route('/api/search', methods=['GET'])
def search_questions():
    """Search questions by keyword"""
    try:
        query = request.args.get('q', '', type=str).lower()
        
        if len(query) < 2:
            return jsonify({
                'status': 'error',
                'message': 'Search query must be at least 2 characters',
                'code': 'QUERY_TOO_SHORT'
            }), 400
        
        training_data = load_training_data()
        results = [
            d for d in training_data
            if query in d.get('question', '').lower()
        ]
        
        return jsonify({
            'status': 'success',
            'data': results[:50],  # Limit to 50 results
            'total_found': len(results)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Search failed',
            'code': 'SEARCH_ERROR'
        }), 500

# =====================================================
# Batch Processing Endpoint
# =====================================================

@api.route('/api/batch-ask', methods=['POST'])
def batch_ask_questions():
    """Process multiple questions at once"""
    try:
        data = request.get_json()
        
        if not data or 'questions' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: questions',
                'code': 'MISSING_QUESTIONS'
            }), 400
        
        questions = data.get('questions', [])
        
        if not isinstance(questions, list) or len(questions) == 0:
            return jsonify({
                'status': 'error',
                'message': 'Questions must be a non-empty list',
                'code': 'INVALID_FORMAT'
            }), 400
        
        if len(questions) > 100:
            return jsonify({
                'status': 'error',
                'message': 'Maximum 100 questions allowed per batch',
                'code': 'BATCH_TOO_LARGE'
            }), 400
        
        results = []
        for question in questions:
            try:
                q = question.strip() if isinstance(question, str) else str(question)
                if len(q) < 3:
                    results.append({'error': 'Question too short'})
                    continue
                
                classification = classify_question(q)
                result = {
                    'question': q,
                    'subject': classification.get('subject'),
                    'difficulty': classification.get('difficulty'),
                    'subject_confidence': classification.get('subject_confidence'),
                    'difficulty_confidence': classification.get('difficulty_confidence')
                }
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
        
        return jsonify({
            'status': 'success',
            'data': results,
            'processed': len(results),
            'code': 'BATCH_PROCESSED'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Batch processing failed',
            'code': 'BATCH_ERROR'
        }), 500

# =====================================================
# Feedback Endpoint
# =====================================================

@api.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for questions and explanations"""
    try:
        data = request.get_json()
        
        if not data or 'question_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: question_id',
                'code': 'MISSING_FEEDBACK_ID'
            }), 400
        
        feedback_record = {
            'id': datetime.now().isoformat(),
            'question_id': data.get('question_id'),
            'rating': data.get('rating', 0),  # 1-5
            'comment': data.get('comment', ''),
            'helpful': data.get('helpful', False),
            'timestamp': datetime.now().isoformat()
        }
        
        feedback_list = load_feedback()
        feedback_list.append(feedback_record)
        save_feedback(feedback_list)
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback submitted successfully',
            'code': 'FEEDBACK_SAVED',
            'data': feedback_record
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to submit feedback',
            'code': 'FEEDBACK_ERROR'
        }), 500

# =====================================================
# Data Export Endpoint
# =====================================================

@api.route('/api/export', methods=['GET'])
def export_data():
    """Export all data as CSV"""
    try:
        format_type = request.args.get('format', 'csv', type=str)
        
        training_data = load_training_data()
        
        if format_type == 'json':
            output = io.StringIO()
            json.dump(training_data, output)
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='application/json',
                as_attachment=True,
                download_name=f'edusolver_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
        
        elif format_type == 'csv':
            output = io.StringIO()
            if training_data:
                fieldnames = training_data[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(training_data)
            
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'edusolver_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unsupported format. Use csv or json',
                'code': 'UNSUPPORTED_FORMAT'
            }), 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Export failed',
            'code': 'EXPORT_ERROR'
        }), 500

# =====================================================
# Data Management Endpoints
# =====================================================

@api.route('/api/clear-data', methods=['POST'])
def clear_data():
    """Clear all stored training data (requires confirmation)"""
    try:
        data = request.get_json() or {}
        confirm = data.get('confirm', False)
        
        if not confirm:
            return jsonify({
                'status': 'error',
                'message': 'Please set confirm to true to delete all data',
                'code': 'CONFIRMATION_REQUIRED'
            }), 400
        
        save_training_data([])
        
        return jsonify({
            'status': 'success',
            'message': 'All training data cleared',
            'code': 'DATA_CLEARED'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to clear data',
            'code': 'CLEAR_ERROR'
        }), 500

@api.route('/api/delete-record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a specific record by ID"""
    try:
        training_data = load_training_data()
        original_length = len(training_data)
        
        training_data = [d for d in training_data if d.get('id') != record_id]
        
        if len(training_data) == original_length:
            return jsonify({
                'status': 'error',
                'message': 'Record not found',
                'code': 'RECORD_NOT_FOUND'
            }), 404
        
        save_training_data(training_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Record deleted successfully',
            'code': 'RECORD_DELETED'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete record',
            'code': 'DELETE_ERROR'
        }), 500

# =====================================================
# Error Handlers
# =====================================================

@api.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'code': 'ENDPOINT_NOT_FOUND'
    }), 404

@api.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors"""
    return jsonify({
        'status': 'error',
        'message': 'Method not allowed',
        'code': 'METHOD_NOT_ALLOWED'
    }), 405

@api.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'code': 'INTERNAL_ERROR'
    }), 500



