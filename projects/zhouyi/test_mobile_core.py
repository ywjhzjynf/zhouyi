#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试核心功能"""

from zhouyi.core.calculator import DivinationCalculator
from zhouyi.data import DataLoader

calc = DivinationCalculator()
loader = DataLoader()

print("=" * 50)
print("核心功能测试")
print("=" * 50)

# 测试铜钱起卦
print("\n【铜钱起卦】")
result = calc.divinate('coin')
hex_id = result['hexagram_id']
print(f"卦象 ID: {hex_id}")

hex_data = loader.get_hexagram(hex_id)
if hex_data:
    print(f"卦名：{hex_data.get('name')}")
    print(f"卦辞：{hex_data.get('judgment', 'N/A')[:50]}")
else:
    print("未找到卦象数据")

# 测试时间起卦
print("\n【时间起卦】")
result = calc.divinate('time')
hex_id = result['hexagram_id']
print(f"卦象 ID: {hex_id}")

hex_data = loader.get_hexagram(hex_id)
if hex_data:
    print(f"卦名：{hex_data.get('name')}")
else:
    print("未找到卦象数据")

# 测试数字起卦
print("\n【数字起卦】")
result = calc.divinate('number', number=20260320)
hex_id = result['hexagram_id']
print(f"卦象 ID: {hex_id}")

hex_data = loader.get_hexagram(hex_id)
if hex_data:
    print(f"卦名：{hex_data.get('name')}")
else:
    print("未找到卦象数据")

print("\n" + "=" * 50)
print("测试完成!")
