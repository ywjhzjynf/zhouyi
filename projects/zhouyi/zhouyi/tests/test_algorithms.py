#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易起卦算法单元测试
Test Suite for Zhouyi Divination Algorithms

测试覆盖：
1. 铜钱起卦法（CoinMethod）
2. 蓍草起卦法（ShicaoMethod）
3. 数字起卦法（NumberMethod）
4. 时间起卦法（TimeMethod）
"""

import unittest
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.calculator import CoinMethod, ShicaoMethod, NumberMethod, TimeMethod
from core.hexagram import Hexagram, HexagramCalculator


class TestCoinMethod(unittest.TestCase):
    """铜钱起卦法测试"""
    
    def setUp(self):
        self.coin = CoinMethod()
    
    def test_toss_range(self):
        """测试单次抛掷结果范围（6-9）"""
        for _ in range(100):
            result = self.coin.toss()
            self.assertIn(result, [6, 7, 8, 9], 
                f"铜钱抛掷结果 {result} 不在有效范围 [6,7,8,9]")
    
    def test_generate_six_lines(self):
        """测试生成六爻"""
        lines = self.coin.generate()
        self.assertEqual(len(lines), 6, "应生成六爻")
    
    def test_line_meanings(self):
        """测试爻位解释"""
        meanings = {
            6: '老阴（变爻）',
            7: '少阳（不变）',
            8: '少阴（不变）',
            9: '老阳（变爻）'
        }
        for value, expected in meanings.items():
            result = self.coin.get_line_meaning(value)
            self.assertEqual(result, expected, 
                f"爻值 {value} 的解释应为 {expected}")
    
    def test_probability_distribution(self):
        """测试概率分布（大样本）"""
        results = {6: 0, 7: 0, 8: 0, 9: 0}
        for _ in range(1000):
            result = self.coin.toss()
            results[result] += 1
        
        # 理论上：6(老阴)≈1/8, 7(少阳)≈3/8, 8(少阴)≈3/8, 9(老阳)≈1/8
        # 允许较大误差范围
        self.assertGreater(results[7], 200, "少阳应占约 37.5%")
        self.assertGreater(results[8], 200, "少阴应占约 37.5%")
        self.assertGreater(results[6], 50, "老阴应占约 12.5%")
        self.assertGreater(results[9], 50, "老阳应占约 12.5%")


class TestShicaoMethod(unittest.TestCase):
    """蓍草起卦法测试"""
    
    def setUp(self):
        self.shicao = ShicaoMethod()
    
    def test_generate_six_lines(self):
        """测试生成六爻"""
        lines = self.shicao.generate()
        self.assertEqual(len(lines), 6, "应生成六爻")
    
    def test_line_values(self):
        """测试爻值有效性"""
        for _ in range(10):
            lines = self.shicao.generate()
            for line in lines:
                self.assertIn(line, [6, 7, 8, 9], 
                    f"蓍草结果 {line} 不在有效范围")
    
    def test_divide_process(self):
        """测试分二挂一过程"""
        # 测试 49 根蓍草的分法
        # divide 返回的是揲四后的余数，不是实际蓍草数
        left, right, gui_yi = self.shicao.divide(49)
        self.assertEqual(gui_yi, 1, "挂一应为 1")
        self.assertIn(left, [1, 2, 3, 4], "左余数应在 1-4 之间")
        self.assertIn(right, [1, 2, 3, 4], "右余数应在 1-4 之间")
        # 余数 + 挂一 = 5 或 9（第一变）
        total = left + right + gui_yi
        self.assertIn(total, [5, 9], f"第一变余数和应为 5 或 9，实际{total}")


class TestNumberMethod(unittest.TestCase):
    """数字起卦法测试"""
    
    def setUp(self):
        self.number = NumberMethod()
    
    def test_single_number(self):
        """测试单个数字起卦"""
        lines = self.number.generate(12345)
        self.assertEqual(len(lines), 6, "应生成六爻")
        for line in lines:
            self.assertIn(line, [6, 7, 8, 9])
    
    def test_deterministic_result(self):
        """测试相同数字产生相同卦象"""
        lines1 = self.number.generate(9999)
        lines2 = self.number.generate(9999)
        self.assertEqual(lines1, lines2, "相同数字应产生相同卦象")
    
    def test_trigram_info(self):
        """测试卦象信息接口"""
        info = self.number.get_trigram_info(12345)
        self.assertIn('upper', info)
        self.assertIn('lower', info)
        self.assertIn('moving', info)
        self.assertIn('upper_name', info)
        self.assertIn('lower_name', info)


class TestTimeMethod(unittest.TestCase):
    """时间起卦法测试"""
    
    def setUp(self):
        self.time = TimeMethod()
    
    def test_current_time(self):
        """测试当前时间起卦"""
        lines = self.time.generate()
        self.assertEqual(len(lines), 6, "应生成六爻")
        for line in lines:
            self.assertIn(line, [6, 7, 8, 9])
    
    def test_specific_time(self):
        """测试指定时间起卦"""
        from datetime import datetime
        specific_time = datetime(2026, 3, 20, 14, 30, 0)
        lines = self.time.generate(specific_time)
        self.assertEqual(len(lines), 6, "应生成六爻")
    
    def test_deterministic_for_same_time(self):
        """测试相同时间产生相同卦象"""
        from datetime import datetime
        test_time = datetime(2026, 1, 1, 12, 0, 0)
        lines1 = self.time.generate(test_time)
        lines2 = self.time.generate(test_time)
        self.assertEqual(lines1, lines2, "相同时间应产生相同卦象")
    
    def test_time_info(self):
        """测试时间卦象信息接口"""
        from datetime import datetime
        test_time = datetime(2026, 3, 20, 14, 30, 0)
        info = self.time.get_time_info(test_time)
        self.assertIn('upper', info)
        self.assertIn('lower', info)
        self.assertIn('moving', info)
        self.assertIn('time', info)
        self.assertIn('upper_name', info)
        self.assertIn('lower_name', info)


class TestHexagramCalculator(unittest.TestCase):
    """卦象计算器测试"""
    
    def test_binary_conversion(self):
        """测试二进制转换"""
        # 乾卦：全阳（9,9,9,9,9,9）
        hexagram = Hexagram([9, 9, 9, 9, 9, 9])
        self.assertEqual(hexagram.to_binary(), '111111')
        
        # 坤卦：全阴（6,6,6,6,6,6）
        hexagram = Hexagram([6, 6, 6, 6, 6, 6])
        self.assertEqual(hexagram.to_binary(), '000000')
    
    def test_trigram_identification(self):
        """测试上下卦识别"""
        # 乾为天：上乾下乾
        hexagram = Hexagram([9, 9, 9, 9, 9, 9])
        upper, lower = hexagram.get_trigrams()
        self.assertEqual(upper, '乾')
        self.assertEqual(lower, '乾')
        
        # 地天泰：上坤下乾
        hexagram = Hexagram([9, 9, 9, 6, 6, 6])
        upper, lower = hexagram.get_trigrams()
        self.assertEqual(upper, '坤')
        self.assertEqual(lower, '乾')
    
    def test_changing_lines(self):
        """测试变爻识别"""
        lines = [9, 7, 8, 6, 7, 8]  # 初爻和四爻是变爻
        hexagram = Hexagram(lines)
        changing = hexagram.get_changing_lines()
        self.assertEqual(len(changing), 2)
        self.assertIn(1, changing)  # 初爻
        self.assertIn(4, changing)  # 四爻
    
    def test_transformed_hexagram(self):
        """测试变卦计算"""
        # 有变爻的情况
        lines = [9, 7, 8, 8, 8, 8]  # 初爻是老阳，会变阴
        calc = HexagramCalculator(lines)
        transformed = calc.get_transformed_lines()
        self.assertEqual(transformed[0], 8)  # 老阳变少阴


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_coin_method_speed(self):
        """测试铜钱起卦性能"""
        import time
        coin = CoinMethod()
        start = time.time()
        for _ in range(1000):
            coin.generate()
        elapsed = time.time() - start
        self.assertLess(elapsed, 1.0, f"1000 次铜钱起卦应在 1 秒内完成，实际 {elapsed:.3f}秒")
    
    def test_shicao_method_speed(self):
        """测试蓍草起卦性能"""
        import time
        shicao = ShicaoMethod()
        start = time.time()
        for _ in range(100):
            shicao.generate()
        elapsed = time.time() - start
        self.assertLess(elapsed, 2.0, f"100 次蓍草起卦应在 2 秒内完成，实际 {elapsed:.3f}秒")


def run_tests():
    """运行所有测试并生成报告"""
    print("\n" + "=" * 60)
    print("        周易占卜系统 - 算法单元测试报告")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestCoinMethod))
    suite.addTests(loader.loadTestsFromTestCase(TestShicaoMethod))
    suite.addTests(loader.loadTestsFromTestCase(TestNumberMethod))
    suite.addTests(loader.loadTestsFromTestCase(TestTimeMethod))
    suite.addTests(loader.loadTestsFromTestCase(TestHexagramCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 生成摘要
    print("\n" + "=" * 60)
    print("测试摘要")
    print("=" * 60)
    print(f"总测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    print(f"成功率：{(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    if result.failures or result.errors:
        print("\n[WARN] 存在失败或错误的测试，请检查上方详情")
        return False
    else:
        print("\n[PASS] 所有测试通过！")
        return True


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
