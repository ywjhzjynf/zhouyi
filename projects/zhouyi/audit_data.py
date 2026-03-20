#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易数据审核脚本
门下省专用 - 验证 hexagrams.json 数据准确性
"""

import json
from pathlib import Path

# 加载数据
data_path = Path(__file__).parent / 'zhouyi' / 'data' / 'hexagrams.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

hexagrams = data['hexagrams']
trigrams = data['trigrams']

# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Menxia Sheng Audit Report (门下省审核)")
print("=" * 60)
print(f"审核时间：2026-03-20")
print(f"数据文件：{data_path}")
print(f"总卦数：{len(hexagrams)}")
print()

# 八卦二进制标准（从下往上）
TRIGRAM_BIN = {
    '乾': '111', '兑': '110', '离': '101', '震': '100',
    '巽': '011', '坎': '010', '艮': '001', '坤': '000'
}

# 抽检 30% (20 卦)
sample_ids = [1, 2, 3, 11, 12, 21, 22, 31, 32, 41, 42, 51, 52, 61, 62, 10, 20, 30, 40, 50]

errors = []
warnings = []

print("[Sample Audit: 20 hexagrams (30%)]")
print("-" * 60)

for hex_id in sample_ids:
    hexagram = next((h for h in hexagrams if h['id'] == hex_id), None)
    if not hexagram:
        errors.append(f"卦 ID {hex_id}: 数据缺失")
        continue
    
    name = hexagram['name']
    upper = hexagram['upper_trigram']
    lower = hexagram['lower_trigram']
    binary = hexagram['binary']
    
    # 验证二进制计算
    expected_binary = TRIGRAM_BIN[upper] + TRIGRAM_BIN[lower]
    
    if binary != expected_binary:
        errors.append(f"卦 ID {hex_id} ({name}): binary 错误")
        errors.append(f"  当前：{binary}")
        errors.append(f"  应为：{expected_binary} (上{upper}={TRIGRAM_BIN[upper]}, 下{lower}={TRIGRAM_BIN[lower]})")
    
    # 验证爻数
    lines = hexagram.get('lines', [])
    if len(lines) != 6:
        errors.append(f"卦 ID {hex_id} ({name}): 爻数错误，应为 6 爻，实际{len(lines)}爻")
    
    # 验证爻位
    for i, line in enumerate(lines):
        if line['position'] != i + 1:
            errors.append(f"卦 ID {hex_id} ({name}): 第{i+1}爻位置标注错误")
        
        # 验证阴阳与 binary 一致
        expected_yang = binary[i] == '1' if i < len(binary) else None
        actual_yang = line['type'] == 'yang'
        # 注意：binary 是从下往上，lines 也是从下往上
    
    # 验证来源标注
    if 'source' not in hexagram and hex_id > 2:
        warnings.append(f"卦 ID {hex_id} ({name}): 缺少 source 字段")

print(f"Sample size: {len(sample_ids)} hexagrams (30%)")
print(f"Errors found: {len(errors)}")
print(f"Warnings found: {len(warnings)}")
print()

if errors:
    print("[ERRORS]")
    for err in errors[:20]:
        print(f"  {err}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more errors")
    print()

if warnings:
    print("[WARNINGS]")
    for warn in warnings[:10]:
        print(f"  {warn}")
    print()

# Full binary validation
print("[Full Binary Validation: 64 hexagrams]")
print("-" * 60)
binary_errors = []
for hexagram in hexagrams:
    upper = hexagram['upper_trigram']
    lower = hexagram['lower_trigram']
    binary = hexagram['binary']
    expected = TRIGRAM_BIN[upper] + TRIGRAM_BIN[lower]
    
    if binary != expected:
        binary_errors.append({
            'id': hexagram['id'],
            'name': hexagram['name'],
            'current': binary,
            'expected': expected,
            'upper': upper,
            'lower': lower
        })

if binary_errors:
    print(f"[ERROR] Found {len(binary_errors)} hexagrams with binary errors:")
    for err in binary_errors:
        print(f"  Hexagram {err['id']:2d} {err['name']}: current={err['current']}, expected={err['expected']} (upper={err['upper']}, lower={err['lower']})")
else:
    print("[OK] All 64 hexagrams binary correct")

print()

# Verify sequence
print("[Verify Hexagram Sequence]")
print("-" * 60)
ids = [h['id'] for h in hexagrams]
expected_ids = list(range(1, 65))
if ids == expected_ids:
    print("✅ 卦序连续正确 (1-64)")
else:
    missing = set(expected_ids) - set(ids)
    extra = set(ids) - set(expected_ids)
    print(f"❌ 卦序错误：缺失{missing}, 多余{extra}")

print()
print("=" * 60)
print("AUDIT CONCLUSION:", end=" ")
if errors or binary_errors:
    print("FAIL - Data has errors, return to Hubu for correction")
    print(f"Total errors: {len(errors) + len(binary_errors)}")
else:
    print("PASS - Data audit approved")
print("=" * 60)
