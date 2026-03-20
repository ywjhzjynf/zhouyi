#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'zhouyi'))
from core.calculator import NumberMethod
from core.hexagram import HexagramCalculator

print('=' * 50)
print('🔮 周易占卜 - 闫文杰 97 年出生')
print('=' * 50)
print()

num = NumberMethod()
result = num.generate(97)
print(f'【数字起卦】97')
print(f'上卦：{result["upper_name"]} ({result["upper"]})')
print(f'下卦：{result["lower_name"]} ({result["lower"]})')
print(f'动爻：第{result["moving"]}爻')
print()

trigram_bin = {'乾':'111', '兑':'110', '离':'101', '震':'100', '巽':'011', '坎':'010', '艮':'001', '坤':'000'}
upper_bin = trigram_bin[result['upper_name']]
lower_bin = trigram_bin[result['lower_name']]
binary = upper_bin + lower_bin

lines = []
for i, bit in enumerate(reversed(binary)):
    lines.append(7 if bit == '1' else 8)

moving_idx = result['moving'] - 1
lines[moving_idx] = 9 if lines[moving_idx] == 7 else 6

print('【六爻】（从下往上）')
for i, line in enumerate(lines):
    meaning = {9:'老阳（变爻）', 6:'老阴（变爻）', 7:'少阳（不变）', 8:'少阴（不变）'}[line]
    print(f'  第{i+1}爻：{line} - {meaning}')
print()

calc = HexagramCalculator(lines)
print(calc.display_all())

data_path = Path('data/hexagrams.json')
if data_path.exists():
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('\n【卦辞解析】')
    for h in data['hexagrams']:
        if h['id'] == 1:
            print(f"\n{h['full_name']}")
            print(f"卦辞：{h['judgment']}")
            print(f"象传：{h['image']}")
            print("\n爻辞：")
            for ld in h['lines']:
                print(f"  第{ld['position']}爻：{ld['text']}")
            break
