import json

# Load data
with open('data/training_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Before cleanup: {len(data)} records")

# Remove the duplicate (keep only first occurrence of each question+timestamp pair)
seen = set()
cleaned_data = []
for record in data:
    key = (record.get('question', ''), record.get('timestamp', '')[:19])  # Use timestamp without milliseconds
    if key not in seen:
        seen.add(key)
        cleaned_data.append(record)
    else:
        print(f"Removed duplicate: {record.get('question', '')[:50]}... - {record.get('timestamp', '')}")

print(f"After cleanup: {len(cleaned_data)} records")

# Save cleaned data
with open('data/training_data.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

print("✅ Data cleaned and saved!")
