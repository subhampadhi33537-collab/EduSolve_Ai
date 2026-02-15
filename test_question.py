"""
Quick test script to ask a question to the running server
"""

import requests
import json

API_URL = 'http://localhost:5000/api/ask'

def test_question(question):
    """Test asking a question to the API"""
    
    print(f"\n{'='*70}")
    print(f"🧪 Testing Question: {question}")
    print(f"{'='*70}\n")
    
    try:
        response = requests.post(
            API_URL,
            json={'question': question},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract data from nested structure
            data = result.get('data', result)  # Handle both nested and flat responses
            status = result.get('status', 'unknown')
            
            print(f"✅ Status: {status}")
            print(f"\n📚 Subject: {data.get('subject', 'N/A')}")
            print(f"   Confidence: {data.get('subject_confidence', 0):.2%}")
            
            print(f"\n🎯 Difficulty: {data.get('difficulty', 'N/A')}")
            print(f"   Confidence: {data.get('difficulty_confidence', 0):.2%}")
            
            print(f"\n💡 Explanation:")
            print("-" * 70)
            explanation = data.get('explanation', 'No explanation provided')
            print(explanation[:500] + ('...' if len(explanation) > 500 else ''))
            print("-" * 70)
            
            print(f"\n⏱️  Timestamp: {data.get('timestamp', 'N/A')}")
            
            # Save full response
            with open('test_response.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full response saved to: test_response.json")
            
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    # Test the question
    test_question("what is python")
