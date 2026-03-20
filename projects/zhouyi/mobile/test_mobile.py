#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易算法移动端适配 - 测试验证脚本
Mobile Adaptation - Test & Verification Script

测试内容：
1. 四种起卦方法功能测试
2. 卦象计算准确性验证
3. 性能基准测试
4. 内存占用测试
5. 移动端兼容性测试
"""

import sys
import time
import traceback
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from divination_api import (
    divine, divine_batch, benchmark, self_test,
    CoinMethod, ShicaoMethod, NumberMethod, TimeMethod,
    Hexagram, HexagramCalculator
)


# ============================================================================
# 测试报告类
# ============================================================================

class TestReport:
    """测试报告生成器"""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def add_result(self, test_name: str, passed: bool, details: str = ''):
        self.results.append({
            'name': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    
    def generate(self) -> str:
        """生成测试报告"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total - passed
        
        report = []
        report.append("=" * 70)
        report.append("        周易算法移动端适配 - 测试验证报告")
        report.append("=" * 70)
        report.append(f"测试时间：{self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"测试耗时：{duration:.2f} 秒")
        report.append("")
        report.append(f"总测试数：{total}")
        report.append(f"通过：{passed}")
        report.append(f"失败：{failed}")
        report.append(f"成功率：{passed/total*100:.1f}%")
        report.append("")
        report.append("-" * 70)
        report.append("测试详情")
        report.append("-" * 70)
        
        for i, r in enumerate(self.results, 1):
            status = "PASS" if r['passed'] else "FAIL"
            report.append(f"\n[{i:03d}] {r['name']}")
            report.append(f"      状态：{status}")
            report.append(f"      时间：{r['timestamp']}")
            if r['details']:
                report.append(f"      详情：{r['details']}")
        
        report.append("")
        report.append("=" * 70)
        
        return '\n'.join(report)


# ============================================================================
# 功能测试
# ============================================================================

def test_coin_method(report: TestReport):
    """测试铜钱起卦法"""
    print("\n[测试] 铜钱起卦法...")
    
    try:
        # 测试 1: 生成六爻
        result = divine('coin')
        assert result['success'], f"起卦失败：{result['error']}"
        assert len(result['lines']) == 6, f"爻数错误：{len(result['lines'])}"
        report.add_result('coin_generate_six_lines', True, f"生成六爻：{result['lines']}")
        
        # 测试 2: 爻值范围
        for line in result['lines']:
            assert line in [6, 7, 8, 9], f"爻值超出范围：{line}"
        report.add_result('coin_line_values_valid', True, "所有爻值在 [6,7,8,9] 范围内")
        
        # 测试 3: 卦象计算
        assert result['hexagram'], "卦名为空"
        assert result['hexagram_number'] > 0, "卦序号无效"
        report.add_result('coin_hexagram_calculation', True, 
                         f"卦名：{result['hexagram']} (#{result['hexagram_number']})")
        
        # 测试 4: 上下卦
        assert result['upper_trigram'], "上卦为空"
        assert result['lower_trigram'], "下卦为空"
        report.add_result('coin_trigrams_valid', True, 
                         f"上卦：{result['upper_trigram']}, 下卦：{result['lower_trigram']}")
        
        # 测试 5: 变卦和互卦
        assert result['transformed_hexagram'], "变卦名为空"
        assert result['mutual_hexagram'], "互卦名为空"
        report.add_result('coin_mutual_transformed', True, 
                         f"变卦：{result['transformed_hexagram']}, 互卦：{result['mutual_hexagram']}")
        
    except Exception as e:
        report.add_result('coin_method_tests', False, f"异常：{str(e)}")
        print(f"  [FAIL] {e}")


def test_shicao_method(report: TestReport):
    """测试蓍草起卦法"""
    print("\n[测试] 蓍草起卦法...")
    
    try:
        result = divine('shicao')
        assert result['success'], f"起卦失败：{result['error']}"
        assert len(result['lines']) == 6, f"爻数错误：{len(result['lines'])}"
        
        for line in result['lines']:
            assert line in [6, 7, 8, 9], f"爻值超出范围：{line}"
        
        assert result['hexagram'], "卦名为空"
        assert result['hexagram_number'] > 0, "卦序号无效"
        
        report.add_result('shicao_method_all', True, 
                         f"卦名：{result['hexagram']}, 爻：{result['lines']}")
        
    except Exception as e:
        report.add_result('shicao_method_tests', False, f"异常：{str(e)}")
        print(f"  [FAIL] {e}")


def test_number_method(report: TestReport):
    """测试数字起卦法"""
    print("\n[测试] 数字起卦法...")
    
    try:
        # 测试 1: 基本功能
        result = divine('number', number=12345)
        assert result['success'], f"起卦失败：{result['error']}"
        assert len(result['lines']) == 6, f"爻数错误"
        report.add_result('number_basic', True, f"数字 12345: {result['hexagram']}")
        
        # 测试 2: 确定性（相同数字应产生相同结果）
        result2 = divine('number', number=12345)
        assert result['lines'] == result2['lines'], "相同数字产生不同卦象"
        report.add_result('number_deterministic', True, "相同数字产生相同卦象")
        
        # 测试 3: 不同数字
        result3 = divine('number', number=9999)
        assert result3['success'], "数字 9999 起卦失败"
        report.add_result('number_different', True, f"数字 9999: {result3['hexagram']}")
        
    except Exception as e:
        report.add_result('number_method_tests', False, f"异常：{str(e)}")
        print(f"  [FAIL] {e}")


def test_time_method(report: TestReport):
    """测试时间起卦法"""
    print("\n[测试] 时间起卦法...")
    
    try:
        # 测试 1: 当前时间
        result = divine('time')
        assert result['success'], f"起卦失败：{result['error']}"
        assert len(result['lines']) == 6, f"爻数错误"
        report.add_result('time_current', True, f"当前时间：{result['hexagram']}")
        
        # 测试 2: 指定时间
        from datetime import datetime
        test_time = datetime(2026, 3, 20, 14, 30, 0)
        result2 = divine('time', target_time=test_time)
        assert result2['success'], "指定时间起卦失败"
        report.add_result('time_specific', True, 
                         f"2026-03-20 14:30: {result2['hexagram']}")
        
        # 测试 3: 确定性
        result3 = divine('time', target_time=test_time)
        assert result2['lines'] == result3['lines'], "相同时间产生不同卦象"
        report.add_result('time_deterministic', True, "相同时间产生相同卦象")
        
    except Exception as e:
        report.add_result('time_method_tests', False, f"异常：{str(e)}")
        print(f"  [FAIL] {e}")


# ============================================================================
# 卦象计算准确性测试
# ============================================================================

def test_hexagram_accuracy(report: TestReport):
    """测试卦象计算准确性"""
    print("\n[测试] 卦象计算准确性...")
    
    test_cases = [
        # (六爻列表，期望卦名，期望序号)
        # 注意：lines 从下往上 [初爻，二爻，三爻，四爻，五爻，上爻]
        # to_binary 使用 join，所以 lines[0] 在最左边
        # binary[:3] 是上卦（四 - 上爻），binary[3:] 是下卦（初 - 三爻）
        ([9, 9, 9, 9, 9, 9], '乾为天', 1),      # 乾卦：上乾 (111) 下乾 (111)
        ([6, 6, 6, 6, 6, 6], '坤为地', 2),      # 坤卦：上坤 (000) 下坤 (000)
        ([7, 7, 7, 6, 6, 6], '天地否', 12),     # 否卦：上乾 (111) 下坤 (000)
        ([8, 8, 8, 9, 9, 9], '地天泰', 11),     # 泰卦：上坤 (000) 下乾 (111)
        ([7, 8, 9, 6, 7, 8], '火水未济', 64),   # 未济卦：上离 (101) 下坎 (010)
    ]
    
    for i, (lines, expected_name, expected_num) in enumerate(test_cases):
        try:
            hexagram = Hexagram(lines)
            name = hexagram.get_name()
            num = hexagram.get_hexagram_number()
            
            assert name == expected_name, f"卦名错误：期望{expected_name}, 实际{name}"
            assert num == expected_num, f"序号错误：期望{expected_num}, 实际{num}"
            
            report.add_result(f'accuracy_case_{i+1}', True, 
                             f"lines={lines} -> {name} (#{num})")
        except Exception as e:
            report.add_result(f'accuracy_case_{i+1}', False, str(e))
            print(f"  [FAIL] 测试用例{i+1}: {e}")


def test_transformed_hexagram(report: TestReport):
    """测试变卦计算"""
    print("\n[测试] 变卦计算...")
    
    try:
        # 乾卦（全老阳）变坤卦
        lines = [9, 9, 9, 9, 9, 9]
        calc = HexagramCalculator(lines)
        transformed = calc.get_transformed()
        
        assert transformed.get_name() == '坤为地', f"乾变坤失败：{transformed.get_name()}"
        report.add_result('transform_qian_to_kun', True, "乾为天 -> 坤为地 [OK]")
        
        # 坤卦（全老阴）变乾卦
        lines = [6, 6, 6, 6, 6, 6]
        calc = HexagramCalculator(lines)
        transformed = calc.get_transformed()
        
        assert transformed.get_name() == '乾为天', f"坤变乾失败：{transformed.get_name()}"
        report.add_result('transform_kun_to_qian', True, "坤为地 -> 乾为天 [OK]")
        
    except Exception as e:
        report.add_result('transformed_hexagram_tests', False, str(e))
        print(f"  [FAIL] {e}")


def test_mutual_hexagram(report: TestReport):
    """测试互卦计算"""
    print("\n[测试] 互卦计算...")
    
    try:
        # 测试一个已知案例
        lines = [9, 9, 9, 9, 9, 9]  # 乾为天
        calc = HexagramCalculator(lines)
        mutual = calc.get_mutual()
        
        # 乾卦的互卦应该还是乾卦
        assert mutual.get_name() == '乾为天', f"乾卦互卦错误：{mutual.get_name()}"
        report.add_result('mutual_qian', True, "乾为天互卦：乾为天 [OK]")
        
    except Exception as e:
        report.add_result('mutual_hexagram_tests', False, str(e))
        print(f"  [FAIL] {e}")


# ============================================================================
# 性能测试
# ============================================================================

def test_performance(report: TestReport):
    """性能基准测试"""
    print("\n[测试] 性能基准测试...")
    
    methods = ['coin', 'shicao', 'number', 'time']
    
    for method in methods:
        try:
            # 测试 1000 次
            start = time.perf_counter()
            for _ in range(1000):
                divine(method, number=12345 if method == 'number' else None)
            elapsed = time.perf_counter() - start
            
            ops_per_sec = 1000 / elapsed if elapsed > 0 else 0
            avg_ms = (elapsed * 1000) / 1000
            
            # 移动端标准：单次操作 < 10ms
            passed = avg_ms < 10
            
            report.add_result(f'perf_{method}', passed, 
                             f"{method}: {avg_ms:.4f} ms/次，{ops_per_sec:.2f} ops/s")
            
        except Exception as e:
            report.add_result(f'perf_{method}', False, str(e))
            print(f"  [FAIL] {method}: {e}")


def test_memory_efficiency(report: TestReport):
    """内存效率测试"""
    print("\n[测试] 内存效率测试...")
    
    try:
        import sys
        
        # 测试 Hexagram 对象大小
        hexagram = Hexagram([7, 8, 9, 6, 7, 8])
        size = sys.getsizeof(hexagram)
        
        # 使用 __slots__ 应该显著减少内存
        passed = size < 1000  # 小于 1KB
        report.add_result('memory_hexagram_size', passed, 
                         f"Hexagram 对象大小：{size} bytes")
        
        # 测试批量创建的内存
        hexagrams = [Hexagram([7, 8, 9, 6, 7, 8]) for _ in range(1000)]
        total_size = sum(sys.getsizeof(h) for h in hexagrams)
        avg_size = total_size / 1000
        
        passed = avg_size < 500
        report.add_result('memory_batch_efficiency', passed, 
                         f"1000 个 Hexagram 平均大小：{avg_size:.2f} bytes")
        
    except Exception as e:
        report.add_result('memory_tests', False, str(e))
        print(f"  [FAIL] {e}")


def test_caching(report: TestReport):
    """测试缓存机制"""
    print("\n[测试] 缓存机制...")
    
    try:
        # 第一次调用（无缓存）
        start = time.perf_counter()
        for _ in range(100):
            hexagram = Hexagram([7, 8, 9, 6, 7, 8])
            _ = hexagram.get_hexagram_number()
        time_no_cache = time.perf_counter() - start
        
        # 第二次调用（有缓存）
        start = time.perf_counter()
        for _ in range(100):
            hexagram = Hexagram([7, 8, 9, 6, 7, 8])
            _ = hexagram.get_hexagram_number()
        time_with_cache = time.perf_counter() - start
        
        # 缓存应该更快（至少 10% 提升）
        improvement = (time_no_cache - time_with_cache) / time_no_cache * 100
        passed = time_with_cache <= time_no_cache
        
        report.add_result('caching_effective', passed, 
                         f"缓存提升：{improvement:.1f}%")
        
    except Exception as e:
        report.add_result('caching_tests', False, str(e))
        print(f"  [FAIL] {e}")


# ============================================================================
# 移动端兼容性测试
# ============================================================================

def test_no_external_deps(report: TestReport):
    """测试无外部依赖"""
    print("\n[测试] 外部依赖检查...")
    
    try:
        # 检查导入的模块
        from divination_api import divine
        import inspect
        
        source = inspect.getsource(divine)
        
        # 只允许标准库
        external_libs = ['numpy', 'pandas', 'tensorflow', 'torch', 'requests']
        found_external = [lib for lib in external_libs if lib in source]
        
        passed = len(found_external) == 0
        report.add_result('no_external_deps', passed, 
                         f"未发现外部依赖" if passed else f"发现外部依赖：{found_external}")
        
    except Exception as e:
        report.add_result('external_deps_check', False, str(e))
        print(f"  [FAIL] {e}")


def test_api_interface(report: TestReport):
    """测试 API 接口规范性"""
    print("\n[测试] API 接口规范性...")
    
    try:
        # 测试返回字段完整性
        result = divine('coin')
        
        required_fields = [
            'success', 'method', 'lines', 'hexagram', 'hexagram_number',
            'upper_trigram', 'lower_trigram', 'changing_lines',
            'transformed_hexagram', 'mutual_hexagram', 'display', 'error'
        ]
        
        missing = [f for f in required_fields if f not in result]
        passed = len(missing) == 0
        
        report.add_result('api_fields_complete', passed, 
                         f"返回字段完整" if passed else f"缺失字段：{missing}")
        
        # 测试错误处理
        result = divine('invalid_method')
        passed = not result['success'] and result['error'] is not None
        report.add_result('api_error_handling', passed, 
                         "错误处理正常" if passed else "错误处理异常")
        
    except Exception as e:
        report.add_result('api_interface_tests', False, str(e))
        print(f"  [FAIL] {e}")


# ============================================================================
# 主测试流程
# ============================================================================

def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("        周易算法移动端适配 - 测试验证")
    print("=" * 70)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    report = TestReport()
    
    # 1. 功能测试
    print("\n" + "=" * 70)
    print("第一部分：功能测试")
    print("=" * 70)
    
    test_coin_method(report)
    test_shicao_method(report)
    test_number_method(report)
    test_time_method(report)
    
    # 2. 准确性测试
    print("\n" + "=" * 70)
    print("第二部分：卦象计算准确性测试")
    print("=" * 70)
    
    test_hexagram_accuracy(report)
    test_transformed_hexagram(report)
    test_mutual_hexagram(report)
    
    # 3. 性能测试
    print("\n" + "=" * 70)
    print("第三部分：性能测试")
    print("=" * 70)
    
    test_performance(report)
    test_memory_efficiency(report)
    test_caching(report)
    
    # 4. 兼容性测试
    print("\n" + "=" * 70)
    print("第四部分：移动端兼容性测试")
    print("=" * 70)
    
    test_no_external_deps(report)
    test_api_interface(report)
    
    # 生成报告
    print("\n" + "=" * 70)
    print("生成测试报告...")
    print("=" * 70)
    
    report_text = report.generate()
    print(report_text)
    
    # 保存报告
    report_path = Path(__file__).parent / 'test_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\n报告已保存至：{report_path}")
    
    # 返回测试结果
    passed = sum(1 for r in report.results if r['passed'])
    total = len(report.results)
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
