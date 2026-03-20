#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易移动端演示 - 测试脚本
"""
import sys
import io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'zhouyi'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("        周易占卜系统 v2.0.0 - 移动端演示")
print("=" * 60)
print()

# 测试导入
try:
    from core.calculator import CoinMethod, ShicaoMethod, NumberMethod, TimeMethod
    from core.hexagram import HexagramCalculator
    print("✅ 核心算法模块 - 加载成功")
except Exception as e:
    print(f"❌ 核心算法模块 - 加载失败：{e}")

try:
    import json
    from pathlib import Path
    data_path = Path('zhouyi/data/hexagrams.json')
    if data_path.exists():
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 六十四卦数据 - 加载成功 ({len(data.get('hexagrams', []))}卦)")
    else:
        print("❌ 六十四卦数据 - 文件不存在")
except Exception as e:
    print(f"❌ 六十四卦数据 - 加载失败：{e}")

try:
    import flet as ft
    print(f"✅ Flet 框架 - 加载成功 (v{ft.__version__})")
except Exception as e:
    print(f"❌ Flet 框架 - 加载失败：{e}")

print()
print("=" * 60)
print("【功能演示】")
print("=" * 60)
print()

# 演示铜钱起卦
print("🪙 铜钱起卦演示：")
coin = CoinMethod()
lines = coin.generate()
for i, line in enumerate(lines):
    meaning = "老阳★" if line == 9 else "老阴★" if line == 6 else "少阳" if line == 7 else "少阴"
    print(f"  第{i+1}爻：{line} - {meaning}")

print()
print("=" * 60)
print("✅ 移动端核心功能验证完成！")
print("=" * 60)
print()
print("📱 运行方式：")
print("  Web 版：python zhouyi/mobile/main.py")
print("  或访问：http://localhost:8550")
print()
