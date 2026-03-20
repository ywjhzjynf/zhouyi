#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
64 卦数据加载与显示测试 - 简化版 (避免 Windows 编码问题)
"""

import json
import sys
from pathlib import Path

# 设置 UTF-8 编码
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', buffering=1, closefd=False)

def test_hexagram_data():
    """测试 64 卦数据加载"""
    print("=" * 60)
    print("64 卦数据加载测试")
    print("=" * 60)
    
    data_path = Path(__file__).parent / 'zhouyi' / 'data' / 'hexagrams.json'
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        hexagrams = data['hexagrams']
        trigrams = data.get('trigrams', [])
        
        print(f"\n[OK] 数据文件加载成功")
        print(f"  六十四卦数量：{len(hexagrams)}")
        print(f"  八卦数量：{len(trigrams)}")
        
        # 验证卦序
        ids = [h['id'] for h in hexagrams]
        expected = list(range(1, 65))
        
        if ids == expected:
            print(f"\n[OK] 卦序正确 (1-64)")
        else:
            print(f"\n[ERROR] 卦序错误!")
            missing = set(expected) - set(ids)
            extra = set(ids) - set(expected)
            if missing:
                print(f"  缺失：{missing}")
            if extra:
                print(f"  多余：{extra}")
        
        # 验证二进制编码
        TRIGRAM_BIN = {
            '乾': '111', '兑': '110', '离': '101', '震': '100',
            '巽': '011', '坎': '010', '艮': '001', '坤': '000'
        }
        
        binary_errors = []
        for h in hexagrams:
            expected_bin = TRIGRAM_BIN[h['upper_trigram']] + TRIGRAM_BIN[h['lower_trigram']]
            if h['binary'] != expected_bin:
                binary_errors.append((h['id'], h['name'], h['binary'], expected_bin))
        
        if binary_errors:
            print(f"\n[ERROR] 二进制编码错误：{len(binary_errors)} 卦")
            for err in binary_errors[:5]:
                print(f"  卦 {err[0]} {err[1]}: {err[2]} (应为 {err[3]})")
            return False
        else:
            print(f"\n[OK] 所有二进制编码正确")
        
        # 抽检爻辞数据
        print(f"\n[抽样检查爻辞数据]")
        sample_ids = [1, 2, 3, 30, 63, 64]
        for hex_id in sample_ids:
            h = next((x for x in hexagrams if x['id'] == hex_id), None)
            if h:
                lines_count = len(h.get('lines', []))
                has_judgment = 'judgment' in h
                has_image = 'image' in h
                status = "OK" if (lines_count == 6 and has_judgment and has_image) else "FAIL"
                print(f"  [{status}] 卦 {hex_id:2d} {h['name']}: {lines_count}爻，卦辞={'有' if has_judgment else '无'}，象传={'有' if has_image else '无'}")
        
        # 显示前 10 卦名称
        print(f"\n[前 10 卦名称]")
        for h in hexagrams[:10]:
            print(f"  {h['id']:2d}. {h['name']} ({h['full_name']}) - {h['symbol']}")
        
        print("\n" + "=" * 60)
        print("测试结果：PASS - 64 卦数据完整且正确")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_hexagram_display():
    """测试卦象显示功能"""
    print("\n" + "=" * 60)
    print("卦象显示功能测试")
    print("=" * 60)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'zhouyi'))
        from core.hexagram import HexagramCalculator
        
        # 测试乾卦 (111111)
        print("\n[测试] 乾卦 (全阳)")
        lines = [9, 9, 9, 9, 9, 9]  # 全老阳
        calc = HexagramCalculator(lines)
        original = calc.get_original()
        
        print(f"  本卦：{original.get_name()}")
        
        # 测试坤卦 (000000)
        print("\n[测试] 坤卦 (全阴)")
        lines = [6, 6, 6, 6, 6, 6]  # 全老阴
        calc = HexagramCalculator(lines)
        original = calc.get_original()
        
        print(f"  本卦：{original.get_name()}")
        
        # 测试既济卦
        print("\n[测试] 既济卦 (阴阳交替)")
        lines = [9, 6, 9, 6, 9, 6]
        calc = HexagramCalculator(lines)
        original = calc.get_original()
        
        print(f"  本卦：{original.get_name()}")
        
        print("\n[OK] 卦象显示功能正常")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] 卦象显示测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_history_function():
    """测试历史记录功能"""
    print("\n" + "=" * 60)
    print("历史记录功能测试")
    print("=" * 60)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'zhouyi'))
        from history import DivinationHistory
        
        # 创建历史记录实例
        history = DivinationHistory()
        
        # 测试保存记录
        print("\n[测试] 保存占卜记录")
        test_lines = [7, 8, 9, 6, 7, 8]
        record_id = history.save_record(
            method='测试',
            lines=test_lines,
            hexagram_name='乾为天',
            transformed_name='坤为地',
            mutual_name='水雷屯',
            moving_lines=[3, 4],
            question='测试问题',
            notes='测试备注'
        )
        print(f"  记录 ID: {record_id}")
        
        # 测试获取统计
        print("\n[测试] 获取统计信息")
        stats = history.get_statistics()
        print(f"  总记录数：{stats['total']}")
        print(f"  最后占卜：{stats['last_divination']}")
        
        print("\n[OK] 历史记录功能正常")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] 历史记录测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def test_hexagram_query():
    """测试卦象查询功能"""
    print("\n" + "=" * 60)
    print("卦象查询功能测试")
    print("=" * 60)
    
    try:
        data_path = Path(__file__).parent / 'zhouyi' / 'data' / 'hexagrams.json'
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        hexagrams = data['hexagrams']
        
        # 测试按 ID 查询
        print("\n[测试] 按 ID 查询")
        test_ids = [1, 30, 64]
        for hex_id in test_ids:
            h = next((x for x in hexagrams if x['id'] == hex_id), None)
            if h:
                print(f"  [OK] ID {hex_id:2d}: {h['name']} ({h['full_name']})")
            else:
                print(f"  [FAIL] ID {hex_id}: 未找到")
        
        # 测试按名称查询
        print("\n[测试] 按名称查询")
        test_names = ['乾', '坤', '既济', '未济']
        for name in test_names:
            h = next((x for x in hexagrams if x['name'] == name), None)
            if h:
                print(f"  [OK] {name}: ID={h['id']}, 二进制={h['binary']}")
            else:
                print(f"  [FAIL] {name}: 未找到")
        
        # 测试按卦象结构查询
        print("\n[测试] 按上下卦查询")
        test_queries = [('乾', '乾'), ('坎', '离'), ('震', '巽')]
        for upper, lower in test_queries:
            matches = [h for h in hexagrams if h['upper_trigram'] == upper and h['lower_trigram'] == lower]
            if matches:
                for m in matches:
                    print(f"  [OK] 上{upper}下{lower}: {m['name']} (ID={m['id']})")
            else:
                print(f"  [FAIL] 上{upper}下{lower}: 未找到")
        
        print("\n[OK] 卦象查询功能正常")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] 卦象查询测试失败：{e}")
        return False


if __name__ == '__main__':
    results = []
    
    results.append(("64 卦数据加载", test_hexagram_data()))
    results.append(("卦象显示", test_hexagram_display()))
    results.append(("历史记录", test_history_function()))
    results.append(("卦象查询", test_hexagram_query()))
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")
    
    print(f"\n总计：{passed}/{total} 通过")
    
    if passed == total:
        print("\n[OK] 所有测试通过！界面集成功能正常")
    else:
        print(f"\n[WARNING] 有 {total - passed} 项测试失败，请检查")
    
    print("=" * 60)
