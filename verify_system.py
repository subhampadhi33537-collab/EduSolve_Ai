"""
Comprehensive System Verification Script
Checks all components and connections before running the application
"""

import os
import sys
import json
import pickle

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def check_python_version():
    """Check Python version"""
    print("\n✓ Python Version Check:")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_environment_variables():
    """Check environment variables"""
    print("\n✓ Environment Variables Check:")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['GROQ_API_KEY', 'GROQ_API_URL', 'GROQ_MODEL']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            preview = value[:20] + '...' if len(value) > 20 else value
            print(f"  ✓ {var}: {preview}")
        else:
            print(f"  ✗ {var}: MISSING")
            missing.append(var)
    
    return len(missing) == 0

def check_model_files():
    """Check if ML model files exist and are valid"""
    print("\n✓ ML Model Files Check:")
    
    models_dir = 'models'
    required_models = ['subject_model.pkl', 'difficulty_model.pkl']
    all_exist = True
    
    for model_file in required_models:
        path = os.path.join(models_dir, model_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {model_file} ({size} bytes)")
            
            # Try to load and verify
            try:
                with open(path, 'rb') as f:
                    model = pickle.load(f)
                print(f"    → Successfully loaded")
            except Exception as e:
                print(f"    → Error loading: {str(e)}")
                all_exist = False
        else:
            print(f"  ✗ {model_file}: NOT FOUND")
            all_exist = False
    
    return all_exist

def check_training_data():
    """Check if training data exists and is valid"""
    print("\n✓ Training Data Check:")
    
    data_file = 'data/training_data.json'
    
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            print(f"  ✓ training_data.json ({os.path.getsize(data_file)} bytes)")
            print(f"    → {len(data)} training samples loaded")
            
            # Verify structure
            if len(data) > 0:
                sample = data[0]
                required_fields = ['question', 'subject', 'difficulty']
                missing_fields = [f for f in required_fields if f not in sample]
                
                if missing_fields:
                    print(f"    ✗ Missing fields: {missing_fields}")
                    return False
                else:
                    print(f"    ✓ Data structure valid")
                    
                    # Count by subject
                    subjects = {}
                    for item in data:
                        subject = item.get('subject', 'Unknown')
                        subjects[subject] = subjects.get(subject, 0) + 1
                    
                    print(f"    → Subjects: {', '.join(f'{s}({c})' for s, c in sorted(subjects.items()))}")
                    
            return True
        except Exception as e:
            print(f"  ✗ Error loading training data: {str(e)}")
            return False
    else:
        print(f"  ✗ training_data.json: NOT FOUND")
        return False

def check_frontend_files():
    """Check if frontend files exist"""
    print("\n✓ Frontend Files Check:")
    
    checks = {
        'Templates': {
            'index.html': 'frontend/templates/index.html',
            'dashboard.html': 'frontend/templates/dashboard.html',
            'features.html': 'frontend/templates/features.html',
            'about.html': 'frontend/templates/about.html',
        },
        'CSS Files': {
            'style.css': 'frontend/static/css/style.css',
            'navigation.css': 'frontend/static/css/navigation.css',
            'home.css': 'frontend/static/css/home.css',
            'dashboard.css': 'frontend/static/css/dashboard.css',
        },
        'JavaScript Files': {
            'script.js': 'frontend/static/js/script.js',
            'dashboard.js': 'frontend/static/js/dashboard.js',
            'features.js': 'frontend/static/js/features.js',
        }
    }
    
    all_exist = True
    
    for category, files in checks.items():
        print(f"\n  {category}:")
        for name, path in files.items():
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"    ✓ {name} ({size} bytes)")
            else:
                print(f"    ✗ {name}: NOT FOUND")
                all_exist = False
    
    return all_exist

def check_python_packages():
    """Check required Python packages"""
    print("\n✓ Python Packages Check:")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'sklearn': 'scikit-learn',
        'requests': 'requests',
        'nltk': 'nltk',
        'numpy': 'numpy'
    }
    
    all_installed = True
    
    for import_name, display_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ {display_name}")
        except ImportError:
            print(f"  ✗ {display_name}: NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_ml_models():
    """Test ML models with sample data"""
    print("\n✓ ML Model Functionality Check:")
    
    try:
        from ml_model import classify_question
        
        # Test with a sample question
        test_question = "What is the derivative of x squared?"
        classification = classify_question(test_question)
        
        print(f"  Test Question: '{test_question}'")
        print(f"  ✓ Subject: {classification['subject']} ({classification['subject_confidence']:.2%})")
        print(f"  ✓ Difficulty: {classification['difficulty']} ({classification['difficulty_confidence']:.2%})")
        
        return True
    except Exception as e:
        print(f"  ✗ Model test failed: {str(e)}")
        return False

def check_groq_connection():
    """Test Groq API connection"""
    print("\n✓ Groq API Connection Check:")
    
    try:
        from config import Config
        
        if not Config.GROQ_API_KEY:
            print("  ✗ GROQ_API_KEY not configured")
            return False
        
        print(f"  ✓ API Key configured")
        print(f"  ✓ API URL: {Config.GROQ_API_URL}")
        print(f"  ✓ Model: {Config.GROQ_MODEL}")
        print(f"  → Note: Full API test requires active request (will test on first use)")
        
        return True
    except Exception as e:
        print(f"  ✗ Groq configuration error: {str(e)}")
        return False

def main():
    """Run all checks"""
    
    print("\n" + "="*70)
    print("🔍 EduSolve AI - COMPREHENSIVE SYSTEM VERIFICATION")
    print("="*70)
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment Variables", check_environment_variables),
        ("ML Model Files", check_model_files),
        ("Training Data", check_training_data),
        ("Frontend Files", check_frontend_files),
        ("Python Packages", check_python_packages),
        ("ML Model Functionality", check_ml_models),
        ("Groq API Configuration", check_groq_connection),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
        except Exception as e:
            print(f"\n✗ {check_name} failed with error: {str(e)}")
            results[check_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 VERIFICATION SUMMARY")
    print("="*70)
    
    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print("\n" + "-"*70)
    print(f"Overall Status: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n✨ All systems operational! Ready to launch the application.")
        print("\n💚 GREEN THEME WITH FULL FUNCTIONALITY ACTIVATED!")
        print("="*70 + "\n")
        return True
    else:
        print(f"\n⚠️  {total_checks - passed_checks} checks failed. Please review the issues above.")
        print("="*70 + "\n")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
