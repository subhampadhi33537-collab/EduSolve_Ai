"""
Train ML Models for EduSolve AI
This script retrains the subject and difficulty classifiers
"""

import os
import sys
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.ml_model import SubjectClassifier, DifficultyClassifier

def train_models():
    """Train both subject and difficulty models"""
    
    print("\n" + "="*60)
    print("🤖 EduSolve AI - ML Model Training")
    print("="*60 + "\n")
    
    # Load training data
    data_file = 'data/training_data.json'
    
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
        
        if len(training_data) > 0:
            print(f"📊 Found {len(training_data)} training samples")
            
            # Extract questions and labels
            questions = [item['question'] for item in training_data]
            subjects = [item['subject'] for item in training_data]
            difficulties = [item['difficulty'] for item in training_data]
            
            # Train subject classifier
            print("\n🎯 Training Subject Classifier...")
            subject_model = SubjectClassifier()
            subject_model.train(questions, subjects)
            
            # Train difficulty classifier
            print("\n📊 Training Difficulty Classifier...")
            difficulty_model = DifficultyClassifier()
            difficulty_model.train(questions, difficulties)
            
            print("\n✅ Model training completed successfully!")
            print(f"📁 Models saved to: models/")
            
        else:
            print("⚠️  No training data found. Using default sample data...")
            train_default_models()
    else:
        print("⚠️  Training data file not found. Using default sample data...")
        train_default_models()
    
    print("\n" + "="*60)
    print("✨ Ready to use!")
    print("="*60 + "\n")

def train_default_models():
    """Train models with default sample data"""
    
    # Enhanced sample data for better initial performance
    sample_questions = [
        # Mathematics
        "How do I solve a quadratic equation using the quadratic formula?",
        "What is the derivative of x squared?",
        "Explain the Pythagorean theorem",
        "How to find the area of a circle?",
        "What is integration in calculus?",
        "Solve for x in the equation 2x + 5 = 15",
        
        # Physics
        "What is Newton's second law of motion?",
        "Explain the relationship between velocity and acceleration",
        "What is the speed of light?",
        "How does gravity work?",
        "What is kinetic energy?",
        "Explain electromagnetic waves",
        
        # Chemistry
        "What is the atomic number of oxygen?",
        "Explain the structure of an atom",
        "What is a chemical bond?",
        "How does photosynthesis work chemically?",
        "What is pH scale?",
        "Explain oxidation and reduction",
        
        # Biology
        "What is photosynthesis in plants?",
        "How does DNA replication work?",
        "What is mitosis?",
        "Explain the human circulatory system",
        "What are cells made of?",
        "How do vaccines work?",
        
        # English
        "Who wrote Romeo and Juliet?",
        "What is a metaphor in literature?",
        "Explain verb tenses",
        "What is Shakespeare famous for?",
        "Define a noun",
        "What is alliteration?",
        
        # History
        "Who was the first president of the United States?",
        "When did World War 2 end?",
        "What was the Renaissance?",
        "Explain the French Revolution",
        "Who was Napoleon Bonaparte?",
        
        # Geography
        "What is the capital of France?",
        "What are tectonic plates?",
        "Explain climate change",
        "What is the largest ocean?",
        "Where is Mount Everest located?"
    ]
    
    sample_subjects = [
        # Mathematics (6)
        'Mathematics', 'Mathematics', 'Mathematics', 'Mathematics', 'Mathematics', 'Mathematics',
        # Physics (6)
        'Physics', 'Physics', 'Physics', 'Physics', 'Physics', 'Physics',
        # Chemistry (6)
        'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry',
        # Biology (6)
        'Biology', 'Biology', 'Biology', 'Biology', 'Biology', 'Biology',
        # English (6)
        'English', 'English', 'English', 'English', 'English', 'English',
        # History (5)
        'History', 'History', 'History', 'History', 'History',
        # Geography (5)
        'Geography', 'Geography', 'Geography', 'Geography', 'Geography'
    ]
    
    sample_difficulties = [
        # Mathematics
        'Medium', 'Easy', 'Medium', 'Easy', 'Hard', 'Easy',
        # Physics
        'Medium', 'Medium', 'Easy', 'Medium', 'Easy', 'Hard',
        # Chemistry
        'Easy', 'Medium', 'Easy', 'Hard', 'Easy', 'Medium',
        # Biology
        'Medium', 'Hard', 'Medium', 'Medium', 'Easy', 'Medium',
        # English
        'Easy', 'Medium', 'Easy', 'Easy', 'Easy', 'Easy',
        # History
        'Easy', 'Easy', 'Medium', 'Medium', 'Medium',
        # Geography
        'Easy', 'Medium', 'Hard', 'Easy', 'Easy'
    ]
    
    print(f"📚 Training with {len(sample_questions)} sample questions...")
    
    # Train subject classifier
    print("\n🎯 Training Subject Classifier...")
    subject_model = SubjectClassifier()
    subject_model.train(sample_questions, sample_subjects)
    
    # Train difficulty classifier
    print("\n📊 Training Difficulty Classifier...")
    difficulty_model = DifficultyClassifier()
    difficulty_model.train(sample_questions, sample_difficulties)
    
    print("\n✅ Default models trained successfully!")

if __name__ == '__main__':
    train_models()
