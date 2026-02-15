"""
Configuration module for EduSolve AI
Loads environment variables and sets up application configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    """Base configuration class"""
    
    # Flask configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Groq API configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', 800))
    GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', 0.5))
    
    # File paths - use PROJECT_ROOT for absolute paths
    TRAINING_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'training_data.json')
    LABELS_PATH = os.path.join(PROJECT_ROOT, 'data', 'labels.json')
    SUBJECT_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'subject_model.pkl')
    DIFFICULTY_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'difficulty_model.pkl')
    
    # ML configuration
    MIN_CONFIDENCE = 0.5
    RETRAINING_THRESHOLD = 10
    
    # Server configuration
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))

# Validate required environment variables
if not Config.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

if not Config.GROQ_API_URL:
    raise ValueError("GROQ_API_URL not found in environment variables")
