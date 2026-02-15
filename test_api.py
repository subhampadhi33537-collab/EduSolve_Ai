"""
Test Script for EduSolve AI
Tests all API endpoints and fixes
"""

import os
import sys
import json
import requests
from datetime import datetime

# Configuration
API_BASE_URL = 'http://localhost:5000/api'

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"🧪 {text}")
    print("="*70)

def test_health_check():
    """Test health check endpoint"""
    print_header("Testing Health Check")
    try:
        response = requests.get(f'{API_BASE_URL}/health', timeout=5)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_question_submission():
    """Test question submission endpoint"""
    print_header("Testing Question Submission")
    
    test_questions = [
        "What is the derivative of x squared?",
        "Explain photosynthesis",
        "Who was Shakespeare?"
    ]
    
    for question in test_questions:
        try:
            print(f"\n📝 Testing: {question[:50]}...")
            
            payload = {'question': question}
            response = requests.post(
                f'{API_BASE_URL}/ask',
                json=payload,
                timeout=30
            )
            
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ Status: {data.get('status')}")
                print(f"  ✓ Subject: {data.get('subject')}")
                print(f"  ✓ Difficulty: {data.get('difficulty')}")
                print(f"  ✓ Explanation Length: {len(data.get('explanation', ''))}")
                
                if data.get('status') != 'success':
                    print(f"  ✗ Error: {data.get('message')}")
                    return False
            else:
                print(f"  ✗ Error Status: {response.status_code}")
                print(f"  ✗ Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"  ✗ Exception: {str(e)}")
            return False
    
    return True

def test_statistics():
    """Test statistics endpoint"""
    print_header("Testing Statistics Endpoint")
    
    try:
        response = requests.get(f'{API_BASE_URL}/stats', timeout=5)
        print(f"✓ Status Code: {response.status_code}")
        
        data = response.json()
        print(f"✓ Total Questions: {data.get('total_questions')}")
        print(f"✓ Subjects: {list(data.get('subjects', {}).keys())}")
        print(f"✓ Difficulties: {list(data.get('difficulties', {}).keys())}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_history():
    """Test history endpoint"""
    print_header("Testing History Endpoint")
    
    try:
        response = requests.get(f'{API_BASE_URL}/history', timeout=5)
        print(f"✓ Status Code: {response.status_code}")
        
        data = response.json()
        print(f"✓ Total Records: {data.get('total_records')}")
        
        if data.get('data'):
            sample = data.get('data')[0]
            print(f"✓ Sample Record:")
            print(f"  - Question: {sample.get('question', 'N/A')[:50]}...")
            print(f"  - Subject: {sample.get('subject')}")
            print(f"  - Difficulty: {sample.get('difficulty')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_ml_models():
    """Test ML model functionality"""
    print_header("Testing ML Models")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        from backend.ml_model import classify_question
        
        test_text = "What is the derivative of x^2?"
        result = classify_question(test_text)
        
        print(f"✓ Classification Result:")
        print(f"  - Subject: {result['subject']}")
        print(f"  - Subject Confidence: {(result['subject_confidence']*100):.1f}%")
        print(f"  - Difficulty: {result['difficulty']}")
        print(f"  - Difficulty Confidence: {(result['difficulty_confidence']*100):.1f}%")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   🧪 EduSolve AI - Comprehensive Test Suite 🧪         ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    print("\n⏳ Waiting for server to be ready...")
    import time
    time.sleep(2)
    
    results = {
        'health_check': test_health_check(),
        'ml_models': test_ml_models(),
        'statistics': test_statistics(),
        'history': test_history(),
        'question_submission': test_question_submission(),
    }
    
    # Print Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All tests passed! Application is ready to use.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    main()
