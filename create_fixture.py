import json

with open('dump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

specialties = [item for item in data if item['model'] == 'data.specialty']

with open('fixture.json', 'w', encoding='utf-8') as f:
    json.dump(specialties, f, ensure_ascii=False, indent=2)

print("Фикстура создана: fixture.json")