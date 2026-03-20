"""
周易卦象计算模块
Zhouyi Divination - Hexagram Calculation

包含：
- 本卦计算
- 变卦计算
- 互卦计算
- 卦象查询
"""

from typing import List, Dict, Optional


class Hexagram:
    """
    单个卦象类
    """
    
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
    
    # 完整的 64 卦映射表 (上卦，下卦) -> 卦序号
    # 基于 hexagrams.json 数据生成
    HEXAGRAM_MAP = {
        ('乾', '乾'): 1,   # 乾为天
        ('坤', '坤'): 2,   # 坤为地
        ('坎', '震'): 3,   # 水雷屯
        ('艮', '坎'): 4,   # 山水蒙
        ('坎', '乾'): 5,   # 水天需
        ('乾', '坎'): 6,   # 天水讼
        ('坤', '坎'): 7,   # 地水师
        ('坎', '坤'): 8,   # 水地比
        ('巽', '乾'): 9,   # 风天小畜
        ('乾', '兑'): 10,  # 天泽履
        ('坤', '乾'): 11,  # 地天泰
        ('乾', '坤'): 12,  # 天地否
        ('乾', '离'): 13,  # 天火同人
        ('离', '乾'): 14,  # 火天大有
        ('坤', '艮'): 15,  # 地山谦
        ('震', '坤'): 16,  # 雷地豫
        ('兑', '震'): 17,  # 泽雷随
        ('艮', '巽'): 18,  # 山风蛊
        ('坤', '兑'): 19,  # 地泽临
        ('巽', '坤'): 20,  # 风地观
        ('离', '震'): 21,  # 火雷噬嗑
        ('艮', '离'): 22,  # 山火贲
        ('艮', '坤'): 23,  # 山地剥
        ('坤', '震'): 24,  # 地雷复
        ('乾', '震'): 25,  # 天雷无妄
        ('艮', '乾'): 26,  # 山天大畜
        ('艮', '震'): 27,  # 山雷颐
        ('兑', '巽'): 28,  # 泽风大过
        ('坎', '坎'): 29,  # 坎为水
        ('离', '离'): 30,  # 离为火
        ('兑', '艮'): 31,  # 泽山咸
        ('震', '巽'): 32,  # 雷风恒
        ('乾', '艮'): 33,  # 天山遁
        ('震', '乾'): 34,  # 雷天大壮
        ('离', '坤'): 35,  # 火地晋
        ('坤', '离'): 36,  # 地火明夷
        ('巽', '离'): 37,  # 风火家人
        ('离', '兑'): 38,  # 火泽睽
        ('坎', '艮'): 39,  # 水山蹇
        ('震', '坎'): 40,  # 雷水解
        ('艮', '兑'): 41,  # 山泽损
        ('巽', '震'): 42,  # 风雷益
        ('兑', '乾'): 43,  # 泽天夬
        ('乾', '巽'): 44,  # 天风姤
        ('兑', '坤'): 45,  # 泽地萃
        ('坤', '巽'): 46,  # 地风升
        ('兑', '坎'): 47,  # 泽水困
        ('坎', '巽'): 48,  # 水风井
        ('兑', '离'): 49,  # 泽火革
        ('离', '巽'): 50,  # 火风鼎
        ('震', '震'): 51,  # 震为雷
        ('艮', '艮'): 52,  # 艮为山
        ('巽', '艮'): 53,  # 风山渐
        ('震', '兑'): 54,  # 雷泽归妹
        ('震', '离'): 55,  # 雷火丰
        ('离', '艮'): 56,  # 火山旅
        ('巽', '巽'): 57,  # 巽为风
        ('兑', '兑'): 58,  # 兑为泽
        ('巽', '坎'): 59,  # 风水涣
        ('坎', '兑'): 60,  # 水泽节
        ('巽', '兑'): 61,  # 风泽中孚
        ('震', '艮'): 62,  # 雷山小过
        ('坎', '离'): 63,  # 水火既济
        ('离', '坎'): 64,  # 火水未济
    }
    
    def __init__(self, lines: List[int]):
        """
        初始化卦象
        
        Args:
            lines: 六爻列表，从下往上 [初爻，二爻，三爻，四爻，五爻，上爻]
                   数值：6=老阴，7=少阳，8=少阴，9=老阳
        """
        self.lines = lines
        self.name = ''
        self.number = 0
    
    def to_binary(self) -> str:
        """
        转换为二进制字符串（阳=1，阴=0）
        从下往上读
        """
        binary = ''
        for line in self.lines:
            if line in [7, 9]:  # 阳
                binary = '1' + binary
            else:  # 阴 (6, 8)
                binary = '0' + binary
        return binary
    
    def get_trigrams(self) -> tuple:
        """
        获取上下卦
        
        Returns:
            (上卦，下卦) 的八卦名
        """
        binary = self.to_binary()
        upper_bin = binary[:3]
        lower_bin = binary[3:]
        
        # 反向查找八卦名
        upper_name = [k for k, v in self.TRIGRAM_BINARY.items() if v == upper_bin][0]
        lower_name = [k for k, v in self.TRIGRAM_BINARY.items() if v == lower_bin][0]
        
        return upper_name, lower_name
    
    def get_hexagram_number(self) -> int:
        """
        获取六十四卦序号
        
        使用完整的 64 卦 (上卦，下卦) → 卦序号映射表
        基于《周易》标准卦序
        """
        upper, lower = self.get_trigrams()
        return self.HEXAGRAM_MAP.get((upper, lower), 1)
    
    def get_name(self) -> str:
        """获取卦名"""
        num = self.get_hexagram_number()
        return self.HEXAGRAM_NAMES.get(num, '未知卦')
    
    def display(self) -> str:
        """
        显示卦象（ASCII 艺术）
        """
        display_lines = []
        for line in reversed(self.lines):  # 从上往下显示
            if line in [7, 9]:  # 阳
                display_lines.append('───────')
            else:  # 阴
                display_lines.append('── ──')
        
        return '\n'.join(display_lines)
    
    def display_unicode(self) -> str:
        """
        使用 Unicode 符号显示卦象
        """
        upper, lower = self.get_trigrams()
        upper_sym = self.TRIGRAM_SYMBOLS.get(upper, '?')
        lower_sym = self.TRIGRAM_SYMBOLS.get(lower, '?')
        
        return f"{upper_sym}\n{lower_sym}"
    
    def get_changing_lines(self) -> List[int]:
        """
        获取变爻位置（动爻）
        
        Returns:
            变爻位置列表（从 1 开始计数）
        """
        changing = []
        for i, line in enumerate(self.lines):
            if line in [6, 9]:  # 老阴或老阳
                changing.append(i + 1)
        return changing


class HexagramCalculator:
    """
    卦象计算器
    
    负责：
    - 本卦计算
    - 变卦计算
    - 互卦计算
    """
    
    def __init__(self, lines: List[int]):
        """
        初始化计算器
        
        Args:
            lines: 六爻列表 [初爻，二爻，三爻，四爻，五爻，上爻]
        """
        self.original_lines = lines
        self.original_hexagram = Hexagram(lines)
    
    def get_original(self) -> Hexagram:
        """获取本卦（原始卦象）"""
        return self.original_hexagram
    
    def get_transformed_lines(self) -> List[int]:
        """
        获取变卦的六爻列表
        
        Returns:
            变卦的六爻列表
        """
        transformed_lines = []
        for line in self.original_lines:
            if line == 6:  # 老阴变阳
                transformed_lines.append(7)
            elif line == 9:  # 老阳变阴
                transformed_lines.append(8)
            else:  # 不变
                transformed_lines.append(line)
        return transformed_lines
    
    def get_transformed(self) -> Hexagram:
        """
        获取变卦（之卦）
        
        规则：老阴 (6) 变阳，老阳 (9) 变阴
        """
        transformed_lines = []
        for line in self.original_lines:
            if line == 6:  # 老阴变阳
                transformed_lines.append(7)
            elif line == 9:  # 老阳变阴
                transformed_lines.append(8)
            else:  # 不变
                transformed_lines.append(line)
        
        return Hexagram(transformed_lines)
    
    def get_mutual(self) -> Hexagram:
        """
        获取互卦
        
        规则：
        - 互卦下卦 = 本卦二三四爻
        - 互卦上卦 = 本卦三四五爻
        """
        # 重新组合为六爻（从下往上）
        mutual_lines = [
            self.original_lines[1],  # 初爻 = 原二爻
            self.original_lines[2],  # 二爻 = 原三爻
            self.original_lines[3],  # 三爻 = 原四爻
            self.original_lines[2],  # 四爻 = 原三爻
            self.original_lines[3],  # 五爻 = 原四爻
            self.original_lines[4],  # 上爻 = 原五爻
        ]
        
        return Hexagram(mutual_lines)
    
    def get_moving_lines(self) -> List[int]:
        """
        获取动爻位置
        
        Returns:
            动爻位置列表（从 1 开始）
        """
        moving = []
        for i, line in enumerate(self.original_lines):
            if line in [6, 9]:  # 老阴或老阳
                moving.append(i + 1)  # 从 1 开始计数
        return moving
    
    def display_all(self) -> str:
        """
        显示全部卦象（本卦、变卦、互卦）
        """
        original = self.get_original()
        transformed = self.get_transformed()
        mutual = self.get_mutual()
        moving = self.get_moving_lines()
        
        result = []
        result.append("=" * 40)
        result.append("【本卦】")
        result.append(original.display())
        result.append(f"卦名：{original.get_name()}")
        
        if moving:
            result.append(f"\n动爻：第{', '.join(map(str, moving))}爻")
        
        result.append("\n【变卦】")
        result.append(transformed.display())
        result.append(f"卦名：{transformed.get_name()}")
        
        result.append("\n【互卦】")
        result.append(mutual.display())
        result.append(f"卦名：{mutual.get_name()}")
        
        result.append("=" * 40)
        
        return '\n'.join(result)


# 测试代码
if __name__ == '__main__':
    print("=" * 50)
    print("周易卦象计算测试")
    print("=" * 50)
    
    # 测试：乾为天（全阳）
    print("\n【测试：乾为天】")
    qian_lines = [9, 9, 9, 9, 9, 9]
    calc = HexagramCalculator(qian_lines)
    print(calc.display_all())
    
    # 测试：坤为地（全阴）
    print("\n【测试：坤为地】")
    kun_lines = [6, 6, 6, 6, 6, 6]
    calc = HexagramCalculator(kun_lines)
    print(calc.display_all())
    
    # 测试：混合卦
    print("\n【测试：混合卦】")
    mixed_lines = [7, 8, 9, 6, 7, 8]
    calc = HexagramCalculator(mixed_lines)
    print(calc.display_all())
    
    print("\n" + "=" * 50)
