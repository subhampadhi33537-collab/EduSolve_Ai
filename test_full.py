import requests
import json
import time

# Test question submission with debounce check
url = "http://localhost:5000/api/ask"
payload = {
    "question": "what is javascript"
}

print("Testing question submission with debounce protection")
print("=" * 60)

# Get initial count
stats_before = requests.get("http://localhost:5000/api/stats").json()
count_before = stats_before['data']['total_questions']
print(f"Questions before: {count_before}")

# Submit question  
response = requests.post(url, json=payload)
data = response.json()

print(f"\n✅ Status: {data['status']}")
print(f"📚 Subject: {data['data']['subject']}")
print(f"🎯 Difficulty: {data['data']['difficulty']}")
print(f"\n💡 Explanation (first 200 chars):")
print(data['data']['explanation'][:200] + "...")

# Check if ** markdown is present
if '**' in data['data']['explanation']:
    print("\n⚠️  Warning: ** markdown still present in response")
else:
    print("\n✅ No ** markdown in response (will be stripped by frontend)")

# Get final count
time.sleep(1)
stats_after = requests.get("http://localhost:5000/api/stats").json()
count_after = stats_after['data']['total_questions']
print(f"\nQuestions after: {count_after}")

if count_after == count_before + 1:
    print("✅ Question count increased by exactly 1 (no duplicates!)")
else:
    print(f"⚠️  Question count increased by {count_after - count_before}")
