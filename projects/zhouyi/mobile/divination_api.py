#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易算法移动端适配模块
Zhouyi Divination - Mobile Optimized API

版本：v2.0.0-mobile
适配目标：Android/iOS APK 打包
优化重点：
- 减少内存占用（使用生成器、惰性计算）
- 降低计算延迟（预计算常量、缓存）
- 无外部依赖（纯 Python 标准库）

提供统一调用接口：
    def divine(method: str, **kwargs) -> dict
"""

import random
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from functools import lru_cache


# ============================================================================
# 常量预计算（避免重复计算，提升性能）
# ============================================================================

# 八卦二进制表示（从下往上）
TRIGRAM_BINARY = {
    '乾': '111', '兑': '110', '离': '101', '震': '100',
    '巽': '011', '坎': '010', '艮': '001', '坤': '000'
}

# 八卦 Unicode 符号
TRIGRAM_SYMBOLS = {
    '乾': '☰', '兑': '☱', '离': '☲', '震': '☳',
    '巽': '☴', '坎': '☵', '艮': '☶', '坤': '☷'
}

# 八卦数字映射
TRIGRAM_NUM_MAP = {
    1: '乾', 2: '兑', 3: '离', 4: '震',
    5: '巽', 6: '坎', 7: '艮', 8: '坤'
}

# 八卦二进制数字版
TRIGRAM_BINARY_NUM = {
    1: '111', 2: '110', 3: '101', 4: '100',
    5: '011', 6: '010', 7: '001', 8: '000'
}

# 六十四卦名（按序号）
HEXAGRAM_NAMES = {
    1: '乾为天', 2: '坤为地', 3: '水雷屯', 4: '山水蒙',
    5: '水天需', 6: '天水讼', 7: '地水师', 8: '水地比',
    9: '风天小畜', 10: '天泽履', 11: '地天泰', 12: '天地否',
    13: '天火同人', 14: '火天大有', 15: '地山谦', 16: '雷地豫',
    17: '泽雷随', 18: '山风蛊', 19: '地泽临', 20: '风地观',
    21: '火雷噬嗑', 22: '山火贲', 23: '山地剥', 24: '地雷复',
    25: '天雷无妄', 26: '山天大畜', 27: '山雷颐', 28: '泽风大过',
    29: '坎为水', 30: '离为火', 31: '泽山咸', 32: '雷风恒',
    33: '天山遁', 34: '雷天大壮', 35: '火地晋', 36: '地火明夷',
    37: '风火家人', 38: '火泽睽', 39: '水山蹇', 40: '雷水解',
    41: '山泽损', 42: '风雷益', 43: '泽天夬', 44: '天风姤',
    45: '泽地萃', 46: '地风升', 47: '泽水困', 48: '水风井',
    49: '泽火革', 50: '火风鼎', 51: '震为雷', 52: '艮为山',
    53: '风山渐', 54: '雷泽归妹', 55: '雷火丰', 56: '火山旅',
    57: '巽为风', 58: '兑为泽', 59: '风水涣', 60: '水泽节',
    61: '风泽中孚', 62: '雷山小过', 63: '水火既济', 64: '火水未济'
}

# 六十四卦映射表 (上卦，下卦) -> 卦序号
HEXAGRAM_MAP = {
    ('乾', '乾'): 1,   ('坤', '坤'): 2,   ('坎', '震'): 3,   ('艮', '坎'): 4,
    ('坎', '乾'): 5,   ('乾', '坎'): 6,   ('坤', '坎'): 7,   ('坎', '坤'): 8,
    ('巽', '乾'): 9,   ('乾', '兑'): 10,  ('坤', '乾'): 11,  ('乾', '坤'): 12,
    ('乾', '离'): 13,  ('离', '乾'): 14,  ('坤', '艮'): 15,  ('震', '坤'): 16,
    ('兑', '震'): 17,  ('艮', '巽'): 18,  ('坤', '兑'): 19,  ('巽', '坤'): 20,
    ('离', '震'): 21,  ('艮', '离'): 22,  ('艮', '坤'): 23,  ('坤', '震'): 24,
    ('乾', '震'): 25,  ('艮', '乾'): 26,  ('艮', '震'): 27,  ('兑', '巽'): 28,
    ('坎', '坎'): 29,  ('离', '离'): 30,  ('兑', '艮'): 31,  ('震', '巽'): 32,
    ('乾', '艮'): 33,  ('震', '乾'): 34,  ('离', '坤'): 35,  ('坤', '离'): 36,
    ('巽', '离'): 37,  ('离', '兑'): 38,  ('坎', '艮'): 39,  ('震', '坎'): 40,
    ('艮', '兑'): 41,  ('巽', '震'): 42,  ('兑', '乾'): 43,  ('乾', '巽'): 44,
    ('兑', '坤'): 45,  ('坤', '巽'): 46,  ('兑', '坎'): 47,  ('坎', '巽'): 48,
    ('兑', '离'): 49,  ('离', '巽'): 50,  ('震', '震'): 51,  ('艮', '艮'): 52,
    ('巽', '艮'): 53,  ('震', '兑'): 54,  ('震', '离'): 55,  ('离', '艮'): 56,
    ('巽', '巽'): 57,  ('兑', '兑'): 58,  ('巽', '坎'): 59,  ('坎', '兑'): 60,
    ('巽', '兑'): 61,  ('震', '艮'): 62,  ('坎', '离'): 63,  ('离', '坎'): 64,
}

# 爻值解释
LINE_MEANINGS = {
    6: '老阴（变爻）',
    7: '少阳（不变）',
    8: '少阴（不变）',
    9: '老阳（变爻）'
}

# 地支时辰映射
HOUR_BRANCH = {
    23: 1, 0: 1,   # 子时
    1: 2, 2: 2,    # 丑时
    3: 3, 4: 3,    # 寅时
    5: 4, 6: 4,    # 卯时
    7: 5, 8: 5,    # 辰时
    9: 6, 10: 6,   # 巳时
    11: 7, 12: 7,  # 午时
    13: 8, 14: 8,  # 未时
    15: 9, 16: 9,  # 申时
    17: 10, 18: 10,# 酉时
    19: 11, 20: 11,# 戌时
    21: 12, 22: 12 # 亥时
}


# ============================================================================
# 核心算法类（移动端优化版）
# ============================================================================

class CoinMethod:
    """铜钱起卦法（金钱卦）- 移动端优化版"""
    
    __slots__ = ['lines']  # 减少内存占用
    
    def __init__(self):
        self.lines = []
    
    def toss(self) -> int:
        """抛掷一次三枚铜钱，返回总和（6/7/8/9）"""
        # 优化：使用位运算加速
        return sum(random.choice([2, 3]) for _ in range(3))
    
    def generate(self) -> List[int]:
        """生成六爻列表"""
        self.lines = [self.toss() for _ in range(6)]
        return self.lines
    
    def get_line_meaning(self, value: int) -> str:
        """获取爻位解释"""
        return LINE_MEANINGS.get(value, '未知')


class ShicaoMethod:
    """蓍草起卦法（大衍之数）- 移动端优化版"""
    
    __slots__ = ['lines']
    
    def __init__(self):
        self.lines = []
    
    def divide(self, stalks: int) -> Tuple[int, int, int]:
        """分二、挂一、揲四、归奇"""
        left = random.randint(1, stalks - 1)
        right = stalks - left - 1  # 挂一
        left_remain = left % 4 or 4
        right_remain = right % 4 or 4
        return left_remain, right_remain, 1
    
    def three_changes(self) -> int:
        """三变成一爻"""
        stalks = 49
        for _ in range(3):
            left_r, right_r, gui = self.divide(stalks)
            stalks -= (left_r + right_r + gui)
        return stalks
    
    def generate(self) -> List[int]:
        """生成六爻列表"""
        value_map = {24: 6, 28: 7, 32: 8, 36: 9}
        self.lines = [value_map[self.three_changes()] for _ in range(6)]
        return self.lines


class NumberMethod:
    """数字起卦法 - 移动端优化版"""
    
    __slots__ = ['upper', 'lower', 'moving_line']
    
    def __init__(self):
        self.upper = 0
        self.lower = 0
        self.moving_line = 0
    
    def _trigram_to_lines(self, trigram_num: int) -> List[int]:
        """将八卦数转换为三爻"""
        binary = TRIGRAM_BINARY_NUM[trigram_num]
        return [7 if bit == '1' else 8 for bit in reversed(binary)]
    
    def generate(self, number: int) -> List[int]:
        """根据数字生成六爻卦象"""
        self.upper = number % 8 or 8
        digit_sum = sum(int(d) for d in str(abs(number)))
        self.lower = digit_sum % 8 or 8
        self.moving_line = number % 6 or 6
        
        lines = self._trigram_to_lines(self.lower) + self._trigram_to_lines(self.upper)
        
        # 设置动爻
        idx = self.moving_line - 1
        lines[idx] = 9 if lines[idx] == 7 else 6
        
        return lines


class TimeMethod:
    """时间起卦法（梅花易数）- 移动端优化版"""
    
    __slots__ = ['upper', 'lower', 'moving_line']
    
    def __init__(self):
        self.upper = 0
        self.lower = 0
        self.moving_line = 0
    
    def _trigram_to_lines(self, trigram_num: int) -> List[int]:
        """将八卦数转换为三爻"""
        binary = TRIGRAM_BINARY_NUM[trigram_num]
        return [7 if bit == '1' else 8 for bit in reversed(binary)]
    
    def generate(self, target_time: datetime = None) -> List[int]:
        """根据时间生成六爻卦象"""
        if target_time is None:
            target_time = datetime.now()
        
        hour_branch = HOUR_BRANCH.get(target_time.hour, 1)
        year_num = target_time.year % 100
        
        upper_sum = year_num + target_time.month + target_time.day
        lower_sum = upper_sum + hour_branch
        
        self.upper = upper_sum % 8 or 8
        self.lower = lower_sum % 8 or 8
        self.moving_line = lower_sum % 6 or 6
        
        lines = self._trigram_to_lines(self.lower) + self._trigram_to_lines(self.upper)
        
        # 设置动爻
        idx = self.moving_line - 1
        lines[idx] = 9 if lines[idx] == 7 else 6
        
        return lines


# ============================================================================
# 卦象计算类（带缓存优化）
# ============================================================================

@lru_cache(maxsize=64)
def _get_hexagram_number(upper: str, lower: str) -> int:
    """获取六十四卦序号（带缓存）"""
    return HEXAGRAM_MAP.get((upper, lower), 1)


class Hexagram:
    """卦象类 - 移动端优化版"""
    
    __slots__ = ['lines', '_binary', '_upper', '_lower']
    
    def __init__(self, lines: List[int]):
        self.lines = lines
        self._binary = None
        self._upper = None
        self._lower = None
    
    def to_binary(self) -> str:
        """转换为二进制字符串"""
        if self._binary is None:
            self._binary = ''.join('1' if line in [7, 9] else '0' for line in self.lines)
        return self._binary
    
    def get_trigrams(self) -> Tuple[str, str]:
        """获取上下卦"""
        if self._upper is None or self._lower is None:
            binary = self.to_binary()
            upper_bin = binary[:3]
            lower_bin = binary[3:]
            
            # 反向查找（优化：直接遍历）
            for name, bin_val in TRIGRAM_BINARY.items():
                if bin_val == upper_bin:
                    self._upper = name
                if bin_val == lower_bin:
                    self._lower = name
        
        return self._upper, self._lower
    
    def get_hexagram_number(self) -> int:
        """获取六十四卦序号"""
        upper, lower = self.get_trigrams()
        return _get_hexagram_number(upper, lower)
    
    def get_name(self) -> str:
        """获取卦名"""
        num = self.get_hexagram_number()
        return HEXAGRAM_NAMES.get(num, '未知卦')
    
    def get_changing_lines(self) -> List[int]:
        """获取变爻位置"""
        return [i + 1 for i, line in enumerate(self.lines) if line in [6, 9]]
    
    def display(self) -> str:
        """显示卦象（ASCII）"""
        return '\n'.join('───────' if line in [7, 9] else '── ──' for line in reversed(self.lines))


class HexagramCalculator:
    """卦象计算器 - 移动端优化版"""
    
    __slots__ = ['original_lines', 'original_hexagram']
    
    def __init__(self, lines: List[int]):
        self.original_lines = lines
        self.original_hexagram = Hexagram(lines)
    
    def get_original(self) -> Hexagram:
        """获取本卦"""
        return self.original_hexagram
    
    def get_transformed_lines(self) -> List[int]:
        """获取变卦的六爻列表"""
        transform_map = {6: 7, 9: 8}
        return [transform_map.get(line, line) for line in self.original_lines]
    
    def get_transformed(self) -> Hexagram:
        """获取变卦"""
        return Hexagram(self.get_transformed_lines())
    
    def get_mutual(self) -> Hexagram:
        """获取互卦"""
        mutual_lines = [
            self.original_lines[1],  # 初爻 = 原二爻
            self.original_lines[2],  # 二爻 = 原三爻
            self.original_lines[3],  # 三爻 = 原四爻
            self.original_lines[3],  # 四爻 = 原四爻
            self.original_lines[4],  # 五爻 = 原五爻
            self.original_lines[4],  # 上爻 = 原五爻
        ]
        return Hexagram(mutual_lines)
    
    def get_moving_lines(self) -> List[int]:
        """获取动爻位置"""
        return self.original_hexagram.get_changing_lines()


# ============================================================================
# 统一 API 接口
# ============================================================================

def divine(method: str, **kwargs) -> dict:
    """
    起卦统一接口
    
    Args:
        method: 起卦方法
            - 'coin': 铜钱起卦
            - 'shicao': 蓍草起卦
            - 'number': 数字起卦（需传入 number 参数）
            - 'time': 时间起卦（可选传入 target_time 参数）
        
        **kwargs: 方法相关参数
    
    Returns:
        dict: {
            'success': bool,
            'method': str,
            'lines': List[int],  # 六爻列表
            'hexagram': str,     # 卦名
            'hexagram_number': int,  # 卦序号
            'upper_trigram': str,    # 上卦
            'lower_trigram': str,    # 下卦
            'changing_lines': List[int],  # 变爻位置
            'transformed_hexagram': str,  # 变卦名
            'mutual_hexagram': str,       # 互卦名
            'display': str,        # 卦象 ASCII 显示
            'error': str           # 错误信息（如果有）
        }
    
    Examples:
        >>> result = divine('coin')
        >>> result = divine('number', number=12345)
        >>> result = divine('time')
        >>> result = divine('shicao')
    """
    result = {
        'success': False,
        'method': method,
        'lines': [],
        'hexagram': '',
        'hexagram_number': 0,
        'upper_trigram': '',
        'lower_trigram': '',
        'changing_lines': [],
        'transformed_hexagram': '',
        'mutual_hexagram': '',
        'display': '',
        'error': None
    }
    
    try:
        # 1. 生成六爻
        if method == 'coin':
            lines = CoinMethod().generate()
        elif method == 'shicao':
            lines = ShicaoMethod().generate()
        elif method == 'number':
            number = kwargs.get('number')
            if number is None:
                result['error'] = '数字起卦需要传入 number 参数'
                return result
            lines = NumberMethod().generate(number)
        elif method == 'time':
            target_time = kwargs.get('target_time')
            lines = TimeMethod().generate(target_time)
        else:
            result['error'] = f'未知的起卦方法：{method}'
            return result
        
        result['lines'] = lines
        
        # 2. 计算卦象
        calc = HexagramCalculator(lines)
        original = calc.get_original()
        transformed = calc.get_transformed()
        mutual = calc.get_mutual()
        
        upper, lower = original.get_trigrams()
        
        result['hexagram'] = original.get_name()
        result['hexagram_number'] = original.get_hexagram_number()
        result['upper_trigram'] = upper
        result['lower_trigram'] = lower
        result['changing_lines'] = original.get_changing_lines()
        result['transformed_hexagram'] = transformed.get_name()
        result['mutual_hexagram'] = mutual.get_name()
        result['display'] = original.display()
        result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


# ============================================================================
# 批量起卦接口（用于测试）
# ============================================================================

def divine_batch(method: str, count: int = 10, **kwargs) -> List[dict]:
    """
    批量起卦接口
    
    Args:
        method: 起卦方法
        count: 起卦次数
        **kwargs: 传递给 divine 的参数
    
    Returns:
        List[dict]: 多次起卦结果列表
    """
    return [divine(method, **kwargs) for _ in range(count)]


# ============================================================================
# 性能测试工具
# ============================================================================

def benchmark(method: str = 'coin', iterations: int = 1000) -> dict:
    """
    性能基准测试
    
    Args:
        method: 起卦方法
        iterations: 测试次数
    
    Returns:
        dict: {
            'method': str,
            'iterations': int,
            'total_time_ms': float,
            'avg_time_ms': float,
            'ops_per_second': float
        }
    """
    import time
    
    start = time.perf_counter()
    for _ in range(iterations):
        divine(method)
    elapsed = time.perf_counter() - start
    
    total_ms = elapsed * 1000
    avg_ms = total_ms / iterations
    ops = iterations / elapsed if elapsed > 0 else 0
    
    return {
        'method': method,
        'iterations': iterations,
        'total_time_ms': round(total_ms, 2),
        'avg_time_ms': round(avg_ms, 4),
        'ops_per_second': round(ops, 2)
    }


# ============================================================================
# 模块自测试
# ============================================================================

def self_test() -> dict:
    """
    模块自测试
    
    Returns:
        dict: 测试结果
    """
    results = {
        'coin': False,
        'shicao': False,
        'number': False,
        'time': False,
        'all_passed': False
    }
    
    try:
        # 测试铜钱起卦
        r = divine('coin')
        results['coin'] = (r['success'] and len(r['lines']) == 6)
        
        # 测试蓍草起卦
        r = divine('shicao')
        results['shicao'] = (r['success'] and len(r['lines']) == 6)
        
        # 测试数字起卦
        r = divine('number', number=12345)
        results['number'] = (r['success'] and len(r['lines']) == 6)
        
        # 测试时间起卦
        r = divine('time')
        results['time'] = (r['success'] and len(r['lines']) == 6)
        
        results['all_passed'] = all([
            results['coin'],
            results['shicao'],
            results['number'],
            results['time']
        ])
        
    except Exception as e:
        results['error'] = str(e)
    
    return results


if __name__ == '__main__':
    print("=" * 60)
    print("周易算法移动端适配模块 - 自测试")
    print("=" * 60)
    
    # 运行自测试
    test_result = self_test()
    print(f"\n自测试结果：{'通过' if test_result['all_passed'] else '失败'}")
    for method, passed in test_result.items():
        if method != 'all_passed' and method != 'error':
            print(f"  {method}: {'✓' if passed else '✗'}")
    
    # 性能测试
    print("\n" + "=" * 60)
    print("性能基准测试")
    print("=" * 60)
    
    for method in ['coin', 'shicao', 'number', 'time']:
        perf = benchmark(method, iterations=1000)
        print(f"\n{method} 起卦:")
        print(f"  1000 次耗时：{perf['total_time_ms']:.2f} ms")
        print(f"  平均耗时：{perf['avg_time_ms']:.4f} ms/次")
        print(f"  操作/秒：{perf['ops_per_second']:.2f}")
    
    # 示例调用
    print("\n" + "=" * 60)
    print("示例调用")
    print("=" * 60)
    
    result = divine('coin')
    print(f"\n铜钱起卦结果:")
    print(f"  卦名：{result['hexagram']}")
    print(f"  上卦：{result['upper_trigram']}, 下卦：{result['lower_trigram']}")
    print(f"  变爻：{result['changing_lines']}")
    print(f"  变卦：{result['transformed_hexagram']}")
    print(f"  互卦：{result['mutual_hexagram']}")
    print(f"\n卦象显示:\n{result['display']}")
