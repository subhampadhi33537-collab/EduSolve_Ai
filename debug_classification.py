"""
Debug script to test ML model classification directly
"""

import sys
import os
import importlib

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import and use the module
import ml_model
importlib.reload(ml_model)  # Force reload to get latest changes

from ml_model import subject_classifier, difficulty_classifier, classify_question

def test_classification(questions):
    """Test classification on a list of questions"""
    
    print("\n" + "="*70)
    print("🔍 ML Model Classification Debug")
    print("="*70 + "\n")
    
    print(f"Subject Model Classes: {subject_classifier.model.classes_ if hasattr(subject_classifier, 'model') and subject_classifier.model else 'Not loaded'}")
    print(f"Difficulty Model Classes: {difficulty_classifier.model.classes_ if hasattr(difficulty_classifier, 'model') and difficulty_classifier.model else 'Not loaded'}")
    
    print("\n" + "="*70)
    print("Testing Questions:")
    print("="*70 + "\n")
    
    for question in questions:
        result = classify_question(question)
        
        print(f"❓ Question: {question}")
        print(f"   📚 Subject: {result['subject']} ({result['subject_confidence']:.2%})")
        print(f"   🎯 Difficulty: {result['difficulty']} ({result['difficulty_confidence']:.2%})")
        print()

if __name__ == '__main__':
    test_questions = [
        "what is python",
        "what is python programming language",
        "explain python programming",
        "how to code in python",
        "what are variables in python",
        "what is the capital of France",
        "explain photosynthesis",
        "what is calculus",
        "who was Shakespeare"
    ]
    
    test_classification(test_questions)
