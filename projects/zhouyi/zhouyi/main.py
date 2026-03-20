#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易占卜系统
Zhouyi Divination System v1.0.0

主程序入口

功能：
- 铜钱起卦（金钱卦）
- 蓍草起卦（大衍之数）
- 数字起卦
- 时间起卦（梅花易数）
- 卦象解析
- 历史记录管理
"""

import sys
import io

# 设置 UTF-8 编码，避免 Windows 终端显示问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from ui.menu import MainMenu


def main():
    """主函数"""
    print("=" * 60)
    print("        周易占卜系统 v1.0.0 启动中...")
    print("=" * 60)
    
    try:
        menu = MainMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n系统已中断，感谢使用！")
    except Exception as e:
        print(f"\n发生错误：{e}")
        print("请检查系统配置或联系管理员")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
