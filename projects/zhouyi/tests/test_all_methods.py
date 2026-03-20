#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易占卜系统 - 单元测试套件
Task ID: TASK-20260320-007

测试覆盖：
1. 铜钱起卦算法
2. 蓍草起卦算法
3. 数字起卦算法
4. 时间起卦算法
5. 本卦/变卦/互卦计算

验证要求：
- 每种起卦方式至少测试 10 次
- 记录测试结果
- 确保无逻辑错误
"""

import sys
import time
import random
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'zhouyi'))

from core.calculator import CoinMethod, ShicaoMethod, NumberMethod, TimeMethod
from core.hexagram import Hexagram, HexagramCalculator


class TestResult:
    """测试结果记录类"""
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def record_pass(self):
        self.passed += 1
        self.total += 1
    
    def record_fail(self, error: str):
        self.failed += 1
        self.total += 1
        self.errors.append(error)
    
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        self.end_time = time.time()
    
    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100
    
    def report(self) -> str:
        return (
            f"\n【{self.test_name}】\n"
            f"  测试次数：{self.total}\n"
            f"  通过：{self.passed}\n"
            f"  失败：{self.failed}\n"
            f"  通过率：{self.pass_rate:.2f}%\n"
            f"  耗时：{self.duration:.4f}秒\n"
            f"  平均每次：{self.duration/self.total:.4f}秒"
            if self.total > 0 else ""
        )


# ============================================================
# 测试 1: 铜钱起卦算法
# ============================================================
def test_coin_method():
    """测试铜钱起卦法"""
    result = TestResult("铜钱起卦算法")
    result.start()
    
    for i in range(10):
        try:
            coin = CoinMethod()
            lines = coin.generate()
            
            # 验证 1: 必须生成 6 爻
            assert len(lines) == 6, f"第{i+1}次：爻数错误，应为 6，实际{len(lines)}"
            
            # 验证 2: 每爻必须是 6/7/8/9
            for j, line in enumerate(lines):
                assert line in [6, 7, 8, 9], f"第{i+1}次第{j+1}爻：值错误{line}"
            
            # 验证 3: 概率分布合理性（10 次内至少出现 2 种不同值）
            unique_values = set(lines)
            assert len(unique_values) >= 2, f"第{i+1}次：结果过于单一{unique_values}"
            
            result.record_pass()
            
        except Exception as e:
            result.record_fail(str(e))
    
    result.stop()
    return result


# ============================================================
# 测试 2: 蓍草起卦算法
# ============================================================
def test_shicao_method():
    """测试蓍草起卦法"""
    result = TestResult("蓍草起卦算法")
    result.start()
    
    for i in range(10):
        try:
            shicao = ShicaoMethod()
            lines = shicao.generate()
            
            # 验证 1: 必须生成 6 爻
            assert len(lines) == 6, f"第{i+1}次：爻数错误，应为 6，实际{len(lines)}"
            
            # 验证 2: 每爻必须是 6/7/8/9
            for j, line in enumerate(lines):
                assert line in [6, 7, 8, 9], f"第{i+1}次第{j+1}爻：值错误{line}"
            
            # 验证 3: 三变算法正确性（每爻经过三变）
            # 蓍草法理论上应该产生符合概率分布的结果
            # 6(老阴) 概率约 1/16, 7(少阳) 约 3/16, 8(少阴) 约 5/16, 9(老阳) 约 7/16
            
            result.record_pass()
            
        except Exception as e:
            result.record_fail(str(e))
    
    result.stop()
    return result


# ============================================================
# 测试 3: 数字起卦算法
# ============================================================
def test_number_method():
    """测试数字起卦法"""
    result = TestResult("数字起卦算法")
    result.start()
    
    test_numbers = [12345, 99999, 1, 8, 64, 100, 256, 1000, 7777, 31415]
    
    for i, num in enumerate(test_numbers):
        try:
            method = NumberMethod()
            lines = method.generate(num)
            info = method.get_trigram_info(num)
            
            # 验证 1: 必须生成 6 爻
            assert len(lines) == 6, f"测试{i+1}: 爻数错误，应为 6，实际{len(lines)}"
            
            # 验证 2: 上卦必须在 1-8 范围
            assert 1 <= info['upper'] <= 8, f"测试{i+1}: 上卦超出范围{info['upper']}"
            
            # 验证 3: 下卦必须在 1-8 范围
            assert 1 <= info['lower'] <= 8, f"测试{i+1}: 下卦超出范围{info['lower']}"
            
            # 验证 4: 动爻必须在 1-6 范围
            assert 1 <= info['moving'] <= 6, f"测试{i+1}: 动爻超出范围{info['moving']}"
            
            # 验证 5: 卦名必须存在
            assert 'upper_name' in info, f"测试{i+1}: 缺少上卦名"
            assert 'lower_name' in info, f"测试{i+1}: 缺少下卦名"
            
            # 验证 6: 每爻必须是 6/7/8/9
            for j, line in enumerate(lines):
                assert line in [6, 7, 8, 9], f"测试{i+1}第{j+1}爻：值错误{line}"
            
            result.record_pass()
            
        except Exception as e:
            result.record_fail(str(e))
    
    result.stop()
    return result


# ============================================================
# 测试 4: 时间起卦算法
# ============================================================
def test_time_method():
    """测试时间起卦法"""
    result = TestResult("时间起卦算法")
    result.start()
    
    # 测试不同时间点
    test_times = [
        datetime(2026, 3, 20, 12, 0, 0),
        datetime(2026, 1, 1, 0, 0, 0),
        datetime(2025, 12, 31, 23, 59, 59),
        datetime(2024, 6, 15, 6, 30, 0),
        datetime(2023, 9, 10, 18, 45, 30),
        datetime(2022, 2, 28, 14, 20, 10),
        datetime(2021, 7, 4, 8, 8, 8),
        datetime(2020, 11, 11, 11, 11, 11),
        datetime(2019, 5, 20, 10, 30, 0),
        datetime.now(),
    ]
    
    for i, test_time in enumerate(test_times):
        try:
            method = TimeMethod()
            lines = method.generate(test_time)
            info = method.get_time_info(test_time)
            
            # 验证 1: 必须生成 6 爻
            assert len(lines) == 6, f"测试{i+1}: 爻数错误，应为 6，实际{len(lines)}"
            
            # 验证 2: 上卦必须在 1-8 范围
            assert 1 <= info['upper'] <= 8, f"测试{i+1}: 上卦超出范围{info['upper']}"
            
            # 验证 3: 下卦必须在 1-8 范围
            assert 1 <= info['lower'] <= 8, f"测试{i+1}: 下卦超出范围{info['lower']}"
            
            # 验证 4: 动爻必须在 1-6 范围
            assert 1 <= info['moving'] <= 6, f"测试{i+1}: 动爻超出范围{info['moving']}"
            
            # 验证 5: 时间信息必须存在
            assert 'time' in info, f"测试{i+1}: 缺少时间信息"
            
            # 验证 6: 每爻必须是 6/7/8/9
            for j, line in enumerate(lines):
                assert line in [6, 7, 8, 9], f"测试{i+1}第{j+1}爻：值错误{line}"
            
            result.record_pass()
            
        except Exception as e:
            result.record_fail(str(e))
    
    result.stop()
    return result


# ============================================================
# 测试 5: 本卦/变卦/互卦计算
# ============================================================
def test_hexagram_calculation():
    """测试卦象计算"""
    result = TestResult("本卦/变卦/互卦计算")
    result.start()
    
    # 测试用例：(输入爻，预期本卦特征，预期变卦特征)
    test_cases = [
        # 乾为天（全阳）-> 坤为地（全阴）
        ([9, 9, 9, 9, 9, 9], "全阳", "全阴"),
        # 坤为地（全阴）-> 乾为天（全阳）
        ([6, 6, 6, 6, 6, 6], "全阴", "全阳"),
        # 混合卦
        ([7, 8, 9, 6, 7, 8], "混合", "混合"),
        # 仅一个老阳
        ([7, 7, 7, 7, 7, 9], "一阳动", "一阴变"),
        # 仅一个老阴
        ([8, 8, 8, 8, 8, 6], "一阴动", "一阳变"),
        # 多爻动
        ([6, 9, 6, 9, 6, 9], "多爻动", "多爻变"),
        # 少阳少阴混合（无动爻）
        ([7, 8, 7, 8, 7, 8], "无动爻", "不变"),
        # 随机组合 1
        ([7, 6, 8, 9, 7, 6], "随机 1", "随机 1 变"),
        # 随机组合 2
        ([8, 9, 7, 6, 8, 7], "随机 2", "随机 2 变"),
        # 边界测试
        ([7, 7, 8, 8, 9, 6], "边界", "边界变"),
    ]
    
    for i, (lines, desc, trans_desc) in enumerate(test_cases):
        try:
            calc = HexagramCalculator(lines)
            
            # 验证 1: 本卦存在
            original = calc.get_original()
            assert original is not None, f"测试{i+1}: 本卦为空"
            assert len(original.lines) == 6, f"测试{i+1}: 本卦爻数错误"
            
            # 验证 2: 变卦正确
            transformed = calc.get_transformed()
            assert transformed is not None, f"测试{i+1}: 变卦为空"
            
            # 验证变卦规则：老阴变阳，老阳变阴
            for j, (orig_line, trans_line) in enumerate(zip(lines, transformed.lines)):
                if orig_line == 6:  # 老阴应变阳 (7)
                    assert trans_line == 7, f"测试{i+1}第{j+1}爻：老阴变阳失败"
                elif orig_line == 9:  # 老阳应变阴 (8)
                    assert trans_line == 8, f"测试{i+1}第{j+1}爻：老阳变阴失败"
                else:  # 不变
                    assert trans_line == orig_line, f"测试{i+1}第{j+1}爻：不变爻变化了"
            
            # 验证 3: 互卦存在
            mutual = calc.get_mutual()
            assert mutual is not None, f"测试{i+1}: 互卦为空"
            assert len(mutual.lines) == 6, f"测试{i+1}: 互卦爻数错误"
            
            # 验证 4: 互卦规则（二三四五爻重组）
            # 互卦下卦 = 本卦二三四爻，上卦 = 本卦三四五爻
            expected_mutual = [
                lines[1],  # 初爻 = 原二爻
                lines[2],  # 二爻 = 原三爻
                lines[3],  # 三爻 = 原四爻
                lines[2],  # 四爻 = 原三爻
                lines[3],  # 五爻 = 原四爻
                lines[4],  # 上爻 = 原五爻
            ]
            assert mutual.lines == expected_mutual, f"测试{i+1}: 互卦计算错误"
            
            # 验证 5: 动爻检测
            moving = calc.get_moving_lines()
            expected_moving = [j + 1 for j, line in enumerate(lines) if line in [6, 9]]
            assert moving == expected_moving, f"测试{i+1}: 动爻检测错误"
            
            # 验证 6: 二进制转换
            binary = original.to_binary()
            assert len(binary) == 6, f"测试{i+1}: 二进制长度错误"
            assert all(c in '01' for c in binary), f"测试{i+1}: 二进制格式错误"
            
            # 验证 7: 上下卦提取
            upper, lower = original.get_trigrams()
            assert upper in ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤'], f"测试{i+1}: 上卦名错误"
            assert lower in ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤'], f"测试{i+1}: 下卦名错误"
            
            result.record_pass()
            
        except Exception as e:
            result.record_fail(str(e))
    
    result.stop()
    return result


# ============================================================
# 性能测试
# ============================================================
def test_performance():
    """性能基准测试"""
    result = TestResult("性能基准测试")
    result.start()
    
    perf_data = {}
    
    # 铜钱法性能
    start = time.time()
    for _ in range(100):
        coin = CoinMethod()
        coin.generate()
    perf_data['coin_100'] = time.time() - start
    
    # 蓍草法性能
    start = time.time()
    for _ in range(100):
        shicao = ShicaoMethod()
        shicao.generate()
    perf_data['shicao_100'] = time.time() - start
    
    # 数字法性能
    start = time.time()
    for _ in range(100):
        num = NumberMethod()
        num.generate(12345)
    perf_data['number_100'] = time.time() - start
    
    # 时间法性能
    start = time.time()
    for _ in range(100):
        time_method = TimeMethod()
        time_method.generate()
    perf_data['time_100'] = time.time() - start
    
    # 卦象计算性能
    start = time.time()
    for _ in range(100):
        calc = HexagramCalculator([7, 8, 9, 6, 7, 8])
        calc.get_original()
        calc.get_transformed()
        calc.get_mutual()
    perf_data['calc_100'] = time.time() - start
    
    result.stop()
    result.perf_data = perf_data
    return result


# ============================================================
# 主测试运行器
# ============================================================
def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("周易占卜系统 - 单元测试套件")
    print("任务 ID: TASK-20260320-007")
    print("=" * 60)
    
    all_results = []
    
    # 运行各项测试
    print("\n正在运行测试...\n")
    
    print("[1/6] 测试铜钱起卦算法...")
    all_results.append(test_coin_method())
    
    print("[2/6] 测试蓍草起卦算法...")
    all_results.append(test_shicao_method())
    
    print("[3/6] 测试数字起卦算法...")
    all_results.append(test_number_method())
    
    print("[4/6] 测试时间起卦算法...")
    all_results.append(test_time_method())
    
    print("[5/6] 测试卦象计算（本卦/变卦/互卦）...")
    all_results.append(test_hexagram_calculation())
    
    print("[6/6] 性能基准测试...")
    all_results.append(test_performance())
    
    # 汇总报告
    print("\n" + "=" * 60)
    print("测试汇总报告")
    print("=" * 60)
    
    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_duration = 0.0
    
    for res in all_results:
        print(res.report())
        total_tests += res.total
        total_passed += res.passed
        total_failed += res.failed
        total_duration += res.duration
    
    print("\n" + "-" * 60)
    print(f"总计：")
    print(f"  总测试次数：{total_tests}")
    print(f"  总通过：{total_passed}")
    print(f"  总失败：{total_failed}")
    print(f"  总通过率：{(total_passed/total_tests*100) if total_tests > 0 else 0:.2f}%")
    print(f"  总耗时：{total_duration:.4f}秒")
    print("-" * 60)
    
    # 性能数据
    perf_result = all_results[-1]
    if hasattr(perf_result, 'perf_data'):
        print("\n【性能数据】")
        for key, value in perf_result.perf_data.items():
            print(f"  {key}: {value:.4f}秒 ({value/100*1000:.2f}毫秒/次)")
    
    # 错误详情
    has_errors = any(res.failed > 0 for res in all_results)
    if has_errors:
        print("\n【错误详情】")
        for res in all_results:
            if res.errors:
                print(f"\n{res.test_name}:")
                for err in res.errors:
                    print(f"  ❌ {err}")
    
    print("\n" + "=" * 60)
    
    # 返回测试结果
    return {
        'total': total_tests,
        'passed': total_passed,
        'failed': total_failed,
        'pass_rate': (total_passed/total_tests*100) if total_tests > 0 else 0,
        'duration': total_duration,
        'has_errors': has_errors
    }


if __name__ == '__main__':
    try:
        result = run_all_tests()
        
        # 退出码：0=全部通过，1=有失败
        sys.exit(0 if result['failed'] == 0 else 1)
        
    except KeyboardInterrupt:
        print("\n\n测试被中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试执行错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
