#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易占卜系统 - 自动化测试脚本
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.calculator import CoinMethod, ShicaoMethod, NumberMethod, TimeMethod
from core.hexagram import HexagramCalculator

def test_all():
    print("=" * 60)
    print("        周易占卜系统 v0.1.0 - 功能测试")
    print("=" * 60)
    
    # 测试 1: 铜钱起卦
    print("\n【测试 1】铜钱起卦")
    coin = CoinMethod()
    lines = coin.generate()
    print(f"  结果：{lines}")
    
    calc = HexagramCalculator(lines)
    print(calc.display_all())
    
    # 测试 2: 蓍草起卦
    print("\n【测试 2】蓍草起卦")
    shicao = ShicaoMethod()
    lines = shicao.generate()
    print(f"  结果：{lines}")
    
    calc = HexagramCalculator(lines)
    print(calc.display_all())
    
    # 测试 3: 数字起卦
    print("\n【测试 3】数字起卦 (12345)")
    num = NumberMethod()
    lines = num.generate(12345)
    info = num.get_trigram_info(12345)
    print(f"  六爻：{lines}")
    print(f"  上卦：{info['upper_name']}")
    print(f"  下卦：{info['lower_name']}")
    print(f"  动爻：第{info['moving']}爻")
    
    # 测试 4: 时间起卦
    print("\n【测试 4】时间起卦")
    time_method = TimeMethod()
    lines = time_method.generate()
    info = time_method.get_time_info()
    print(f"  六爻：{lines}")
    print(f"  时间：{info['time']}")
    print(f"  上卦：{info['upper_name']}")
    print(f"  下卦：{info['lower_name']}")
    print(f"  动爻：第{info['moving']}爻")
    
    print("\n" + "=" * 60)
    print("[OK] 全部测试完成！")
    print("=" * 60)

if __name__ == '__main__':
    test_all()
