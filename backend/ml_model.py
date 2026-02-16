"""
Machine Learning Models for EduSolve AI
Handles subject classification and difficulty prediction
Improved with ensemble methods and better feature extraction
"""

import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier
from preprocess import preprocess_input

class MLModel:
    """
    Improved ML Model for subject and difficulty classification
    Uses ensemble methods and advanced feature extraction
    """
    
    def __init__(self, model_type='subject'):
        """
        Initialize ML model
        
        Args:
            model_type (str): Type of model - 'subject' or 'difficulty'
        """
        self.model_type = model_type
        self.model = None
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
        # Enhanced feature extraction
        self.vectorizer = TfidfVectorizer(
            max_features=200,
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95,
            lowercase=True,
            stop_words='english'
        )
        
        # Define possible classes
        self.subjects = [
            'Mathematics', 'Physics', 'Chemistry', 'Biology',
            'English', 'History', 'Geography'
        ]
        self.difficulties = ['Easy', 'Medium', 'Hard']
        
        # Model file paths - use absolute paths
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        models_dir = os.path.join(project_root, 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        self.model_path = os.path.join(models_dir, f'{model_type}_model.pkl')
        self.vectorizer_path = os.path.join(models_dir, f'{model_type}_vectorizer.pkl')
        self.encoder_path = os.path.join(models_dir, f'{model_type}_encoder.pkl')
    
    def train(self, texts, labels):
        """
        Train the ML model on provided data
        
        Args:
            texts (list): List of text samples
            labels (list): Corresponding labels
        """
        print(f"🤖 Training {self.model_type} model with {len(texts)} samples...")
        
        if len(texts) < 5:
            print(f"⚠️ Warning: Only {len(texts)} samples for training. Minimum recommended: 10")
        
        try:
            # Fit label encoder
            unique_labels = list(set(labels))
            self.label_encoder.fit(unique_labels)
            
            # Create ensemble pipeline
            if self.model_type == 'subject':
                # Use multiple classifiers for subjects
                self.model = Pipeline([
                    ('tfidf', TfidfVectorizer(
                        max_features=200,
                        ngram_range=(1, 3),
                        min_df=1,
                        max_df=0.95,
                        lowercase=True,
                        stop_words='english'
                    )),
                    ('clf', GradientBoostingClassifier(
                        n_estimators=100,
                        learning_rate=0.1,
                        max_depth=7,
                        subsample=0.8,
                        random_state=42
                    ))
                ])
            else:  # difficulty
                self.model = Pipeline([
                    ('tfidf', TfidfVectorizer(
                        max_features=150,
                        ngram_range=(1, 2),
                        min_df=1,
                        max_df=0.95,
                        lowercase=True
                    )),
                    ('clf', RandomForestClassifier(
                        n_estimators=100,
                        max_depth=10,
                        min_samples_split=5,
                        min_samples_leaf=2,
                        random_state=42,
                        n_jobs=-1
                    ))
                ])
            
            # Train the model
            self.model.fit(texts, labels)
            self.is_trained = True
            
            print(f"✅ {self.model_type.capitalize()} model trained successfully!")
            print(f"   Classes: {', '.join(unique_labels)}")
            print(f"   Training samples: {len(texts)}")
            
            # Save model
            self.save_model()
            
        except Exception as e:
            print(f"❌ Error training model: {str(e)}")
            self._train_default_model()
    
    def predict(self, text):
        """
        Predict class for given text
        
        Args:
            text (str): Input text to classify
            
        Returns:
            tuple: (predicted_label, confidence_score)
        """
        try:
            if self.model is None:
                self.load_model()
            
            # Preprocess input
            processed_text, _ = preprocess_input(text)
            
            if not processed_text or len(processed_text.strip()) < 2:
                # Fallback for very short text
                return self._get_default_prediction()
            
            # Make prediction
            prediction = self.model.predict([processed_text])[0]
            
            # Get confidence scores
            probabilities = self.model.predict_proba([processed_text])[0]
            confidence = max(probabilities) if probabilities is not None else 0.5
            
            # Ensure confidence is between 0 and 1
            confidence = min(max(float(confidence), 0.0), 1.0)
            
            return prediction, confidence
            
        except Exception as e:
            print(f"⚠️ Prediction error: {str(e)}")
            return self._get_default_prediction()
    
    def _get_default_prediction(self):
        """Return default prediction when model fails"""
        if self.model_type == 'subject':
            return 'Mathematics', 0.5
        else:
            return 'Medium', 0.5
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(self.encoder_path, 'wb') as f:
                pickle.dump(self.label_encoder, f)
            
            print(f"💾 {self.model_type.capitalize()} model saved successfully")
        
        except Exception as e:
            print(f"❌ Error saving model: {str(e)}")
    
    def load_model(self):
        """Load pre-trained model from disk"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                with open(self.encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                
                self.is_trained = True
                print(f"✅ {self.model_type.capitalize()} model loaded successfully!")
                return True
            else:
                print(f"⚠️ Model files not found at {self.model_path}")
                self._train_default_model()
                return False
        
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            self._train_default_model()
            return False
    
    def _train_default_model(self):
        """Train a default model with sample data"""
        print(f"🔧 Training default {self.model_type} model with sample data...")
        
        if self.model_type == 'subject':
            sample_texts = [
                "calculate derivative integrate solve equation",
                "velocity acceleration force motion physics",
                "atomic molecular chemical reaction element",
                "photosynthesis cell mitosis biology organism",
                "literature poem novel story character",
                "historical event ancient civilization empire",
                "geographic location map coordinates climate"
            ]
            sample_labels = [
                'Mathematics', 'Physics', 'Chemistry',
                'Biology', 'English', 'History', 'Geography'
            ]
        else:  # difficulty
            sample_texts = [
                "basic simple addition number",
                "derive solve quadratic equation calculus",
                "prove theorem eigenvalues differential equation"
            ]
            sample_labels = ['Easy', 'Medium', 'Hard']
        
        try:
            self.train(sample_texts, sample_labels)
        except Exception as e:
            print(f"❌ Error training default model: {str(e)}")
            # Use DummyClassifier as fallback - don't recurse
            self.model = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=100,
                    ngram_range=(1, 2),
                    min_df=1,
                    max_df=1.0
                )),
                ('clf', DummyClassifier(strategy='prior'))
            ])
            self.model.fit(sample_texts, sample_labels)
            self.is_trained = True
            print(f"✅ Default {self.model_type} model ({sample_labels}) ready as fallback")

class SubjectClassifier(MLModel):
    """Subject classification model"""
    def __init__(self):
        super().__init__(model_type='subject')

class DifficultyClassifier(MLModel):
    """Difficulty classification model"""
    def __init__(self):
        super().__init__(model_type='difficulty')

# Model instances
subject_classifier = SubjectClassifier()
difficulty_classifier = DifficultyClassifier()

def classify_question(question_text):
    """
    Classify a question by subject and difficulty with improved accuracy
    
    Args:
        question_text (str): The student's question
        
    Returns:
        dict: Classification results with subject, difficulty, and confidence scores
    """
    try:
        # Get raw predictions
        subject, subject_conf = subject_classifier.predict(question_text)
        difficulty, difficulty_conf = difficulty_classifier.predict(question_text)
        
        # Apply keyword-based fallback for low-confidence predictions
        if subject_conf < 0.40:  # Low confidence threshold
            subject, subject_conf = apply_keyword_fallback(question_text, subject, subject_conf)
        
        return {
            'subject': subject,
            'subject_confidence': float(subject_conf),
            'difficulty': difficulty,
            'difficulty_confidence': float(difficulty_conf)
        }
    except Exception as e:
        print(f"Classification error: {str(e)}")
        return {
            'status': 'error',
            'subject': 'General',
            'subject_confidence': 0.5,
            'difficulty': 'Medium',
            'difficulty_confidence': 0.5,
            'error': str(e)
        }

def apply_keyword_fallback(question_text, predicted_subject, predicted_conf):
    """
    Apply keyword-based rules for ambiguous questions
    
    Args:
        question_text: The question
        predicted_subject: Model's prediction
        predicted_conf: Prediction confidence
        
    Returns:
        tuple: (subject, confidence)
    """
    import re
    
    question_lower = question_text.lower()
    
    # Helper function for whole-word matching
    def count_keyword_matches(text, keywords):
        """Count whole-word matches only to avoid substring issues"""
        count = 0
        for keyword in keywords:
            # Use word boundary regex to match whole words only
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                count += 1
        return count
    
    # Programming/CS keywords
    cs_keywords = ['python', 'java', 'code', 'programming', 'algorithm', 'function',
                   'variable', 'loop', 'array', 'class', 'object', 'software',
                   'database', 'api', 'html', 'css', 'javascript', 'computer']
    
    # Math keywords
    math_keywords = ['calculus', 'derivative', 'integral', 'algebra', 'equation',
                     'solve', 'calculate', 'theorem', 'proof', 'matrix', 'vector',
                     'geometry', 'trigonometry', 'statistics', 'probability']
    
    # Science keywords
    bio_keywords = ['cell', 'dna', 'photosynthesis', 'evolution', 'organism',
                    'bacteria', 'virus', 'protein', 'gene', 'biology', 'species']
    
    chem_keywords = ['atom', 'molecule', 'chemical', 'reaction', 'element',
                     'compound', 'bond', 'acid', 'base', 'chemistry', 'periodic']
    
    phys_keywords = ['force', 'velocity', 'acceleration', 'energy', 'motion',
                     'gravity', 'wave', 'electricity', 'physics', 'momentum']
    
    # English/Literature keywords
    eng_keywords = ['shakespeare', 'poem', 'novel', 'literature', 'author',
                    'metaphor', 'grammar', 'writing', 'essay', 'story']
    
    # History keywords
    hist_keywords = ['war', 'ancient', 'empire', 'civilization', 'century',
                     'revolution', 'historical', 'history', 'president']
    
    # Geography keywords
    geo_keywords = ['capital', 'country', 'continent', 'ocean', 'mountain',
                    'river', 'climate', 'geography', 'map', 'location']
    
    # Check for keyword matches using whole-word matching
    keyword_map = {
        'Computer Science': cs_keywords,
        'Mathematics': math_keywords,
        'Biology': bio_keywords,
        'Chemistry': chem_keywords,
        'Physics': phys_keywords,
        'English': eng_keywords,
        'History': hist_keywords,
        'Geography': geo_keywords
    }
    
    # Count matches for each subject
    subject_scores = {}
    for subject, keywords in keyword_map.items():
        matches = count_keyword_matches(question_lower, keywords)
        if matches > 0:
            subject_scores[subject] = matches
    
    # Get best match
    if subject_scores:
        best_match = max(subject_scores, key=subject_scores.get)
        max_matches = subject_scores[best_match]
        
        # If we found keyword matches and original confidence was low
        if max_matches > 0 and predicted_conf < 0.40:
            new_conf = min(0.75, 0.50 + (max_matches * 0.15))
            print(f"🔧 Keyword fallback: {predicted_subject} → {best_match} ({new_conf:.2%})")
            return best_match, new_conf
    
    return predicted_subject, predicted_conf
