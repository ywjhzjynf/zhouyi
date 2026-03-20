#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易占卜系统 - 移动版
Zhouyi Divination System - Mobile Version

基于 Flet 的 Android/iOS 移动应用
"""

import flet as ft
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.calculator import DivinationCalculator
from data import DataLoader


def main(page: ft.Page):
    """应用入口"""
    # 配置页面
    page.title = "周易占卜"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFF8E7"  # 米黄色背景
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    # 初始化组件
    calculator = DivinationCalculator()
    data_loader = DataLoader()
    
    # 结果展示文本
    result_text = ft.Text(
        "心诚则灵，请选择起卦方式...",
        size=16,
        color="#696969",
        text_align=ft.TextAlign.CENTER,
        width=400,
    )
    
    hexagram_display = ft.Container(
        visible=False,
        padding=ft.padding.all(20),
    )
    
    def display_result(hexagram_data, result):
        """显示卦象结果"""
        if not hexagram_data:
            result_text.value = "未找到卦象数据"
            result_text.color = "#FF0000"
            hexagram_display.visible = True
            page.update()
            return
        
        name = hexagram_data.get('name', '未知')
        pinyin = hexagram_data.get('pinyin', '')
        judgment = hexagram_data.get('judgment', '')
        image = hexagram_data.get('image', '')
        
        hexagram_display.content = ft.Column(
            controls=[
                ft.Text(
                    f"【{name}】{pinyin}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#8B4513",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"卦辞：{judgment}",
                    size=16,
                    color="#000000",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"象曰：{image}",
                    size=14,
                    color="#696969",
                    text_align=ft.TextAlign.CENTER,
                    italic=True,
                ),
            ],
            spacing=10,
        )
        hexagram_display.visible = True
        page.update()
    
    def perform_divination(method: str, number: int = None):
        """执行起卦"""
        try:
            # 显示加载提示
            page.snack_bar = ft.SnackBar(
                content=ft.Text("起卦中..."),
            )
            page.snack_bar.open = True
            page.update()
            
            # 调用核心算法
            if method == 'number' and number is not None:
                result = calculator.divinate(method=method, number=number)
            else:
                result = calculator.divinate(method=method)
            
            # 获取卦象信息
            hexagram_id = result['hexagram_id']
            hexagram_data = data_loader.get_hexagram(hexagram_id)
            
            # 显示结果
            display_result(hexagram_data, result)
            
        except Exception as ex:
            result_text.value = f"起卦失败：{str(ex)}"
            result_text.color = "#FF0000"
            hexagram_display.visible = True
            page.update()
    
    # 起卦按钮事件处理
    def coin_divination(e):
        perform_divination("coin")
    
    def yarrow_divination(e):
        perform_divination("yarrow")
    
    def time_divination(e):
        perform_divination("time")
    
    def number_divination(e):
        # 弹出数字输入对话框
        number_field = ft.TextField(
            label="请输入数字",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        def submit(e):
            try:
                number = int(number_field.value)
                dialog.open = False
                perform_divination("number", number=number)
            except ValueError:
                number_field.error_text = "请输入有效数字"
                page.update()
        
        def cancel(e):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("数字起卦"),
            content=ft.Column(
                controls=[
                    ft.Text("请输入一个数字用于起卦："),
                    number_field,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("取消", on_click=cancel),
                ft.TextButton("确定", on_click=submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def show_history(e):
        """显示历史记录"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text("历史记录功能开发中..."),
        )
        page.snack_bar.open = True
        page.update()
    
    # 构建界面
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "☯ 周易占卜",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#8B4513",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "传承千年智慧，启迪人生方向",
                    size=14,
                    color="#A0522D",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=5,
        ),
        padding=ft.padding.all(20),
        border_radius=10,
        bgcolor="#FFE4C4",
    )
    
    divination_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "选择起卦方式",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color="#8B4513",
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "🪙 铜钱起卦",
                            on_click=coin_divination,
                            style=ft.ButtonStyle(
                                bgcolor="#DEB887",
                                color="#000000",
                            ),
                        ),
                        ft.ElevatedButton(
                            "🌿 蓍草起卦",
                            on_click=yarrow_divination,
                            style=ft.ButtonStyle(
                                bgcolor="#DEB887",
                                color="#000000",
                            ),
                        ),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "🔢 数字起卦",
                            on_click=number_divination,
                            style=ft.ButtonStyle(
                                bgcolor="#DEB887",
                                color="#000000",
                            ),
                        ),
                        ft.ElevatedButton(
                            "⏰ 时间起卦",
                            on_click=time_divination,
                            style=ft.ButtonStyle(
                                bgcolor="#DEB887",
                                color="#000000",
                            ),
                        ),
                    ],
                    spacing=10,
                    wrap=True,
                ),
            ],
            spacing=15,
        ),
        padding=ft.padding.all(20),
        border_radius=10,
        bgcolor="#FFFFFF",
    )
    
    result_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "占卜结果",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color="#8B4513",
                ),
                ft.Divider(),
                result_text,
                hexagram_display,
            ],
            spacing=10,
        ),
        padding=ft.padding.all(20),
        border_radius=10,
        bgcolor="#FFFFFF",
        width=450,
    )
    
    history_button = ft.ElevatedButton(
        "📜 查看历史记录",
        on_click=show_history,
        style=ft.ButtonStyle(
            bgcolor="#D2B48C",
            color="#000000",
        ),
    )
    
    # 添加所有控件到页面
    page.add(
        header,
        divination_section,
        result_section,
        history_button,
    )


if __name__ == "__main__":
    ft.app(target=main)
