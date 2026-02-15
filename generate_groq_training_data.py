"""
Generate 10,000+ Training Data Samples using Groq API
This script fetches diverse question-answer pairs from Groq API for ML model training
"""

import os
import sys
import json
import time
import random
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = os.getenv('GROQ_API_URL')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')

OUTPUT_FILE = 'data/training_data.json'
TARGET_SAMPLES = 10000

# Subject definitions
SUBJECTS = {
    'Mathematics': ['algebra', 'calculus', 'geometry', 'statistics', 'trigonometry', 'linear algebra', 'differential equations'],
    'Physics': ['mechanics', 'thermodynamics', 'electromagnetism', 'quantum mechanics', 'optics', 'waves', 'relativity'],
    'Chemistry': ['organic chemistry', 'inorganic chemistry', 'physical chemistry', 'biochemistry', 'analytical chemistry'],
    'Biology': ['cell biology', 'genetics', 'ecology', 'evolution', 'anatomy', 'microbiology', 'botany'],
    'Computer Science': ['programming', 'algorithms', 'data structures', 'databases', 'AI', 'machine learning', 'networks'],
    'English': ['grammar', 'literature', 'poetry', 'writing', 'vocabulary', 'essay writing'],
    'History': ['world history', 'ancient civilizations', 'modern history', 'wars', 'revolutions'],
    'Geography': ['physical geography', 'human geography', 'cartography', 'climate', 'ecosystems']
}

DIFFICULTIES = {
    'Easy': 'basic understanding, simple concepts',
    'Medium': 'intermediate level, requires analysis',
    'Hard': 'advanced level, complex problem-solving'
}

def generate_batch_questions_with_groq(subject, topics, difficulty, batch_size=20):
    """
    Generate multiple questions in one API call for efficiency
    
    Args:
        subject: Subject area
        topics: List of topics within the subject
        difficulty: Difficulty level
        batch_size: Number of questions to generate in one call
        
    Returns:
        list: Generated questions
    """
    topics_str = ', '.join(topics[:5])  # Use first 5 topics
    
    prompt = f"""Generate {batch_size} diverse student questions about {subject}.
Topics to cover: {topics_str}
Difficulty level: {difficulty} ({DIFFICULTIES[difficulty]})

Requirements:
- Each question should be realistic (as students would ask)
- Clear and specific
- Between 10-50 words each
- Cover different aspects of the topics
- No numbering or formatting

Output format: One question per line, nothing else."""

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': GROQ_MODEL,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.9,
                'max_tokens': 2000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Split by newlines and clean
            questions = []
            for line in content.split('\n'):
                line = line.strip()
                # Remove numbering like "1.", "1)", etc.
                line = line.lstrip('0123456789.)- ')
                if len(line) > 10 and not line.startswith(('Generate', 'Question', 'Output')):
                    questions.append(line)
            
            return questions[:batch_size]  # Ensure we don't exceed batch size
        
        return []
        
    except Exception as e:
        print(f"Error in batch generation: {str(e)}")
        return []

def generate_training_dataset(target_count=TARGET_SAMPLES):
    """
    Generate a large training dataset using Groq API with batch processing
    
    Args:
        target_count: Number of samples to generate
        
    Returns:
        list: Training data samples
    """
    print(f"\n{'='*70}")
    print(f"🤖 Generating {target_count:,} Training Samples with Groq API")
    print(f"{'='*70}\n")
    
    training_data = []
    subjects_list = list(SUBJECTS.keys())
    difficulties_list = list(DIFFICULTIES.keys())
    
    successful = 0
    failed = 0
    start_time = time.time()
    
    # Batch configuration
    BATCH_SIZE = 20  # Generate 20 questions per API call
    
    # Calculate batches needed
    samples_per_subject = target_count // len(subjects_list)
    samples_per_difficulty = samples_per_subject // len(difficulties_list)
    batches_needed = (samples_per_difficulty + BATCH_SIZE - 1) // BATCH_SIZE
    
    for subject in subjects_list:
        topics = SUBJECTS[subject]
        print(f"\n📚 Generating ~{samples_per_subject} samples for {subject}...")
        
        for difficulty in difficulties_list:
            print(f"   🎯 {difficulty} level...")
            
            for batch_num in range(batches_needed):
                # Generate batch of questions
                questions = generate_batch_questions_with_groq(
                    subject, topics, difficulty, BATCH_SIZE
                )
                
                if questions:
                    # Create training samples from batch
                    for question in questions:
                        if question and len(question) > 10:
                            sample = {
                                'question': question,
                                'subject': subject,
                                'difficulty': difficulty,
                                'topic': random.choice(topics),
                                'generated': True,
                                'batch': batch_num
                            }
                            training_data.append(sample)
                            successful += 1
                    
                    # Progress indicator
                    elapsed = time.time() - start_time
                    rate = successful / elapsed if elapsed > 0 else 0
                    remaining = (target_count - successful) / rate if rate > 0 else 0
                    
                    print(f"      ✓ {successful:,}/{target_count:,} samples "
                          f"({rate:.1f}/sec, ~{remaining/60:.1f} min left)")
                    
                    # Delay to avoid rate limiting
                    time.sleep(0.5)
                else:
                    failed += BATCH_SIZE
                    print(f"      ⚠️  Batch failed (total failures: {failed})")
                
                # Stop if we've reached target
                if successful >= target_count:
                    break
            
            if successful >= target_count:
                break
        
        if successful >= target_count:
            break
    
    # Save to file
    if training_data:
        os.makedirs('data', exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*70}")
        print(f"✅ Successfully generated {successful:,} training samples!")
        print(f"❌ Failed attempts: {failed}")
        print(f"⏱️  Time taken: {elapsed_time/60:.2f} minutes")
        print(f"⚡ Average rate: {successful/elapsed_time:.1f} samples/second")
        print(f"💾 Saved to: {OUTPUT_FILE}")
        print(f"📊 Success rate: {successful/(successful+failed)*100:.1f}%")
        print(f"{'='*70}\n")
        
        # Distribution statistics
        print("\n📊 Distribution Statistics:")
        print(f"{'Subject':<20} {'Easy':<10} {'Medium':<10} {'Hard':<10} {'Total':<10}")
        print("-" * 60)
        
        for subject in subjects_list:
            easy = sum(1 for s in training_data if s['subject'] == subject and s['difficulty'] == 'Easy')
            medium = sum(1 for s in training_data if s['subject'] == subject and s['difficulty'] == 'Medium')
            hard = sum(1 for s in training_data if s['subject'] == subject and s['difficulty'] == 'Hard')
            total = easy + medium + hard
            print(f"{subject:<20} {easy:<10} {medium:<10} {hard:<10} {total:<10}")
        
        return training_data
    else:
        print("\n❌ No training data generated!")
        return []

def validate_environment():
    """Validate that environment is properly configured"""
    if not GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not found in environment variables!")
        print("   Please set it in your .env file.")
        return False
    
    print("✅ Environment validated successfully!")
    return True

def main():
    """Main execution function"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   🤖 Groq-Powered Training Data Generator 🤖           ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Validate environment
    if not validate_environment():
        return
    
    # Ask user for confirmation
    print(f"\n⚠️  This will generate {TARGET_SAMPLES:,} samples using Groq API.")
    print(f"⏱️  Estimated time: {TARGET_SAMPLES * 0.15 / 60:.1f} - {TARGET_SAMPLES * 0.25 / 60:.1f} minutes")
    print(f"💰 Cost: This may consume API credits.")
    
    response = input("\n➡️  Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        return
    
    # Generate dataset
    dataset = generate_training_dataset(TARGET_SAMPLES)
    
    if dataset:
        print("\n✨ Training data generation complete!")
        print(f"📁 Next step: Run 'python train_models.py' to train models with this data.")
    else:
        print("\n❌ Training data generation failed!")

if __name__ == '__main__':
    main()
