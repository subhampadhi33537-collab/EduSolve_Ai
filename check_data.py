import json

with open('data/training_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total records: {len(data)}")
print("\nLast 5 questions:")
for i, d in enumerate(data[-5:]):
    q = d.get('question', 'N/A')[:50]
    ts = d.get('timestamp', 'N/A')
    print(f"{i+1}. {q}... - {ts}")

# Check for duplicate timestamps
timestamps = [d.get('timestamp') for d in data]
duplicates = [t for t in timestamps if timestamps.count(t) > 1]
if duplicates:
    print(f"\n⚠️  Found {len(set(duplicates))} duplicate timestamps!")
    for dup in set(duplicates):
        print(f"   - {dup}")
