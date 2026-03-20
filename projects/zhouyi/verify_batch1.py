#!/usr/bin/env python3
"""
验证第一批 17 卦数据正确性
v1.0-beta 交付验证脚本
"""
import sys
sys.path.insert(0, 'zhouyi')
from core.hexagram import Hexagram
import json

# 第一批 17 卦
BATCH_1_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# 加载数据
with open('zhouyi/data/hexagrams.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

hexagrams = {h['id']: h for h in data['hexagrams']}

print("=" * 60)
print("第一批 17 卦验证 (v1.0-beta)")
print("=" * 60)

errors = []
warnings = []

for hex_id in BATCH_1_IDS:
    h = hexagrams.get(hex_id)
    if not h:
        errors.append(f"卦 {hex_id}: 数据缺失")
        continue
    
    name = h['name']
    binary = h['binary']
    upper = h['upper_trigram']
    lower = h['lower_trigram']
    lines = h.get('lines', [])
    judgment = h.get('judgment', '')
    image = h.get('image', '')
    
    # 验证 binary
    TRIGRAM_BIN = {
        '乾': '111', '兑': '110', '离': '101', '震': '100',
        '巽': '011', '坎': '010', '艮': '001', '坤': '000'
    }
    expected_binary = TRIGRAM_BIN[upper] + TRIGRAM_BIN[lower]
    
    if binary != expected_binary:
        errors.append(f"卦 {hex_id} {name}: binary 错误 (当前={binary}, 应为={expected_binary})")
    
    # 验证爻数
    if len(lines) != 6:
        errors.append(f"卦 {hex_id} {name}: 爻数错误 ({len(lines)}爻)")
    
    # 验证卦辞
    if not judgment:
        warnings.append(f"卦 {hex_id} {name}: 缺少卦辞")
    
    # 验证象传
    if not image:
        warnings.append(f"卦 {hex_id} {name}: 缺少象传")
    
    # 验证卦名映射
    full_binary = binary
    lines_test = []
    for i in range(6):
        bit = full_binary[5 - i]
        lines_test.append(7 if bit == '1' else 8)
    
    hexagram = Hexagram(lines_test)
    actual_id = hexagram.get_hexagram_number()
    if actual_id != hex_id:
        errors.append(f"卦 {hex_id} {name}: 卦名映射错误 (期望={hex_id}, 实际={actual_id})")
    
    print(f"  [{hex_id:2d}] {name:6s} binary={binary} upper={upper} lower={lower} [OK]")

print()
print("-" * 60)
print(f"验证结果：{17 - len(errors)}/17 通过")

if errors:
    print("\n[ERROR] Errors found:")
    for err in errors:
        print(f"  {err}")
    print("\n[RESULT] Batch 1 verification FAILED, needs fix")
else:
    print("\n[PASS] All 17 hexagrams verified!")
    if warnings:
        print(f"\n[WARN] {len(warnings)} warnings:")
        for w in warnings:
            print(f"  {w}")
    print("\n[RESULT] v1.0-beta READY FOR DELIVERY")

print("=" * 60)
