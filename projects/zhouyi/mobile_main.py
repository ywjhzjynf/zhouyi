#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易占卜系统 - Kivy 移动端版本
Zhouyi Divination System - Kivy Mobile Version v1.0.0

适配 Android 手机的触摸界面
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
import random
from datetime import datetime

# 设置窗口大小为手机屏幕比例
Window.size = (360, 640)

# ==================== 核心算法（复用现有代码）====================

class CoinMethod:
    """铜钱起卦法"""
    
    def toss(self):
        """抛掷一次三枚铜钱，返回总和（6/7/8/9）"""
        coins = [random.choice([2, 3]) for _ in range(3)]
        return sum(coins)
    
    def generate(self):
        """抛掷六次，从下往上记录"""
        lines = []
        for i in range(6):
            result = self.toss()
            lines.append(result)
        return lines
    
    def get_line_meaning(self, value):
        """解释爻的含义"""
        meanings = {
            6: '老阴（变爻）',
            7: '少阳（不变）',
            8: '少阴（不变）',
            9: '老阳（变爻）'
        }
        return meanings.get(value, '未知')


class ShicaoMethod:
    """蓍草起卦法"""
    
    def divide(self, stalks):
        """分二、挂一、揲四、归奇"""
        left = random.randint(1, stalks - 1)
        right = stalks - left
        right -= 1
        gui_yi = 1
        left_remain = left % 4 if left % 4 != 0 else 4
        right_remain = right % 4 if right % 4 != 0 else 4
        return left_remain, right_remain, gui_yi
    
    def three_changes(self):
        """三变成一爻"""
        stalks = 49
        for _ in range(3):
            left_r, right_r, gui = self.divide(stalks)
            total_remain = left_r + right_r + gui
            stalks -= total_remain
        return stalks
    
    def generate(self):
        """完整起卦流程"""
        lines = []
        for i in range(6):
            result = self.three_changes()
            if result == 24:
                lines.append(6)
            elif result == 28:
                lines.append(7)
            elif result == 32:
                lines.append(8)
            elif result == 36:
                lines.append(9)
        return lines


class NumberMethod:
    """数字起卦法"""
    
    TRIGRAM_BINARY = {
        1: '111', 2: '110', 3: '101', 4: '100',
        5: '011', 6: '010', 7: '001', 8: '000'
    }
    
    def _trigram_to_lines(self, trigram_num):
        """将八卦数转换为三爻"""
        binary = self.TRIGRAM_BINARY[trigram_num]
        lines = []
        for bit in reversed(binary):
            lines.append(7 if bit == '1' else 8)
        return lines
    
    def generate(self, number):
        """根据数字生成六爻卦象"""
        upper = number % 8 if number % 8 != 0 else 8
        digit_sum = sum(int(d) for d in str(abs(number)))
        lower = digit_sum % 8 if digit_sum % 8 != 0 else 8
        moving_line = number % 6 if number % 6 != 0 else 6
        
        lower_lines = self._trigram_to_lines(lower)
        upper_lines = self._trigram_to_lines(upper)
        lines = lower_lines + upper_lines
        
        if moving_line <= 6:
            idx = moving_line - 1
            if lines[idx] == 7:
                lines[idx] = 9
            else:
                lines[idx] = 6
        
        return lines


class TimeMethod:
    """时间起卦法"""
    
    TRIGRAM_BINARY = {
        1: '111', 2: '110', 3: '101', 4: '100',
        5: '011', 6: '010', 7: '001', 8: '000'
    }
    
    def _trigram_to_lines(self, trigram_num):
        """将八卦数转换为三爻"""
        binary = self.TRIGRAM_BINARY[trigram_num]
        lines = []
        for bit in reversed(binary):
            lines.append(7 if bit == '1' else 8)
        return lines
    
    def generate(self):
        """根据当前时间生成卦象"""
        target_time = datetime.now()
        hour_branch = ((target_time.hour + 1) % 12) + 1
        year_num = target_time.year % 100
        
        upper_sum = year_num + target_time.month + target_time.day
        upper = upper_sum % 8 if upper_sum % 8 != 0 else 8
        
        lower_sum = upper_sum + hour_branch
        lower = lower_sum % 8 if lower_sum % 8 != 0 else 8
        
        moving_line = lower_sum % 6 if lower_sum % 6 != 0 else 6
        
        lower_lines = self._trigram_to_lines(lower)
        upper_lines = self._trigram_to_lines(upper)
        lines = lower_lines + upper_lines
        
        if moving_line <= 6:
            idx = moving_line - 1
            if lines[idx] == 7:
                lines[idx] = 9
            else:
                lines[idx] = 6
        
        return lines


# ==================== 卦象显示 ====================

HEXAGRAM_NAMES = {
    '111111': '乾为天', '000000': '坤为地', '100010': '水雷屯',
    '010001': '山水蒙', '111010': '水天需', '010111': '天水讼',
    '010000': '地水师', '000010': '水地比', '111011': '风天小畜',
    '110111': '天泽履', '000111': '地天泰', '111000': '天地否',
    '111101': '天火同人', '101111': '火天大有', '001000': '地山谦',
    '000100': '雷地豫', '100110': '泽雷随', '011001': '山风蛊',
    '110000': '地泽临', '000011': '风地观', '100101': '火雷噬嗑',
    '101001': '山火贲', '000001': '山地剥', '100000': '地雷复',
    '100111': '天雷无妄', '111001': '山天大畜', '100001': '山雷颐',
    '011110': '泽风大过', '010010': '坎为水', '101101': '离为火',
    '001110': '泽山咸', '011100': '雷风恒', '001111': '天山遁',
    '111100': '雷天大壮', '000101': '火地晋', '101000': '地火明夷',
    '101011': '风火家人', '110101': '火泽睽', '001010': '水山蹇',
    '010100': '雷水解', '011000': '山泽损', '000110': '风雷益',
    '111110': '泽天夬', '011111': '天风姤', '001100': '泽地萃',
    '001100': '地风升', '010110': '泽水困', '011010': '水风井',
    '101110': '泽火革', '011101': '火风鼎', '100100': '震为雷',
    '001001': '艮为山', '001011': '风山渐', '110100': '雷泽归妹',
    '001011': '雷火丰', '110100': '火山旅', '011011': '巽为风',
    '110110': '兑为泽', '010111': '风水涣', '111010': '水泽节',
    '110011': '风泽中孚', '001100': '雷山小过', '101010': '水火既济',
    '010101': '火水未济'
}


def lines_to_binary(lines):
    """将爻线转换为二进制字符串"""
    binary = ''
    for line in reversed(lines):  # 从上往下
        if line in [7, 9]:  # 阳爻
            binary += '1'
        else:  # 阴爻
            binary += '0'
    return binary


def get_hexagram_name(lines):
    """获取卦名"""
    binary = lines_to_binary(lines)
    return HEXAGRAM_NAMES.get(binary, '未知卦')


# ==================== UI 界面 ====================

class MainScreen(Screen):
    """主菜单屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 标题
        title = Label(
            text='周易占卜系统',
            font_size='24sp',
            size_hint=(1, 0.2),
            bold=True
        )
        
        subtitle = Label(
            text='v1.0.0 手机版',
            font_size='14sp',
            size_hint=(1, 0.1)
        )
        
        # 菜单按钮
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.6))
        
        self.coin_btn = Button(
            text='🪙 铜钱起卦',
            font_size='18sp',
            size_hint=(1, 0.2)
        )
        self.coin_btn.bind(on_press=self.go_coin)
        
        self.shicao_btn = Button(
            text='🌿 蓍草起卦',
            font_size='18sp',
            size_hint=(1, 0.2)
        )
        self.shicao_btn.bind(on_press=self.go_shicao)
        
        self.number_btn = Button(
            text='🔢 数字起卦',
            font_size='18sp',
            size_hint=(1, 0.2)
        )
        self.number_btn.bind(on_press=self.go_number)
        
        self.time_btn = Button(
            text='⏰ 时间起卦',
            font_size='18sp',
            size_hint=(1, 0.2)
        )
        self.time_btn.bind(on_press=self.go_time)
        
        btn_layout.add_widget(self.coin_btn)
        btn_layout.add_widget(self.shicao_btn)
        btn_layout.add_widget(self.number_btn)
        btn_layout.add_widget(self.time_btn)
        
        # 底部
        footer = Label(
            text='传承千年智慧  启迪现代人生',
            font_size='12sp',
            size_hint=(1, 0.1)
        )
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(btn_layout)
        layout.add_widget(footer)
        
        self.add_widget(layout)
    
    def go_coin(self, instance):
        self.manager.current = 'coin'
    
    def go_shicao(self, instance):
        self.manager.current = 'shicao'
    
    def go_number(self, instance):
        self.manager.current = 'number'
    
    def go_time(self, instance):
        self.manager.current = 'time'


class CoinScreen(Screen):
    """铜钱起卦屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.title_label = Label(
            text='铜钱起卦',
            font_size='20sp',
            size_hint=(1, 0.1),
            bold=True
        )
        
        self.instruction = Label(
            text='请心诚默念所问之事',
            font_size='14sp',
            size_hint=(1, 0.1)
        )
        
        self.result_label = Label(
            text='',
            font_size='14sp',
            size_hint=(1, 0.4),
            halign='left',
            valign='top'
        )
        
        self.toss_btn = Button(
            text='🎲 抛掷铜钱',
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        self.toss_btn.bind(on_press=self.toss)
        
        self.back_btn = Button(
            text='返回主菜单',
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        self.back_btn.bind(on_press=self.go_back)
        
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.instruction)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.toss_btn)
        self.layout.add_widget(self.back_btn)
        
        self.add_widget(self.layout)
        
        self.coin = CoinMethod()
        self.toss_count = 0
        self.lines = []
    
    def toss(self, instance):
        if self.toss_count < 6:
            result = self.coin.toss()
            pos = ['初', '二', '三', '四', '五', '上'][self.toss_count]
            meaning = self.coin.get_line_meaning(result)
            self.lines.append(result)
            self.result_label.text += f"第{pos}爻：{result} - {meaning}\n"
            self.toss_count += 1
            
            if self.toss_count == 6:
                self.show_result()
        else:
            self.toss_count = 0
            self.lines = []
            self.result_label.text = ''
            self.toss_btn.text = '🎲 抛掷铜钱'
    
    def show_result(self):
        name = get_hexagram_name(self.lines)
        self.result_label.text += f"\n【{name}】"
        self.toss_btn.text = '重新起卦'
    
    def go_back(self, instance):
        self.toss_count = 0
        self.lines = []
        self.result_label.text = ''
        self.toss_btn.text = '🎲 抛掷铜钱'
        self.manager.current = 'main'


class ShicaoScreen(Screen):
    """蓍草起卦屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text='蓍草起卦',
            font_size='20sp',
            size_hint=(1, 0.1),
            bold=True
        )
        
        instruction = Label(
            text='大衍之数五十，其用四十有九',
            font_size='14sp',
            size_hint=(1, 0.1)
        )
        
        self.result_label = Label(
            text='',
            font_size='14sp',
            size_hint=(1, 0.4),
            halign='left',
            valign='top'
        )
        
        self.start_btn = Button(
            text='开始演算',
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        self.start_btn.bind(on_press=self.start)
        
        back_btn = Button(
            text='返回主菜单',
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(instruction)
        layout.add_widget(self.result_label)
        layout.add_widget(self.start_btn)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
        self.shicao = ShicaoMethod()
        self.is_calculating = False
    
    def start(self, instance):
        if not self.is_calculating:
            self.is_calculating = True
            self.start_btn.text = '演算中...'
            self.result_label.text = '十八变演算中...\n'
            
            # 模拟演算过程
            def calculate(dt):
                lines = self.shicao.generate()
                for i, line in enumerate(lines):
                    pos = ['初', '二', '三', '四', '五', '上'][i]
                    self.result_label.text += f"第{pos}爻：{line}\n"
                
                name = get_hexagram_name(lines)
                self.result_label.text += f"\n【{name}】"
                self.start_btn.text = '重新起卦'
                self.is_calculating = False
            
            Clock.schedule_once(calculate, 0.5)
    
    def go_back(self, instance):
        self.result_label.text = ''
        self.start_btn.text = '开始演算'
        self.is_calculating = False
        self.manager.current = 'main'


class NumberScreen(Screen):
    """数字起卦屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text='数字起卦',
            font_size='20sp',
            size_hint=(1, 0.1),
            bold=True
        )
        
        instruction = Label(
            text='请输入任意数字',
            font_size='14sp',
            size_hint=(1, 0.1)
        )
        
        self.number_input = Button(
            text='点击输入数字',
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        
        self.result_label = Label(
            text='',
            font_size='14sp',
            size_hint=(1, 0.3),
            halign='left',
            valign='top'
        )
        
        self.calc_btn = Button(
            text='起卦',
            font_size='18sp',
            size_hint=(1, 0.15),
            disabled=True
        )
        self.calc_btn.bind(on_press=self.calculate)
        
        back_btn = Button(
            text='返回主菜单',
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(instruction)
        layout.add_widget(self.number_input)
        layout.add_widget(self.result_label)
        layout.add_widget(self.calc_btn)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
        self.number_method = NumberMethod()
        self.number_value = None
    
    def calculate(self, instance):
        if self.number_value:
            lines = self.number_method.generate(self.number_value)
            self.result_label.text = f'输入数字：{self.number_value}\n\n'
            for i, line in enumerate(lines):
                pos = ['初', '二', '三', '四', '五', '上'][i]
                self.result_label.text += f"第{pos}爻：{line}\n"
            
            name = get_hexagram_name(lines)
            self.result_label.text += f"\n【{name}】"


class TimeScreen(Screen):
    """时间起卦屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text='时间起卦',
            font_size='20sp',
            size_hint=(1, 0.1),
            bold=True
        )
        
        subtitle = Label(
            text='梅花易数',
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        
        self.time_label = Label(
            text='',
            font_size='14sp',
            size_hint=(1, 0.1)
        )
        
        self.result_label = Label(
            text='',
            font_size='14sp',
            size_hint=(1, 0.3),
            halign='left',
            valign='top'
        )
        
        self.start_btn = Button(
            text='以当前时间起卦',
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        self.start_btn.bind(on_press=self.start)
        
        back_btn = Button(
            text='返回主菜单',
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        back_btn.bind(on_press=self.go_back)
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(self.time_label)
        layout.add_widget(self.result_label)
        layout.add_widget(self.start_btn)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
        self.time_method = TimeMethod()
    
    def on_enter(self):
        self.time_label.text = datetime.now().strftime('%Y年%m月%d日 %H:%M')
    
    def start(self, instance):
        lines = self.time_method.generate()
        self.result_label.text = f'起卦时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n'
        for i, line in enumerate(lines):
            pos = ['初', '二', '三', '四', '五', '上'][i]
            self.result_label.text += f"第{pos}爻：{line}\n"
        
        name = get_hexagram_name(lines)
        self.result_label.text += f"\n【{name}】"
    
    def go_back(self, instance):
        self.result_label.text = ''
        self.manager.current = 'main'


# ==================== 主程序 ====================

class ZhouyiApp(App):
    """周易占卜 App"""
    
    def build(self):
        self.title = '周易占卜'
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CoinScreen(name='coin'))
        sm.add_widget(ShicaoScreen(name='shicao'))
        sm.add_widget(NumberScreen(name='number'))
        sm.add_widget(TimeScreen(name='time'))
        
        return sm


if __name__ == '__main__':
    ZhouyiApp().run()
