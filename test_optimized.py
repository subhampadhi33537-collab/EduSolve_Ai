import requests
import json
import time

print("=" * 60)
print("Testing OPTIMIZED App - Book Style & Speed")
print("=" * 60)

# Test question
url = "http://localhost:5000/api/ask"
payload = {
    "question": "what is photosynthesis"
}

print("\n📝 Question: what is photosynthesis")
print("\n⏱️  Measuring response time...")

start_time = time.time()
response = requests.post(url, json=payload)
end_time = time.time()

elapsed_time = end_time - start_time

data = response.json()

print(f"\n⚡ Response Time: {elapsed_time:.2f} seconds")
print(f"✅ Status: {data['status']}")

if data['status'] == 'error':
    print(f"\n❌ Error: {data.get('message', 'Unknown error')}")
    print(f"Details: {json.dumps(data, indent=2)}")
    exit(1)

print(f"📚 Subject: {data['data']['subject']}")
print(f"🎯 Difficulty: {data['data']['difficulty']}")

print(f"\n📖 Explanation (Book Format):")
print("=" * 60)
explanation = data['data']['explanation']
print(explanation)
print("=" * 60)

# Check formatting
print("\n✅ Formatting Analysis:")
if '**' not in explanation:
    print("  ✓ No ** markdown (clean)")
else:
    print("  ⚠ Contains ** markdown")

if len(explanation) < 1000:
    print(f"  ✓ Brief response ({len(explanation)} chars)")
else:
    print(f"  ⚠ Long response ({len(explanation)} chars)")

if elapsed_time < 5:
    print(f"  ✓ Fast response ({elapsed_time:.2f}s)")
else:
    print(f"  ⚠ Slow response ({elapsed_time:.2f}s)")
