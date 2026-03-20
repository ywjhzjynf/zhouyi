# -*- coding: utf-8 -*-
"""
周易 64 卦卦名映射表
任务 ID: TASK-20260320-010
修复说明：完整的 64 卦卦名映射，包含卦序、卦名（单字）、全称
"""

# 64 卦卦名映射表 (卦序：卦名)
HEXAGRAM_NAMES = {
    1: "乾",
    2: "坤",
    3: "屯",
    4: "蒙",
    5: "需",
    6: "讼",
    7: "师",
    8: "比",
    9: "小畜",
    10: "履",
    11: "泰",
    12: "否",
    13: "同人",
    14: "大有",
    15: "谦",
    16: "豫",
    17: "随",
    18: "蛊",
    19: "临",
    20: "观",
    21: "噬嗑",
    22: "贲",
    23: "剥",
    24: "复",
    25: "无妄",
    26: "大畜",
    27: "颐",
    28: "大过",
    29: "坎",
    30: "离",
    31: "咸",
    32: "恒",
    33: "遁",
    34: "大壮",
    35: "晋",
    36: "明夷",
    37: "家人",
    38: "睽",
    39: "蹇",
    40: "解",
    41: "损",
    42: "益",
    43: "夬",
    44: "姤",
    45: "萃",
    46: "升",
    47: "困",
    48: "井",
    49: "革",
    50: "鼎",
    51: "震",
    52: "艮",
    53: "渐",
    54: "归妹",
    55: "丰",
    56: "旅",
    57: "巽",
    58: "兑",
    59: "涣",
    60: "节",
    61: "中孚",
    62: "小过",
    63: "既济",
    64: "未济",
}

# 64 卦全称映射表 (卦序：全称)
HEXAGRAM_FULL_NAMES = {
    1: "乾为天",
    2: "坤为地",
    3: "水雷屯",
    4: "山水蒙",
    5: "水天需",
    6: "天水讼",
    7: "地水师",
    8: "水地比",
    9: "风天小畜",
    10: "天泽履",
    11: "地天泰",
    12: "天地否",
    13: "天火同人",
    14: "火天大有",
    15: "地山谦",
    16: "雷地豫",
    17: "泽雷随",
    18: "山风蛊",
    19: "地泽临",
    20: "风地观",
    21: "火雷噬嗑",
    22: "山火贲",
    23: "山地剥",
    24: "地雷复",
    25: "天雷无妄",
    26: "山天大畜",
    27: "山雷颐",
    28: "泽风大过",
    29: "坎为水",
    30: "离为火",
    31: "泽山咸",
    32: "雷风恒",
    33: "天山遁",
    34: "雷天大壮",
    35: "火地晋",
    36: "地火明夷",
    37: "风火家人",
    38: "火泽睽",
    39: "水山蹇",
    40: "雷水解",
    41: "山泽损",
    42: "风雷益",
    43: "泽天夬",
    44: "天风姤",
    45: "泽地萃",
    46: "地风升",
    47: "泽水困",
    48: "水风井",
    49: "泽火革",
    50: "火风鼎",
    51: "震为雷",
    52: "艮为山",
    53: "风山渐",
    54: "雷泽归妹",
    55: "雷火丰",
    56: "火山旅",
    57: "巽为风",
    58: "兑为泽",
    59: "风水涣",
    60: "水泽节",
    61: "风泽中孚",
    62: "雷山小过",
    63: "水火既济",
    64: "火水未济",
}


def get_hexagram_name(order: int) -> str:
    """
    根据卦序获取卦名
    
    Args:
        order: 卦序 (1-64)
    
    Returns:
        卦名（单字或双字）
    
    Raises:
        ValueError: 卦序不在 1-64 范围内
    """
    if order < 1 or order > 64:
        raise ValueError(f"卦序必须在 1-64 范围内，当前为 {order}")
    return HEXAGRAM_NAMES.get(order, "")


def get_hexagram_full_name(order: int) -> str:
    """
    根据卦序获取卦的全称
    
    Args:
        order: 卦序 (1-64)
    
    Returns:
        卦的全称
    
    Raises:
        ValueError: 卦序不在 1-64 范围内
    """
    if order < 1 or order > 64:
        raise ValueError(f"卦序必须在 1-64 范围内，当前为 {order}")
    return HEXAGRAM_FULL_NAMES.get(order, "")


def get_hexagram_by_name(name: str) -> int:
    """
    根据卦名获取卦序
    
    Args:
        name: 卦名
    
    Returns:
        卦序 (1-64)，未找到返回 0
    """
    for order, hex_name in HEXAGRAM_NAMES.items():
        if hex_name == name:
            return order
    return 0


def validate_hexagram_table() -> dict:
    """
    验证卦名映射表的完整性
    
    Returns:
        验证结果字典
    """
    result = {
        "total": len(HEXAGRAM_NAMES),
        "expected": 64,
        "is_complete": len(HEXAGRAM_NAMES) == 64,
        "has_duplicates": len(HEXAGRAM_NAMES) != len(set(HEXAGRAM_NAMES.values())),
        "missing_orders": [],
        "duplicate_names": []
    }
    
    # 检查缺失的卦序
    for i in range(1, 65):
        if i not in HEXAGRAM_NAMES:
            result["missing_orders"].append(i)
    
    # 检查重复的卦名
    name_count = {}
    for name in HEXAGRAM_NAMES.values():
        name_count[name] = name_count.get(name, 0) + 1
    for name, count in name_count.items():
        if count > 1:
            result["duplicate_names"].append(name)
    
    result["is_valid"] = result["is_complete"] and not result["has_duplicates"]
    return result


if __name__ == "__main__":
    # 自检代码
    print("=== Zhouyi 64 Hexagram Validation ===")
    validation = validate_hexagram_table()
    print(f"Total: {validation['total']}/{validation['expected']}")
    print(f"Completeness: {'[OK]' if validation['is_complete'] else '[FAIL]'}")
    print(f"Duplicate Check: {'[OK]' if not validation['has_duplicates'] else '[FAIL]'}")
    print(f"Overall: {'[PASS]' if validation['is_valid'] else '[FAIL]'}")
    
    if validation["missing_orders"]:
        print(f"Missing orders: {validation['missing_orders']}")
    if validation["duplicate_names"]:
        print(f"Duplicate names: {validation['duplicate_names']}")
    
    # 示例查询
    print("\n=== Sample Queries ===")
    for i in [1, 2, 63, 64]:
        print(f"#{i}: {get_hexagram_name(i)} - {get_hexagram_full_name(i)}")
