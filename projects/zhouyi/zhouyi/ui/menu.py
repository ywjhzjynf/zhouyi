#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主菜单模块
Main Menu Module

提供交互式命令行菜单
"""

import sys
from pathlib import Path
from typing import Optional, Callable

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.calculator import CoinMethod, ShicaoMethod, NumberMethod, TimeMethod
from core.hexagram import HexagramCalculator
from ui.display import HexagramDisplay
from ui.history import HistoryManager


class MainMenu:
    """主菜单类"""
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.history = HistoryManager()
        self.running = True
    
    def display_header(self):
        """显示程序头部"""
        print("")
        print("╔" + "═" * 50 + "╗")
        print("║" + "周易占卜系统".center(50) + "║")
        print("║" + f"v{self.VERSION}".center(50) + "║")
        print("╠" + "═" * 50 + "╣")
        print("║  传承千年智慧  启迪现代人生            ║")
        print("╚" + "═" * 50 + "╝")
    
    def display_menu(self):
        """显示主菜单"""
        print("")
        print("┌──────────────────────────────────────────┐")
        print("│  【主菜单】                              │")
        print("├──────────────────────────────────────────┤")
        print("│  1. 铜钱起卦（金钱卦）                   │")
        print("│  2. 蓍草起卦（大衍之数）                 │")
        print("│  3. 数字起卦                             │")
        print("│  4. 时间起卦（梅花易数）                 │")
        print("│  5. 查看历史记录                         │")
        print("│  6. 统计信息                             │")
        print("├──────────────────────────────────────────┤")
        print("│  0. 退出系统                             │")
        print("└──────────────────────────────────────────┘")
    
    def coin_divination(self):
        """铜钱起卦流程"""
        print("")
        print("【铜钱起卦】")
        print("请心诚默念所问之事...")
        input("按回车开始抛掷铜钱...")
        
        print("")
        coin = CoinMethod()
        lines = []
        
        for i in range(6):
            result = coin.toss()
            lines.append(result)
            meaning = coin.get_line_meaning(result)
            pos = ['初', '二', '三', '四', '五', '上'][i]
            print(f"  第{pos}爻：{result} - {meaning}")
        
        # 计算卦象
        calc = HexagramCalculator(lines)
        transformed = calc.get_transformed_lines()
        
        # 显示卦象
        print(HexagramDisplay.display_ascii(lines, "本卦"))
        print("")
        print(HexagramDisplay.display_ascii(transformed, "变卦"))
        
        # 保存到历史记录
        self.history.add_record(
            method='铜钱',
            lines=lines,
            transformed_lines=transformed
        )
        
        input("\n按回车返回主菜单...")
    
    def shicao_divination(self):
        """蓍草起卦流程"""
        print("")
        print("【蓍草起卦】")
        print("大衍之数五十，其用四十有九...")
        print("请心诚默念所问之事...")
        input("按回车开始演算...")
        
        shicao = ShicaoMethod()
        lines = shicao.generate()
        
        print("")
        print("十八变完成，卦象如下：")
        print(HexagramDisplay.display_ascii(lines, "本卦"))
        
        # 计算变卦
        calc = HexagramCalculator(lines)
        transformed = calc.get_transformed_lines()
        print("")
        print(HexagramDisplay.display_ascii(transformed, "变卦"))
        
        # 保存到历史记录
        self.history.add_record(
            method='蓍草',
            lines=lines,
            transformed_lines=transformed
        )
        
        input("\n按回车返回主菜单...")
    
    def number_divination(self):
        """数字起卦流程"""
        print("")
        print("【数字起卦】")
        
        try:
            number = input("请输入任意数字：").strip()
            if not number:
                print("输入无效，返回主菜单")
                return
            
            num_method = NumberMethod()
            lines = num_method.generate(int(number))
            
            print("")
            print(f"数字 {number} 对应的卦象：")
            print(HexagramDisplay.display_ascii(lines, "本卦"))
            
            # 计算变卦
            calc = HexagramCalculator(lines)
            transformed = calc.get_transformed_lines()
            print("")
            print(HexagramDisplay.display_ascii(transformed, "变卦"))
            
            # 保存到历史记录
            self.history.add_record(
                method='数字',
                lines=lines,
                transformed_lines=transformed,
                question=f"数字：{number}"
            )
            
        except ValueError:
            print("请输入有效数字！")
        
        input("\n按回车返回主菜单...")
    
    def time_divination(self):
        """时间起卦流程"""
        print("")
        print("【时间起卦】（梅花易数）")
        print("以当前时间起卦...")
        
        time_method = TimeMethod()
        lines = time_method.generate()
        
        print("")
        print(HexagramDisplay.display_ascii(lines, "本卦"))
        
        # 计算变卦
        calc = HexagramCalculator(lines)
        transformed = calc.get_transformed_lines()
        print("")
        print(HexagramDisplay.display_ascii(transformed, "变卦"))
        
        # 保存到历史记录
        self.history.add_record(
            method='时间',
            lines=lines,
            transformed_lines=transformed
        )
        
        input("\n按回车返回主菜单...")
    
    def view_history(self):
        """查看历史记录"""
        print("")
        print("【历史记录】")
        
        records = self.history.get_records(limit=10)
        
        if not records:
            print("暂无历史记录")
        else:
            print(f"{'ID':<6} {'时间':<22} {'方法':<8} {'卦名':<12}")
            print("-" * 50)
            for record in records:
                timestamp = record['timestamp'][:16].replace('T', ' ')
                print(f"{record['id']:<6} {timestamp:<22} {record['method']:<8} {record['hexagram_name'] or '-':<12}")
        
        print("")
        print("提示：输入记录 ID 查看详情，或按回车返回")
        choice = input("请输入 ID：").strip()
        
        if choice.isdigit():
            record = self.history.get_record_by_id(int(choice))
            if record:
                print("")
                print(HexagramDisplay.display_ascii(record['lines'], "本卦"))
                if record['transformed_lines']:
                    print(HexagramDisplay.display_ascii(record['transformed_lines'], "变卦"))
                print(f"时间：{record['timestamp']}")
                print(f"方法：{record['method']}")
                if record['question']:
                    print(f"问题：{record['question']}")
        
        input("\n按回车返回主菜单...")
    
    def show_statistics(self):
        """显示统计信息"""
        print("")
        print("【统计信息】")
        
        stats = self.history.get_statistics()
        
        print(f"总占卜次数：{stats['total']}")
        print("")
        print("各方法使用次数：")
        for method, count in stats['methods'].items():
            print(f"  {method}: {count}次")
        
        input("\n按回车返回主菜单...")
    
    def run(self):
        """运行主循环"""
        while self.running:
            self.display_header()
            self.display_menu()
            
            choice = input("\n请选择 [0-6]: ").strip()
            
            if choice == '1':
                self.coin_divination()
            elif choice == '2':
                self.shicao_divination()
            elif choice == '3':
                self.number_divination()
            elif choice == '4':
                self.time_divination()
            elif choice == '5':
                self.view_history()
            elif choice == '6':
                self.show_statistics()
            elif choice == '0':
                print("\n感谢使用周易占卜系统，再会！")
                self.running = False
            else:
                print("\n无效选择，请重新输入")


def main():
    """主函数"""
    menu = MainMenu()
    menu.run()


if __name__ == '__main__':
    main()
