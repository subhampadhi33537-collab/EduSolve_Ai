"""
Debug specific question to see keyword matching
"""

import sys
import os
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import ml_model
importlib.reload(ml_model)

from ml_model import classify_question

# Test specific question
question = "what is the capital of France"
question_lower = question.lower()

# Check each keyword set
cs_keywords = ['python', 'java', 'code', 'programming', 'algorithm', 'function',
               'variable', 'loop', 'array', 'class', 'object', 'software',
               'database', 'api', 'html', 'css', 'javascript', 'computer']

geo_keywords = ['capital', 'country', 'continent', 'ocean', 'mountain',
                'river', 'climate', 'geography', 'map', 'location']

print(f"Question: {question}")
print(f"\nCS keyword matches:")
cs_matches = [kw for kw in cs_keywords if kw in question_lower]
print(f"  {cs_matches} (count: {len(cs_matches)})")

print(f"\nGeography keyword matches:")
geo_matches = [kw for kw in geo_keywords if kw in question_lower]
print(f"  {geo_matches} (count: {len(geo_matches)})")

print(f"\n\nClassification result:")
result = classify_question(question)
print(f"Subject: {result['subject']} ({result['subject_confidence']:.2%})")
