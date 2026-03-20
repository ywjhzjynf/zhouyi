"""
周易起卦算法模块
Zhouyi Divination - Hexagram Calculation Methods

包含四种传统起卦方法：
1. 铜钱起卦（金钱卦）
2. 蓍草起卦（大衍之数）
3. 数字起卦
4. 时间起卦（梅花易数）
"""

import random
from datetime import datetime
from typing import List, Tuple


class CoinMethod:
    """
    铜钱起卦法（金钱卦）
    
    方法：三枚铜钱抛掷六次，每次记录正反面
    - 正面（字）= 3，反面（花）= 2
    - 三枚总和：6=老阴，7=少阳，8=少阴，9=老阳
    """
    
    def __init__(self):
        self.lines = []
    
    def toss(self) -> int:
        """抛掷一次三枚铜钱，返回总和（6/7/8/9）"""
        coins = [random.choice([2, 3]) for _ in range(3)]
        return sum(coins)
    
    def generate(self) -> List[int]:
        """
        完整起卦流程：抛掷六次，从下往上记录
        返回：六爻列表 [初爻，二爻，三爻，四爻，五爻，上爻]
        """
        self.lines = []
        for i in range(6):
            result = self.toss()
            self.lines.append(result)
        return self.lines
    
    def get_line_meaning(self, value: int) -> str:
        """解释爻的含义"""
        meanings = {
            6: '老阴（变爻）',
            7: '少阳（不变）',
            8: '少阴（不变）',
            9: '老阳（变爻）'
        }
        return meanings.get(value, '未知')


class ShicaoMethod:
    """
    蓍草起卦法（大衍之数）
    
    方法：大衍之数五十，其用四十有九
    四营成易：分二、挂一、揲四、归奇
    三变成一爻，十八变成一卦
    """
    
    def __init__(self):
        self.lines = []
    
    def divide(self, stalks: int) -> Tuple[int, int, int]:
        """
        分二、挂一、揲四、归奇
        
        返回：左余数，右余数，挂一
        """
        # 分二：随机分成两份
        left = random.randint(1, stalks - 1)
        right = stalks - left
        
        # 挂一：从右边取一根
        right -= 1
        gui_yi = 1
        
        # 揲四：左右分别除以四取余
        left_remain = left % 4 if left % 4 != 0 else 4
        right_remain = right % 4 if right % 4 != 0 else 4
        
        return left_remain, right_remain, gui_yi
    
    def three_changes(self) -> int:
        """
        三变成一爻
        返回：24=6(老阴), 28=7(少阳), 32=8(少阴), 36=9(老阳)
        """
        stalks = 49
        
        for _ in range(3):  # 三变
            left_r, right_r, gui = self.divide(stalks)
            total_remain = left_r + right_r + gui
            stalks -= total_remain
        
        return stalks
    
    def generate(self) -> List[int]:
        """
        完整起卦流程：六爻，每爻三变
        返回：六爻列表 [初爻，二爻，三爻，四爻，五爻，上爻]
        """
        self.lines = []
        
        for i in range(6):
            result = self.three_changes()
            # 24=6, 28=7, 32=8, 36=9
            if result == 24:
                self.lines.append(6)  # 老阴
            elif result == 28:
                self.lines.append(7)  # 少阳
            elif result == 32:
                self.lines.append(8)  # 少阴
            elif result == 36:
                self.lines.append(9)  # 老阳
        
        return self.lines


class NumberMethod:
    """
    数字起卦法
    
    方法：用户输入数字，按规则转换为卦象
    - 上卦：数字除 8 取余
    - 下卦：数字除 8 取余（多位数则分段）
    - 动爻：数字除 6 取余
    """
    
    # 八卦二进制：1 乾 111, 2 兑 110, 3 离 101, 4 震 100, 5 巽 011, 6 坎 010, 7 艮 001, 8 坤 000
    TRIGRAM_BINARY = {
        1: '111', 2: '110', 3: '101', 4: '100',
        5: '011', 6: '010', 7: '001', 8: '000'
    }
    
    # 八卦对应名称
    TRIGRAM_MAP = {
        1: '乾', 2: '兑', 3: '离', 4: '震',
        5: '巽', 6: '坎', 7: '艮', 8: '坤'
    }
    
    def __init__(self):
        self.upper = 0
        self.lower = 0
        self.moving_line = 0
    
    def _trigram_to_lines(self, trigram_num: int) -> List[int]:
        """将八卦数转换为三爻（7=少阳，8=少阴）"""
        binary = self.TRIGRAM_BINARY[trigram_num]
        lines = []
        for bit in reversed(binary):  # 从下往上
            lines.append(7 if bit == '1' else 8)
        return lines
    
    def generate(self, number: int) -> List[int]:
        """
        根据数字生成六爻卦象
        
        Args:
            number: 用户输入的数字
        
        Returns:
            List[int]: 六爻列表 [初爻，二爻，三爻，四爻，五爻，上爻]
                       数值：6=老阴，7=少阳，8=少阴，9=老阳
        """
        # 上卦：除 8 取余（余 0 则为 8）
        self.upper = number % 8 if number % 8 != 0 else 8
        
        # 下卦：数字各位相加后除 8 取余
        digit_sum = sum(int(d) for d in str(abs(number)))
        self.lower = digit_sum % 8 if digit_sum % 8 != 0 else 8
        
        # 动爻：除 6 取余（余 0 则为 6）
        self.moving_line = number % 6 if number % 6 != 0 else 6
        
        # 转换为六爻：下卦（初 - 三爻）+ 上卦（四 - 上爻）
        lower_lines = self._trigram_to_lines(self.lower)
        upper_lines = self._trigram_to_lines(self.upper)
        lines = lower_lines + upper_lines
        
        # 将动爻设为老阳/老阴
        if self.moving_line <= 6:
            # 如果原爻是阳（7），变为老阳（9）；如果是阴（8），变为老阴（6）
            idx = self.moving_line - 1
            if lines[idx] == 7:
                lines[idx] = 9
            else:
                lines[idx] = 6
        
        return lines
    
    def get_trigram_info(self, number: int) -> dict:
        """获取卦象信息（兼容旧接口）"""
        self.generate(number)
        return {
            'upper': self.upper,
            'lower': self.lower,
            'moving': self.moving_line,
            'upper_name': self.TRIGRAM_MAP[self.upper],
            'lower_name': self.TRIGRAM_MAP[self.lower]
        }


class TimeMethod:
    """
    时间起卦法（梅花易数）
    
    方法：以年月日时数字起卦
    - 上卦：（年 + 月 + 日）除 8 取余
    - 下卦：（年 + 月 + 日 + 时）除 8 取余
    - 动爻：（年 + 月 + 日 + 时）除 6 取余
    """
    
    # 八卦二进制
    TRIGRAM_BINARY = {
        1: '111', 2: '110', 3: '101', 4: '100',
        5: '011', 6: '010', 7: '001', 8: '000'
    }
    
    # 八卦对应名称
    TRIGRAM_MAP = {
        1: '乾', 2: '兑', 3: '离', 4: '震',
        5: '巽', 6: '坎', 7: '艮', 8: '坤'
    }
    
    def __init__(self):
        self.upper = 0
        self.lower = 0
        self.moving_line = 0
    
    def _trigram_to_lines(self, trigram_num: int) -> List[int]:
        """将八卦数转换为三爻（7=少阳，8=少阴）"""
        binary = self.TRIGRAM_BINARY[trigram_num]
        lines = []
        for bit in reversed(binary):  # 从下往上
            lines.append(7 if bit == '1' else 8)
        return lines
    
    def generate(self, target_time: datetime = None) -> List[int]:
        """
        根据时间生成六爻卦象
        
        Args:
            target_time: 目标时间，None 则使用当前时间
        
        Returns:
            List[int]: 六爻列表 [初爻，二爻，三爻，四爻，五爻，上爻]
        """
        if target_time is None:
            target_time = datetime.now()
        
        # 地支数：子 1 丑 2 寅 3 卯 4 辰 5 巳 6 午 7 未 8 申 9 酉 10 戌 11 亥 12
        hour_branch = ((target_time.hour + 1) % 12) + 1
        
        # 年支数（简化：取年份后两位）
        year_num = target_time.year % 100
        
        # 上卦：（年 + 月 + 日）除 8 取余
        upper_sum = year_num + target_time.month + target_time.day
        self.upper = upper_sum % 8 if upper_sum % 8 != 0 else 8
        
        # 下卦：（年 + 月 + 日 + 时）除 8 取余
        lower_sum = upper_sum + hour_branch
        self.lower = lower_sum % 8 if lower_sum % 8 != 0 else 8
        
        # 动爻：（年 + 月 + 日 + 时）除 6 取余
        self.moving_line = lower_sum % 6 if lower_sum % 6 != 0 else 6
        
        # 转换为六爻：下卦（初 - 三爻）+ 上卦（四 - 上爻）
        lower_lines = self._trigram_to_lines(self.lower)
        upper_lines = self._trigram_to_lines(self.upper)
        lines = lower_lines + upper_lines
        
        # 将动爻设为老阳/老阴
        if self.moving_line <= 6:
            idx = self.moving_line - 1
            if lines[idx] == 7:
                lines[idx] = 9
            else:
                lines[idx] = 6
        
        return lines
    
    def get_time_info(self, target_time: datetime = None) -> dict:
        """获取时间卦象信息（兼容旧接口）"""
        if target_time is None:
            target_time = datetime.now()
        self.generate(target_time)
        return {
            'upper': self.upper,
            'lower': self.lower,
            'moving': self.moving_line,
            'time': target_time.strftime('%Y-%m-%d %H:%M:%S'),
            'upper_name': self.TRIGRAM_MAP[self.upper],
            'lower_name': self.TRIGRAM_MAP[self.lower]
        }


class DivinationCalculator:
    """
    周易起卦统一接口
    提供四种起卦方法的统一调用接口
    """
    
    def __init__(self):
        self.coin = CoinMethod()
        self.shicao = ShicaoMethod()
        self.number = NumberMethod()
        self.time = TimeMethod()
    
    def divinate(self, method: str, **kwargs):
        """
        统一占卜接口
        
        Args:
            method: 起卦方法 ('coin', 'yarrow', 'number', 'time')
            **kwargs: 额外参数（如 number 方法的 number 参数）
            
        Returns:
            dict: 包含 hexagram_id, lines, method 等信息
        """
        if method == 'coin':
            lines = self.coin.generate()
        elif method == 'yarrow':
            lines = self.shicao.generate()
        elif method == 'number':
            num = kwargs.get('number', 12345)
            lines = self._number_to_lines(num)
        elif method == 'time':
            lines = self.time.generate()
        else:
            raise ValueError(f"未知的起卦方法：{method}")
        
        # 计算卦象 ID
        hexagram_id = self._lines_to_id(lines)
        
        return {
            'method': method,
            'lines': lines,
            'hexagram_id': hexagram_id,
        }
    
    def _number_to_lines(self, number: int) -> List[int]:
        """将数字起卦结果转换为六爻"""
        # 直接调用 number 方法的 generate
        return self.number.generate(number)
    
    def _lines_to_id(self, lines: List[int]) -> int:
        """
        将六爻转换为卦象 ID
        
        Args:
            lines: 六爻列表 [初爻，二爻，三爻，四爻，五爻，上爻]
                   6/7/8/9 -> 0/1/0/1 (阴阳)
        
        Returns:
            卦象 ID (1-64)
        """
        # 将爻转换为二进制（阳=1，阴=0）
        binary = ''
        for line in lines:
            if line in [7, 9]:  # 阳爻
                binary = '1' + binary
            else:  # 阴爻 (6, 8)
                binary = '0' + binary
        
        # 二进制转十进制
        decimal = int(binary, 2)
        
        # 转换为 1-64 的 ID
        hex_id = decimal + 1
        
        return hex_id


# 测试代码
if __name__ == '__main__':
    print("=" * 50)
    print("周易起卦算法测试")
    print("=" * 50)
    
    # 测试铜钱起卦
    print("\n【铜钱起卦】")
    coin = CoinMethod()
    lines = coin.generate()
    for i, line in enumerate(lines):
        print(f"  第{i+1}爻：{line} - {coin.get_line_meaning(line)}")
    
    # 测试蓍草起卦
    print("\n【蓍草起卦】")
    shicao = ShicaoMethod()
    lines = shicao.generate()
    for i, line in enumerate(lines):
        print(f"  第{i+1}爻：{line} - {shicao.get_line_meaning(line) if hasattr(shicao, 'get_line_meaning') else ''}")
    
    # 测试数字起卦
    print("\n【数字起卦】")
    num = NumberMethod()
    result = num.generate(12345)
    print(f"  上卦：{result['upper_name']} ({result['upper']})")
    print(f"  下卦：{result['lower_name']} ({result['lower']})")
    print(f"  动爻：第{result['moving']}爻")
    
    # 测试时间起卦
    print("\n【时间起卦】")
    time = TimeMethod()
    result = time.generate()
    print(f"  时间：{result['time']}")
    print(f"  上卦：{result['upper']}")
    print(f"  下卦：{result['lower']}")
    print(f"  动爻：第{result['moving']}爻")
    
    print("\n" + "=" * 50)
