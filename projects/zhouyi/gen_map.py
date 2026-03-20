#!/usr/bin/env python3
import json

with open('zhouyi/data/hexagrams.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('hexagram_map.txt', 'w', encoding='utf-8') as out:
    for h in data['hexagrams']:
        out.write(f"{h['id']:2d} {h['name']:6s} 上={h['upper_trigram']:2s} 下={h['lower_trigram']:2s}\n")

print("Generated hexagram_map.txt")
