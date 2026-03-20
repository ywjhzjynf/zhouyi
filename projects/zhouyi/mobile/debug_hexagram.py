# -*- coding: utf-8 -*-
from divination_api import Hexagram, TRIGRAM_BINARY

# 测试几个案例
test_cases = [
    [9, 9, 9, 9, 9, 9],  # 全阳
    [6, 6, 6, 6, 6, 6],  # 全阴
    [7, 7, 7, 6, 6, 6],  # 下三阳，上三阴
    [8, 8, 8, 9, 9, 9],  # 下三阴，上三阳
]

print("TRIGRAM_BINARY:", TRIGRAM_BINARY)
print()

for lines in test_cases:
    h = Hexagram(lines)
    binary = h.to_binary()
    upper_bin = binary[:3]
    lower_bin = binary[3:]
    upper, lower = h.get_trigrams()
    
    print(f"lines: {lines}")
    print(f"  binary: {binary} (upper={upper_bin}, lower={lower_bin})")
    print(f"  trigrams: upper={upper}, lower={lower}")
    print(f"  name: {h.get_name()}, num: {h.get_hexagram_number()}")
    print()
