#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证几个关键卦的编码"""
import json

data_path = 'zhouyi/data/hexagrams.json'
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

check_ids = [3, 9, 15, 16, 21, 31, 41, 51, 52, 62]
TRIGRAM_BIN = {
    '乾': '111', '兑': '110', '离': '101', '震': '100',
    '巽': '011', '坎': '010', '艮': '001', '坤': '000'
}

print("验证关键卦的编码：")
print("=" * 60)
for hex_id in check_ids:
    h = [x for x in data['hexagrams'] if x['id'] == hex_id][0]
    expected = TRIGRAM_BIN[h['upper_trigram']] + TRIGRAM_BIN[h['lower_trigram']]
    status = "OK" if h['binary'] == expected else "ERR"
    print(f"{status} ID={hex_id:2d} {h['name']:4s} binary={h['binary']} upper={h['upper_trigram']} lower={h['lower_trigram']}")
