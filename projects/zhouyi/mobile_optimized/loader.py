#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易移动端数据加载模块
任务 ID: TASK-20260320-018

功能：
- 支持全量加载
- 支持增量加载（分块）
- 提供字段名还原功能
- 缓存管理
"""

import json
import os
from typing import Dict, List, Optional, Any

# 字段映射（缩写 -> 原名）
FIELD_MAP_REVERSE = {
    'i': 'id',
    'n': 'name',
    'p': 'pinyin',
    'f': 'full_name',
    's': 'symbol',
    'b': 'binary',
    'u': 'upper_trigram',
    'l': 'lower_trigram',
    'j': 'judgment',
    'img': 'image',
    'ln': 'lines',
    'pos': 'position',
    't': 'text',
    'tp': 'type',
    'src': 'source',
    'tg': 'trigrams',
    'e': 'element',
    'a': 'attribute'
}


class ZhouyiDataLoader:
    """周易数据加载器"""
    
    def __init__(self, data_dir: str):
        """
        初始化加载器
        
        Args:
            data_dir: 优化后数据目录路径
        """
        self.data_dir = data_dir
        self.cache = {}
        self.index = None
        self.full_data = None
    
    def _expand_fields(self, obj: Any) -> Any:
        """还原字段名"""
        if isinstance(obj, dict):
            return {FIELD_MAP_REVERSE.get(k, k): self._expand_fields(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._expand_fields(item) for item in obj]
        else:
            return obj
    
    def load_full(self, expand: bool = True) -> Dict:
        """
        加载完整数据
        
        Args:
            expand: 是否还原字段名（默认 True）
        
        Returns:
            完整数据字典
        """
        if 'full' in self.cache:
            data = self.cache['full']
        else:
            file_path = os.path.join(self.data_dir, 'hexagrams.min.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.cache['full'] = data
        
        if expand:
            return self._expand_fields(data)
        return data
    
    def load_index(self) -> Dict:
        """
        加载索引文件
        
        Returns:
            索引数据
        """
        if self.index:
            return self.index
        
        file_path = os.path.join(self.data_dir, 'index.min.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            self.index = json.load(f)
        
        return self.index
    
    def load_chunk(self, chunk_id: int, expand: bool = True) -> Dict:
        """
        加载指定分块数据
        
        Args:
            chunk_id: 分块 ID (0-7)
            expand: 是否还原字段名
        
        Returns:
            分块数据
        """
        cache_key = f'chunk_{chunk_id}'
        if cache_key in self.cache:
            data = self.cache[cache_key]
        else:
            file_path = os.path.join(self.data_dir, 'chunks', f'chunk_{chunk_id:02d}.min.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.cache[cache_key] = data
        
        if expand:
            return self._expand_fields(data)
        return data
    
    def load_hexagram(self, hex_id: int, expand: bool = True) -> Optional[Dict]:
        """
        加载单个卦的数据
        
        Args:
            hex_id: 卦 ID (1-64)
            expand: 是否还原字段名
        
        Returns:
            卦数据，如不存在返回 None
        """
        # 计算所属分块
        chunk_id = (hex_id - 1) // 8
        
        chunk_data = self.load_chunk(chunk_id, expand=False)
        hexagrams = chunk_data.get('hexagrams', [])
        
        for h in hexagrams:
            if h.get('i') == hex_id:
                if expand:
                    return self._expand_fields(h)
                return h
        
        return None
    
    def load_range(self, start: int, end: int, expand: bool = True) -> List[Dict]:
        """
        加载指定范围的卦数据
        
        Args:
            start: 起始 ID（包含）
            end: 结束 ID（包含）
            expand: 是否还原字段名
        
        Returns:
            卦数据列表
        """
        result = []
        for hex_id in range(start, end + 1):
            h = self.load_hexagram(hex_id, expand)
            if h:
                result.append(h)
        return result
    
    def preload_all_chunks(self) -> int:
        """
        预加载所有分块到缓存
        
        Returns:
            加载的分块数量
        """
        index = self.load_index()
        total_chunks = (index['total'] + 7) // 8
        
        for i in range(total_chunks):
            self.load_chunk(i)
        
        return total_chunks
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        self.index = None


# 便捷函数
def create_loader(data_dir: str) -> ZhouyiDataLoader:
    """创建加载器实例"""
    return ZhouyiDataLoader(data_dir)


def demo():
    """使用示例"""
    # 假设数据目录
    data_dir = r'C:\Users\25243\.openclaw\workspace\projects\zhouyi\mobile_optimized'
    
    loader = create_loader(data_dir)
    
    # 示例 1: 加载索引
    print("=== 加载索引 ===")
    index = loader.load_index()
    print(f"总卦数：{index['total']}")
    print(f"前 5 卦：{index['items'][:5]}")
    
    # 示例 2: 加载单个卦
    print("\n=== 加载第 1 卦（乾卦）===")
    qian = loader.load_hexagram(1)
    print(f"卦名：{qian['name']}")
    print(f"卦辞：{qian['judgment']}")
    print(f"象曰：{qian['image']}")
    print(f"爻辞：{[line['text'] for line in qian['lines']]}")
    
    # 示例 3: 加载范围
    print("\n=== 加载前 8 卦（乾至泰）===")
    first_8 = loader.load_range(1, 8)
    print(f"卦名列表：{[h['name'] for h in first_8]}")
    
    # 示例 4: 增量加载
    print("\n=== 增量加载演示 ===")
    for i in range(8):
        chunk = loader.load_chunk(i, expand=False)
        range_info = chunk['range']
        print(f"分块 {i}: 卦 {range_info[0]+1}-{range_info[1]}")
    
    print("\n[OK] 演示完成")


if __name__ == '__main__':
    demo()
