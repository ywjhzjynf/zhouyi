#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卦象显示模块
Hexagram Display Module

提供美观的卦象 ASCII 艺术显示
"""

from typing import List, Dict, Optional


class HexagramDisplay:
    """卦象美化显示类"""
    
    # 八卦 Unicode 符号
    TRIGRAM_SYMBOLS = {
        '乾': '☰', '兑': '☱', '离': '☲', '震': '☳',
        '巽': '☴', '坎': '☵', '艮': '☶', '坤': '☷'
    }
    
    # 六十四卦 Unicode 符号（部分）
    HEXAGRAM_UNICODE = {
        1: '䷀', 2: '䷁', 3: '䷂', 4: '䷃',
        5: '䷄', 6: '䷅', 7: '䷆', 8: '䷇',
        9: '䷈', 10: '䷉', 11: '䷊', 12: '䷋',
        13: '䷌', 14: '䷍', 15: '䷎', 16: '䷏',
        17: '䷐', 18: '䷑', 19: '䷒', 20: '䷓',
        21: '䷔', 22: '䷕', 23: '䷖', 24: '䷗',
        25: '䷘', 26: '䷙', 27: '䷚', 28: '䷛',
        29: '䷜', 30: '䷝', 31: '䷞', 32: '䷟',
        33: '䷠', 34: '䷡', 35: '䷢', 36: '䷣',
        37: '䷤', 38: '䷥', 39: '䷦', 40: '䷧',
        41: '䷨', 42: '䷩', 43: '䷪', 44: '䷫',
        45: '䷬', 46: '䷭', 47: '䷮', 48: '䷯',
        49: '䷰', 50: '䷱', 51: '䷲', 52: '䷳',
        53: '䷴', 54: '䷵', 55: '䷶', 56: '䷷',
        57: '䷸', 58: '䷹', 59: '䷺', 60: '䷻',
        61: '䷼', 62: '䷽', 63: '䷾', 64: '䷿'
    }
    
    # 爻的 ASCII 表示
    LINE_YANG = '───────'  # 阳爻
    LINE_YIN = '── ──'     # 阴爻
    LINE_YANG_OLD = '──⊙──'  # 老阳（变爻）
    LINE_YIN_OLD = '──✕──'   # 老阴（变爻）
    
    @classmethod
    def display_ascii(cls, lines: List[int], title: str = "") -> str:
        """
        ASCII 艺术显示卦象
        
        Args:
            lines: 六爻列表 [初爻，二爻，三爻，四爻，五爻，上爻]
            title: 标题
        
        Returns:
            格式化后的字符串
        """
        result = []
        
        if title:
            result.append(f"╔{'═' * 40}╗")
            result.append(f"║{title.center(40)}║")
            result.append(f"╚{'═' * 40}╝")
            result.append("")
        
        # 从上往下显示（上爻→初爻）
        for i in range(5, -1, -1):
            line = lines[i]
            pos = i + 1
            
            if line == 7:  # 少阳
                line_str = cls.LINE_YANG
                label = f"  九{pos}  " if pos in [1, 2, 3, 4, 5] else f"  上九  "
            elif line == 8:  # 少阴
                line_str = cls.LINE_YIN
                label = f"  六{pos}  " if pos in [1, 2, 3, 4, 5] else f"  上六  "
            elif line == 9:  # 老阳（变爻）
                line_str = cls.LINE_YANG_OLD
                label = f"  九{pos}* " if pos in [1, 2, 3, 4, 5] else f"  上九* "
            else:  # 6 老阴（变爻）
                line_str = cls.LINE_YIN_OLD
                label = f"  六{pos}* " if pos in [1, 2, 3, 4, 5] else f"  上六* "
            
            result.append(f"  {pos} {line_str} {label}")
        
        return '\n'.join(result)
    
    @classmethod
    def display_unicode(cls, hexagram_num: int) -> str:
        """
        Unicode 卦象符号
        
        Args:
            hexagram_num: 六十四卦序号 (1-64)
        
        Returns:
            Unicode 卦象符号
        """
        return cls.HEXAGRAM_UNICODE.get(hexagram_num, '？')
    
    @classmethod
    def display_full(cls, lines: List[int], hexagram_name: str = "", 
                     judgment: str = "", image: str = "") -> str:
        """
        完整卦象显示（包含卦辞）
        
        Args:
            lines: 六爻列表
            hexagram_name: 卦名
            judgment: 卦辞
            image: 象辞
        
        Returns:
            完整格式化输出
        """
        result = []
        
        # 卦象标题
        result.append("")
        result.append("╔" + "═" * 48 + "╗")
        if hexagram_name:
            result.append("║" + f"【{hexagram_name}】".center(48) + "║")
        result.append("╠" + "═" * 48 + "╣")
        
        # 卦象 ASCII
        result.append("║" + " " * 48 + "║")
        for i in range(5, -1, -1):
            line = lines[i]
            if line == 7:
                line_str = cls.LINE_YANG
            elif line == 8:
                line_str = cls.LINE_YIN
            elif line == 9:
                line_str = cls.LINE_YANG_OLD
            else:
                line_str = cls.LINE_YIN_OLD
            
            pos_name = ['上', '五', '四', '三', '二', '初'][i]
            result.append("║" + f"  {pos_name}  {line_str}".ljust(48) + "║")
        
        result.append("║" + " " * 48 + "║")
        result.append("╠" + "═" * 48 + "╣")
        
        # 卦辞
        if judgment:
            result.append("║" + f"卦辞：{judgment}".ljust(48) + "║")
        if image:
            result.append("║" + f"象曰：{image}".ljust(48) + "║")
        
        result.append("╚" + "═" * 48 + "╝")
        result.append("")
        
        return '\n'.join(result)
    
    @classmethod
    def display_divination_result(cls, original_lines: List[int], 
                                   transformed_lines: Optional[List[int]] = None,
                                   hexagram_data: Optional[Dict] = None) -> str:
        """
        显示完整占卜结果
        
        Args:
            original_lines: 本卦六爻
            transformed_lines: 变卦六爻（可选）
            hexagram_data: 卦象数据（包含卦名、卦辞等）
        
        Returns:
            完整占卜结果字符串
        """
        result = []
        
        # 本卦
        if hexagram_data:
            result.append(cls.display_full(
                original_lines,
                hexagram_data.get('name', ''),
                hexagram_data.get('judgment', ''),
                hexagram_data.get('image', '')
            ))
        else:
            result.append(cls.display_ascii(original_lines, "本卦"))
        
        # 变卦
        if transformed_lines:
            result.append(cls.display_ascii(transformed_lines, "变卦"))
        
        # 动爻说明
        moving_lines = []
        for i, line in enumerate(original_lines):
            if line in [6, 9]:
                pos = ['初', '二', '三', '四', '五', '上'][i]
                moving_lines.append(f"{pos}爻")
        
        if moving_lines:
            result.append(f"动爻：{', '.join(moving_lines)}")
            result.append("")
            result.append("※ 变卦为事物发展趋势，本卦为当前状态")
        
        return '\n'.join(result)
