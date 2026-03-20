#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易算法移动端适配模块
Zhouyi Divination - Mobile API

版本：v2.0.0-mobile
"""

from .divination_api import (
    # 核心 API
    divine,
    divine_batch,
    benchmark,
    self_test,
    
    # 起卦方法类
    CoinMethod,
    ShicaoMethod,
    NumberMethod,
    TimeMethod,
    
    # 卦象计算类
    Hexagram,
    HexagramCalculator,
    
    # 常量
    TRIGRAM_BINARY,
    TRIGRAM_SYMBOLS,
    TRIGRAM_NUM_MAP,
    HEXAGRAM_NAMES,
    HEXAGRAM_MAP,
    LINE_MEANINGS,
)

__version__ = '2.0.0-mobile'
__all__ = [
    # 核心 API
    'divine',
    'divine_batch',
    'benchmark',
    'self_test',
    
    # 起卦方法类
    'CoinMethod',
    'ShicaoMethod',
    'NumberMethod',
    'TimeMethod',
    
    # 卦象计算类
    'Hexagram',
    'HexagramCalculator',
    
    # 常量
    'TRIGRAM_BINARY',
    'TRIGRAM_SYMBOLS',
    'TRIGRAM_NUM_MAP',
    'HEXAGRAM_NAMES',
    'HEXAGRAM_MAP',
    'LINE_MEANINGS',
]
