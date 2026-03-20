#!/usr/bin/env python3
import json

with open('zhouyi/data/hexagrams.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("HEXAGRAM_MAP = {")
for h in data['hexagrams']:
    print(f"    ('{h['upper_trigram']}', '{h['lower_trigram']}'): {h['id']},  # {h['name']}")
print("}")
