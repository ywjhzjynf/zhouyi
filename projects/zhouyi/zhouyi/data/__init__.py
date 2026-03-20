#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据加载模块
Data Loader Module
"""

import json
from pathlib import Path


class DataLoader:
    """周易数据加载器"""
    
    def __init__(self, data_path: str = None):
        """初始化数据加载器
        
        Args:
            data_path: 数据文件路径，默认使用 hexagrams.json
        """
        if data_path is None:
            # 默认数据路径
            self.data_path = Path(__file__).parent / "hexagrams.json"
        else:
            self.data_path = Path(data_path)
        
        # 缓存加载的数据
        self._hexagrams = None
        self._hexagram_map = None
    
    def _load_data(self):
        """加载数据文件"""
        if self._hexagrams is None:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._hexagrams = data.get('hexagrams', [])
                
                # 创建卦名映射
                self._hexagram_map = {}
                for h in self._hexagrams:
                    hex_id = h.get('id')
                    name = h.get('name')
                    binary = h.get('binary')
                    
                    if hex_id:
                        self._hexagram_map[hex_id] = h
                    if name:
                        self._hexagram_map[name] = h
                    if binary:
                        self._hexagram_map[binary] = h
    
    def get_hexagram(self, hex_id: int):
        """根据 ID 获取卦象
        
        Args:
            hex_id: 卦象 ID (1-64)
            
        Returns:
            卦象数据字典，不存在则返回 None
        """
        self._load_data()
        return self._hexagram_map.get(hex_id)
    
    def get_hexagram_by_name(self, name: str):
        """根据卦名获取卦象
        
        Args:
            name: 卦名（如"乾"）
            
        Returns:
            卦象数据字典
        """
        self._load_data()
        return self._hexagram_map.get(name)
    
    def get_hexagram_by_binary(self, binary: str):
        """根据二进制获取卦象
        
        Args:
            binary: 二进制字符串（如"111111"）
            
        Returns:
            卦象数据字典
        """
        self._load_data()
        return self._hexagram_map.get(binary)
    
    def get_all_hexagrams(self):
        """获取所有卦象
        
        Returns:
            卦象列表
        """
        self._load_data()
        return self._hexagrams
    
    def search_hexagram(self, keyword: str):
        """搜索卦象
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的卦象列表
        """
        self._load_data()
        results = []
        for h in self._hexagrams:
            if (keyword in h.get('name', '') or 
                keyword in h.get('pinyin', '') or
                keyword in h.get('judgment', '')):
                results.append(h)
        return results


# 测试
if __name__ == "__main__":
    loader = DataLoader()
    
    # 测试获取乾卦
    qian = loader.get_hexagram(1)
    print(f"乾卦：{qian}")
    
    # 测试获取所有卦象数量
    all_hex = loader.get_all_hexagrams()
    print(f"总卦数：{len(all_hex)}")
