"""
Generate Diverse Training Data for ML Models
This script creates 10,000+ diverse training samples for subject and difficulty classification
"""

import os
import sys
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Define training data structure
SUBJECTS = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Geography']
DIFFICULTIES = ['Easy', 'Medium', 'Hard']

# Sample questions for each subject and difficulty
MATH_EASY = [
    'basic arithmetic', 'simple division', 'addition problem', 'subtraction', 'multiplication',
    'fractions', 'decimals', 'percentages', 'simple geometry', 'counting'
]

MATH_MEDIUM = [
    'quadratic equation', 'algebra', 'trigonometry', 'calculus basics', 'derivatives',
    'integrals', 'probability', 'statistics', 'linear equations', 'polynomials'
]

MATH_HARD = [
    'differential equations', 'complex analysis', 'linear algebra', 'abstract algebra',
    'topology', 'number theory', 'proof by induction', 'eigenvalues', 'matrix theory', 'limit theory'
]

PHYSICS_EASY = [
    'velocity', 'acceleration', 'force', 'Newton laws', 'simple machines',
    'energy', 'motion', 'gravity', 'friction', 'pressure'
]

PHYSICS_MEDIUM = [
    'thermodynamics', 'waves', 'sound', 'optics', 'electricity',
    'magnetism', 'circuit', 'momentum', 'angular velocity', 'circular motion'
]

PHYSICS_HARD = [
    'relativity', 'quantum mechanics', 'wave particle duality', 'Schrodinger equation',
    'field theory', 'electromagnetism', 'spacetime', 'black holes', 'string theory', 'quantum entanglement'
]

CHEMISTRY_EASY = [
    'periodic table', 'elements', 'atoms', 'molecules', 'chemical bonds',
    'pH scale', 'acids bases', 'oxidation', 'reduction', 'states of matter'
]

CHEMISTRY_MEDIUM = [
    'chemical reactions', 'stoichiometry', 'equilibrium', 'kinetics', 'thermochemistry',
    'electrochemistry', 'organic chemistry', 'functional groups', 'bonding theory', 'solutions'
]

CHEMISTRY_HARD = [
    'quantum chemistry', 'spectroscopy', 'crystallography', 'polymer chemistry', 'nanotechnology',
    'surface chemistry', 'coordination chemistry', 'nuclear chemistry', 'astrochemistry', 'biochemistry'
]

BIOLOGY_EASY = [
    'cells', 'photosynthesis', 'respiration', 'DNA', 'chromosomes',
    'genetics', 'traits', 'evolution', 'ecology', 'organisms'
]

BIOLOGY_MEDIUM = [
    'mitosis', 'meiosis', 'protein synthesis', 'gene expression', 'mutations',
    'natural selection', 'adaptation', 'ecosystems', 'food chain', 'reproduction'
]

BIOLOGY_HARD = [
    'molecular biology', 'bioinformatics', 'genetic engineering', 'CRISPR', 'epigenetics',
    'neurobiology', 'developmental biology', 'immunology', 'cancer biology', 'systems biology'
]

ENGLISH_EASY = [
    'parts of speech', 'grammar', 'punctuation', 'sentence structure', 'vocabulary',
    'pronunciation', 'spelling', 'reading comprehension', 'writing basics', 'nouns verbs'
]

ENGLISH_MEDIUM = [
    'literature analysis', 'poetry', 'symbolism', 'themes', 'literary devices',
    'narrative structure', 'character development', 'plot', 'writing essays', 'dialogue'
]

ENGLISH_HARD = [
    'postmodern literature', 'deconstruction', 'literary criticism', 'semiotics', 'discourse analysis',
    'rhetorical strategies', 'narrative theory', 'intertextuality', 'metafiction', 'stream of consciousness'
]

HISTORY_EASY = [
    'ancient civilizations', 'historical figures', 'dates and events', 'ancient rome', 'ancient greece',
    'egyptians', 'empires', 'dynasties', 'kingdoms', 'chronology'
]

HISTORY_MEDIUM = [
    'renaissance', 'enlightenment', 'industrial revolution', 'world wars', 'revolutions',
    'political movements', 'cultural changes', 'social history', 'medieval period', 'colonialism'
]

HISTORY_HARD = [
    'historiography', 'geopolitics', 'cultural relativism', 'world systems theory', 'historical analysis',
    'revisionism', 'postcolonial studies', 'microhistory', 'historical methodology', 'transnational history'
]

GEOGRAPHY_EASY = [
    'capitals', 'continents', 'countries', 'oceans', 'rivers',
    'mountains', 'borders', 'time zones', 'map reading', 'coordinates'
]

GEOGRAPHY_MEDIUM = [
    'tectonic plates', 'earthquakes', 'weather', 'climate', 'biomes',
    'ecosystems', 'water cycle', 'erosion', 'landforms', 'natural resources'
]

GEOGRAPHY_HARD = [
    'geopolitics', 'climate change', 'globalization', 'sustainable development', 'urban planning',
    'demographic patterns', 'cultural geography', 'political geography', 'GIS technology', 'environmental geography'
]

# Create templates for question generation
QUESTION_TEMPLATES = {
    'Mathematics': {'Easy': MATH_EASY, 'Medium': MATH_MEDIUM, 'Hard': MATH_HARD},
    'Physics': {'Easy': PHYSICS_EASY, 'Medium': PHYSICS_MEDIUM, 'Hard': PHYSICS_HARD},
    'Chemistry': {'Easy': CHEMISTRY_EASY, 'Medium': CHEMISTRY_MEDIUM, 'Hard': CHEMISTRY_HARD},
    'Biology': {'Easy': BIOLOGY_EASY, 'Medium': BIOLOGY_MEDIUM, 'Hard': BIOLOGY_HARD},
    'English': {'Easy': ENGLISH_EASY, 'Medium': ENGLISH_MEDIUM, 'Hard': ENGLISH_HARD},
    'History': {'Easy': HISTORY_EASY, 'Medium': HISTORY_MEDIUM, 'Hard': HISTORY_HARD},
    'Geography': {'Easy': GEOGRAPHY_EASY, 'Medium': GEOGRAPHY_MEDIUM, 'Hard': GEOGRAPHY_HARD},
}

# Question generation templates
QUESTION_STARTERS = [
    'What is', 'How do you', 'Explain', 'Why is', 'Can you', 'Define',
    'Describe', 'What does', 'Which of', 'How is', 'What are', 'Where is',
    'When did', 'Who was', 'How would', 'What would', 'Is it true that',
    'Compare', 'Contrast', 'Analyze', 'Evaluate', 'Solve', 'Calculate',
    'Determine', 'Prove', 'Discuss', 'List', 'Name', 'Identify'
]

QUESTION_ENDINGS = [
    'in detail?', 'fundamentally?', 'in nature?', 'practically?',
    'theoretically?', 'historically?', 'scientifically?', 'generally?',
    'approximately?', 'exactly?', 'typically?', 'usually?', 'always?'
]

def generate_diverse_questions(topic, count=100):
    """Generate diverse question variations from a topic"""
    questions = []
    
    for i in range(count):
        # Vary the question structure
        starter = random.choice(QUESTION_STARTERS)
        ending = random.choice(QUESTION_ENDINGS)
        
        # Create variations
        variations = [
            f"{starter} {topic}{random.choice(['', ' in detail'])}?",
            f"{starter} the relationship between {topic} and {random.choice(['learning', 'application', 'development'])}?",
            f"{starter} {topic}? {random.choice(['What is', 'How does', 'Why is'])} it important?",
            f"{starter} {topic} {ending}",
            f"How would you apply {topic} {random.choice(['in practice', 'to real world', 'in solving problems'])}?",
        ]
        
        questions.append(random.choice(variations))
    
    return questions[:count]

def generate_training_data(target_size=10000):
    """
    Generate large diverse training dataset
    
    Args:
        target_size (int): Target number of training samples (default 10000)
    """
    
    print("\n" + "="*70)
    print("🤖 EduSolve AI - Training Data Generator")
    print(f"Target: {target_size:,} samples across {len(SUBJECTS)} subjects")
    print("="*70 + "\n")
    
    training_data = []
    samples_per_difficulty = target_size // (len(SUBJECTS) * len(DIFFICULTIES))
    
    print(f"📊 Generation Plan:")
    print(f"   • Subjects: {len(SUBJECTS)}")
    print(f"   • Difficulty levels: {len(DIFFICULTIES)}")
    print(f"   • Samples per combination: ~{samples_per_difficulty}")
    print(f"   • Total expected: {len(SUBJECTS) * len(DIFFICULTIES) * samples_per_difficulty:,}\n")
    
    sample_count = 0
    
    for subject in SUBJECTS:
        print(f"📚 {subject}")
        
        for difficulty in DIFFICULTIES:
            # Get topics for this subject/difficulty combo
            topics = QUESTION_TEMPLATES[subject][difficulty]
            
            # Generate questions for each topic
            for topic in topics:
                # Generate multiple variations per topic
                questions = generate_diverse_questions(topic, samples_per_difficulty // len(topics))
                
                for question in questions:
                    training_data.append({
                        'question': question.strip(),
                        'subject': subject,
                        'difficulty': difficulty,
                        'topic': topic,
                        'timestamp': datetime.now().isoformat()
                    })
                    sample_count += 1
            
            print(f"   ↳ {difficulty}: +{samples_per_difficulty} samples")
    
    print(f"\n✅ Generated {sample_count:,} training samples")
    
    # Save training data
    data_file = 'data/training_data.json'
    os.makedirs('data', exist_ok=True)
    
    with open(data_file, 'w') as f:
        json.dump(training_data, f, indent=2)
    
    print(f"💾 Saved to: {data_file}")
    
    # Display statistics
    print_statistics(training_data)
    
    return training_data

def print_statistics(training_data):
    """Print detailed statistics about the training data"""
    
    print(f"\n📊 Training Data Statistics:")
    print(f"   Total samples: {len(training_data):,}")
    
    # Count by subject
    subject_counts = {}
    for item in training_data:
        subject = item['subject']
        subject_counts[subject] = subject_counts.get(subject, 0) + 1
    
    print(f"\n   By Subject:")
    for subject in SUBJECTS:
        count = subject_counts.get(subject, 0)
        percentage = (count / len(training_data)) * 100
        print(f"      • {subject}: {count:,} ({percentage:.1f}%)")
    
    # Count by difficulty
    difficulty_counts = {}
    for item in training_data:
        difficulty = item['difficulty']
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
    
    print(f"\n   By Difficulty:")
    for difficulty in DIFFICULTIES:
        count = difficulty_counts.get(difficulty, 0)
        percentage = (count / len(training_data)) * 100
        print(f"      • {difficulty}: {count:,} ({percentage:.1f}%)")
    
    # Sample length statistics
    lengths = [len(item['question'].split()) for item in training_data]
    print(f"\n   Question Characteristics:")
    print(f"      • Average length: {sum(lengths) / len(lengths):.1f} words")
    print(f"      • Min length: {min(lengths)} words")
    print(f"      • Max length: {max(lengths)} words")
    
    return subject_counts, difficulty_counts

def verify_training_data(training_data):
    """Verify the training data quality"""
    
    print("\n🔍 Verifying training data...")
    
    issues = []
    required_fields = ['question', 'subject', 'difficulty']
    
    # Check structure
    for i, item in enumerate(training_data):
        # Check required fields
        for field in required_fields:
            if field not in item:
                issues.append(f"Item {i}: Missing '{field}' field")
        
        # Validate values
        if item.get('subject') not in SUBJECTS:
            issues.append(f"Item {i}: Invalid subject")
        
        if item.get('difficulty') not in DIFFICULTIES:
            issues.append(f"Item {i}: Invalid difficulty")
        
        # Check question quality
        if not item.get('question', '').strip():
            issues.append(f"Item {i}: Empty question")
        
        if len(item.get('question', '').split()) < 2:
            issues.append(f"Item {i}: Question too short")
    
    # Check for duplicates
    questions = [item['question'] for item in training_data]
    if len(questions) != len(set(questions)):
        duplicate_count = len(questions) - len(set(questions))
        print(f"   ⚠️  {duplicate_count} duplicate questions found")
    
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues[:10]:
            print(f"   • {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more")
        return False
    
    print("✅ All validation checks passed!")
    return True

if __name__ == '__main__':
    try:
        # Generate training data
        training_data = generate_training_data(target_size=10000)
        
        # Verify data
        is_valid = verify_training_data(training_data)
        
        if is_valid:
            print("\n" + "="*70)
            print("✨ Training data generation completed successfully!")
            print("="*70)
            print(f"\n🎯 Ready to train models with {len(training_data):,} samples!\n")
        else:
            print("\n⚠️ Training data has issues but will be saved anyway")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
