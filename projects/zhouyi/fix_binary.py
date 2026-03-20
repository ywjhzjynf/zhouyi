#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正 hexagrams.json 中的 binary 编码错误
礼部专用 - 协助户部修正数据
"""

import json
from pathlib import Path

# 八卦二进制标准（从下往上）
TRIGRAM_BIN = {
    '乾': '111', '兑': '110', '离': '101', '震': '100',
    '巽': '011', '坎': '010', '艮': '001', '坤': '000'
}

# 加载数据
data_path = Path(__file__).parent / 'zhouyi' / 'data' / 'hexagrams.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

hexagrams = data['hexagrams']
source_text = "《周易正义》（唐·孔颖达），《周易折中》（清·康熙）校勘"

# 修正 binary 和 source
fixed_count = 0
for hexagram in hexagrams:
    upper = hexagram['upper_trigram']
    lower = hexagram['lower_trigram']
    current_binary = hexagram['binary']
    
    # 计算正确的 binary
    expected_binary = TRIGRAM_BIN[upper] + TRIGRAM_BIN[lower]
    
    # 修正 binary
    if current_binary != expected_binary:
        print(f"修正卦 {hexagram['id']:2d} {hexagram['name']}: {current_binary} -> {expected_binary}")
        hexagram['binary'] = expected_binary
        fixed_count += 1
    
    # 补充 source 字段
    if 'source' not in hexagram:
        hexagram['source'] = source_text
        print(f"  补充 source 字段")

# 保存修正后的数据
backup_path = data_path.with_suffix('.json.bak')
if backup_path.exists():
    backup_path.unlink()
    print(f"已删除旧备份：{backup_path}")
data_path.rename(backup_path)
print(f"\n已备份原文件：{backup_path}")

with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n修正完成！")
print(f"修正 binary 错误：{fixed_count} 卦")
print(f"文件已保存：{data_path}")
