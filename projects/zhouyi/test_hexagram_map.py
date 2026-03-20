#!/usr/bin/env python3
"""
测试 hexagram.py 的卦名映射是否正确
"""
import sys
sys.path.insert(0, 'zhouyi')
from core.hexagram import Hexagram, HexagramCalculator
import json

# 加载正确的卦象数据
with open('zhouyi/data/hexagrams.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("Testing hexagram number mapping")
print("=" * 60)

errors = []
correct = 0

for h in data['hexagrams']:
    upper = h['upper_trigram']
    lower = h['lower_trigram']
    expected_id = h['id']
    expected_name = h['name']
    binary = h['binary']  # e.g., '010100' for 屯
    
    # binary[0:3] = upper trigram (TOP), binary[3:6] = lower trigram (BOTTOM)
    # to_binary() builds: binary[0]=top, binary[5]=bottom
    # lines[0]=bottom, lines[5]=top
    # So: lines[i] corresponds to binary[5-i]
    
    lines = []
    for i in range(6):
        bit = binary[5 - i]  # Reverse: lines[0] gets binary[5], lines[5] gets binary[0]
        if bit == '1':
            lines.append(7)  # 少阳
        else:
            lines.append(8)  # 少阴
    
    # Test
    hexagram = Hexagram(lines)
    actual_id = hexagram.get_hexagram_number()
    actual_name = hexagram.get_name()
    
    if actual_id != expected_id:
        errors.append(f"Hex {expected_id} {expected_name}: expected={expected_id}, got={actual_id}, name={actual_name}, upper={upper}, lower={lower}, binary={binary}, lines={lines}")
    else:
        correct += 1

print(f"\nResult: {correct}/64 correct, {len(errors)}/64 errors")

if errors:
    print("\nErrors:")
    for err in errors[:10]:
        print(f"  {err}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more")
    print("\nFAIL")
else:
    print("\nPASS - All hexagram mappings correct!")
    
print("=" * 60)
