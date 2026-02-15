"""
Groq API Client for EduSolve AI
Handles integration with Groq's generative AI models
"""

import json
import requests
from config import Config

class GroqClient:
    """
    Client for communicating with Groq API
    Sends questions and receives AI-generated explanations
    """
    
    def __init__(self):
        """Initialize Groq client with API configuration"""
        self.api_key = Config.GROQ_API_KEY
        self.api_url = Config.GROQ_API_URL
        self.model = Config.GROQ_MODEL
        self.max_tokens = Config.GROQ_MAX_TOKENS
        self.temperature = Config.GROQ_TEMPERATURE
        
        # Validate configuration
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set")
        if not self.api_url:
            raise ValueError("GROQ_API_URL is not set")
    
    def get_explanation(self, question, subject, difficulty):
        """
        Get AI-generated explanation for a question from Groq API
        
        Args:
            question (str): The student's doubt/question
            subject (str): Classified subject of the question
            difficulty (str): Classified difficulty level
            
        Returns:
            dict: Response containing explanation and metadata
                {
                    'explanation': str,
                    'status': 'success' or 'error',
                    'error_message': str (if error)
                }
        """
        try:
            # Construct the prompt with context
            prompt = self._construct_prompt(question, subject, difficulty)
            
            # Prepare request headers
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Prepare request payload
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a concise tutor. Give brief, clear answers in simple language. Focus on key points only. Do not use markdown like ** or ##. Write in plain text.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }
            
            print(f"Sending request to Groq API...")
            print(f"Model: {self.model}")
            print(f"Question: {question[:50]}...")
            
            # Make API request
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Check if request was successful
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract explanation from response
                explanation = response_data['choices'][0]['message']['content']
                
                return {
                    'explanation': explanation,
                    'status': 'success',
                    'model_used': self.model,
                    'tokens_used': response_data['usage']['total_tokens']
                }
            
            else:
                error_message = f"Groq API Error {response.status_code}: {response.text}"
                print(f"Error: {error_message}")
                
                return {
                    'explanation': None,
                    'status': 'error',
                    'error_message': error_message
                }
        
        except requests.exceptions.RequestException as e:
            error_message = f"Request failed: {str(e)}"
            print(f"Error: {error_message}")
            
            return {
                'explanation': None,
                'status': 'error',
                'error_message': error_message
            }
        
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            print(f"Error: {error_message}")
            
            return {
                'explanation': None,
                'status': 'error',
                'error_message': error_message
            }
    
    def _construct_prompt(self, question, subject, difficulty):
        """
        Construct a well-structured prompt for the AI model
        
        Args:
            question (str): The student's question
            subject (str): Subject of the question
            difficulty (str): Difficulty level
            
        Returns:
            str: Formatted prompt
        """
        prompt = f"""
Question: {question}

Provide a brief, clear explanation in this format:

What is [topic]?
[Answer in 2-3 sentences]

Key Points:
1. [First key point]
2. [Second key point]
3. [Third key point]

Example:
[Simple example if needed]

Keep it concise and educational.
"""
        return prompt.strip()

# Global Groq client instance
groq_client = GroqClient()

def get_ai_explanation(question, subject, difficulty):
    """
    Convenience function to get explanation from Groq
    
    Args:
        question (str): The student's question
        subject (str): Subject classification
        difficulty (str): Difficulty classification
        
    Returns:
        dict: Explanation response
    """
    return groq_client.get_explanation(question, subject, difficulty)
