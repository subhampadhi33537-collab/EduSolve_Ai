import requests
import json

print("\n" + "="*60)
print("Testing Statistics API Endpoint")
print("="*60)

response = requests.get("http://localhost:5000/api/stats")
print(f"\nStatus Code: {response.status_code}")
print(f"\nRaw Response:")
print(json.dumps(response.json(), indent=2))

data = response.json()
if data.get('status') == 'success':
    stats = data.get('data', {})
    print(f"\n✅ Statistics loaded successfully!")
    print(f"   Total Questions: {stats.get('total_questions', 0)}")
    print(f"   Subjects: {list(stats.get('subjects', {}).keys())}")
    print(f"   Difficulties: {stats.get('difficulties', {})}")
