"""
NLP Preprocessing module for EduSolve AI
Handles text cleaning, tokenization, and feature extraction
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('corpora/wordnet_ic')
except LookupError:
    try:
        nltk.download('wordnet_ic', quiet=True)
    except:
        pass  # This is optional and may not be available

class TextPreprocessor:
    """
    Handles all text preprocessing tasks:
    - Text cleaning
    - Lowercasing
    - Tokenization
    - Stop word removal
    - Lemmatization
    """
    
    def __init__(self):
        """Initialize preprocessor with stopwords and lemmatizer"""
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """
        Remove special characters, URLs, and extra whitespace
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned text
        """
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits (except spaces and common punctuation)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def lowercase(self, text):
        """Convert text to lowercase"""
        return text.lower()
    
    def tokenize(self, text):
        """
        Split text into individual words
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of tokens
        """
        tokens = word_tokenize(text)
        return tokens
    
    def remove_stopwords(self, tokens):
        """
        Remove common English stopwords
        
        Args:
            tokens (list): List of word tokens
            
        Returns:
            list: Filtered tokens
        """
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def lemmatize(self, tokens):
        """
        Reduce words to their base form (lemma)
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Preprocessed text
            list: List of processed tokens
        """
        # Apply preprocessing steps
        text = self.clean_text(text)
        text = self.lowercase(text)
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.lemmatize(tokens)
        
        # Return both processed text and tokens
        processed_text = ' '.join(tokens)
        
        return processed_text, tokens

# Global preprocessor instance
preprocessor = TextPreprocessor()

def preprocess_input(text):
    """
    Convenience function for preprocessing text
    
    Args:
        text (str): Input text
        
    Returns:
        tuple: (processed_text, tokens)
    """
    return preprocessor.preprocess(text)
