#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证优化后的数据"""
import json
import os

# 加载优化后的文件
with open('mobile_optimized/hexagrams.min.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

hexagrams = data.get('hexagrams', [])

result = []
result.append(f'Hexagram count: {len(hexagrams)}')
result.append(f'First hexagram: ID={hexagrams[0].get("i")}, Name={hexagrams[0].get("n")}')
result.append(f'Last hexagram: ID={hexagrams[-1].get("i")}, Name={hexagrams[-1].get("n")}')

qian_lines = hexagrams[0].get('ln', [])
result.append(f'Qian lines count: {len(qian_lines)}')
result.append(f'Qian line 1: {qian_lines[0].get("t")}')

# 验证所有卦 ID 连续性
ids = [h.get('i') for h in hexagrams]
expected = list(range(1, 65))
id_check = 'PASS' if ids == expected else 'FAIL'
result.append(f'ID continuity check: {id_check}')

# 写入文件
with open('mobile_optimized/verification_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))

print('Verification complete. Result saved to verification_result.txt')
