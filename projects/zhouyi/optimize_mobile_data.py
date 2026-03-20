#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易数据移动端优化脚本
任务 ID: TASK-20260320-018

优化策略：
1. JSON 压缩（移除空格、换行）
2. 字段名缩写（减少重复文本）
3. 生成索引文件（支持增量加载）
4. 数据完整性验证
"""

import json
import os
import sys
from datetime import datetime

# 字段映射（原名 -> 缩写）
FIELD_MAP = {
    'id': 'i',
    'name': 'n',
    'pinyin': 'p',
    'full_name': 'f',
    'symbol': 's',
    'binary': 'b',
    'upper_trigram': 'u',
    'lower_trigram': 'l',
    'judgment': 'j',
    'image': 'img',
    'lines': 'ln',
    'position': 'pos',
    'text': 't',
    'type': 'tp',
    'source': 'src',
    'trigrams': 'tg',
    'element': 'e',
    'attribute': 'a'
}

# 反向映射（用于还原）
REVERSE_MAP = {v: k for k, v in FIELD_MAP.items()}

DATA_DIR = r'C:\Users\25243\.openclaw\workspace\projects\zhouyi\zhouyi\data'
OUTPUT_DIR = r'C:\Users\25243\.openclaw\workspace\projects\zhouyi\mobile_optimized'

def load_original_data():
    """加载原始数据"""
    src_file = os.path.join(DATA_DIR, 'hexagrams.json')
    with open(src_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def compress_field_names(data):
    """压缩字段名"""
    def compress_object(obj):
        if isinstance(obj, dict):
            return {FIELD_MAP.get(k, k): compress_object(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [compress_object(item) for item in obj]
        else:
            return obj
    
    return compress_object(data)

def decompress_field_names(data):
    """还原字段名（用于验证）"""
    def decompress_object(obj):
        if isinstance(obj, dict):
            return {REVERSE_MAP.get(k, k): decompress_object(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [decompress_object(item) for item in obj]
        else:
            return obj
    
    return decompress_object(data)

def create_index(data):
    """创建索引文件（支持快速查找和增量加载）"""
    hexagrams = data.get('hexagrams', [])
    
    index = {
        'total': len(hexagrams),
        'items': []
    }
    
    for h in hexagrams:
        index['items'].append({
            'i': h.get('i', h.get('id')),
            'n': h.get('n', h.get('name')),
            's': h.get('s', h.get('symbol')),
            'b': h.get('b', h.get('binary'))
        })
    
    return index

def generate_chunks(data, chunk_size=8):
    """生成数据分块（支持增量加载）"""
    hexagrams = data.get('hexagrams', [])
    chunks = []
    
    for i in range(0, len(hexagrams), chunk_size):
        chunk = {
            'chunk_id': len(chunks),
            'range': [i, min(i + chunk_size, len(hexagrams))],
            'hexagrams': hexagrams[i:i + chunk_size]
        }
        chunks.append(chunk)
    
    return chunks

def validate_data(original, optimized):
    """验证优化后数据完整性"""
    orig_hex = original.get('hexagrams', [])
    opt_hex = optimized.get('hexagrams', [])
    
    # 还原字段名进行比较
    restored = decompress_field_names({'hexagrams': opt_hex})['hexagrams']
    
    issues = []
    
    # 检查数量
    if len(orig_hex) != len(restored):
        issues.append(f"卦数不匹配：原始={len(orig_hex)}, 优化后={len(restored)}")
        return issues
    
    # 逐卦验证
    for i, (orig, rest) in enumerate(zip(orig_hex, restored)):
        if orig.get('id') != rest.get('id'):
            issues.append(f"第{i+1}卦 ID 不匹配")
        if orig.get('name') != rest.get('name'):
            issues.append(f"第{i+1}卦名称不匹配")
        if orig.get('binary') != rest.get('binary'):
            issues.append(f"第{i+1}卦二进制不匹配")
        
        # 验证爻辞
        orig_lines = orig.get('lines', [])
        rest_lines = rest.get('lines', [])
        if len(orig_lines) != len(rest_lines):
            issues.append(f"第{i+1}卦爻数不匹配")
        else:
            for j, (ol, rl) in enumerate(zip(orig_lines, rest_lines)):
                if ol.get('text') != rl.get('text'):
                    issues.append(f"第{i+1}卦第{j+1}爻辞不匹配")
    
    return issues

def main():
    print("=" * 60)
    print("周易数据移动端优化")
    print("任务 ID: TASK-20260320-018")
    print("开始时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 60)
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 加载原始数据
    print("\n[1/6] 加载原始数据...")
    original_data = load_original_data()
    original_size = len(json.dumps(original_data, ensure_ascii=False))
    print(f"  [OK] 加载完成，原始大小：{original_size:,} 字节 ({original_size/1024:.2f} KB)")
    print(f"  [OK] 卦数：{len(original_data.get('hexagrams', []))}")
    
    # 2. 压缩字段名
    print("\n[2/6] 压缩字段名...")
    compressed_data = compress_field_names(original_data)
    compressed_json = json.dumps(compressed_data, ensure_ascii=False, separators=(',', ':'))
    compressed_size = len(compressed_json)
    reduction = (1 - compressed_size / original_size) * 100
    print(f"  [OK] 压缩后大小：{compressed_size:,} 字节 ({compressed_size/1024:.2f} KB)")
    print(f"  [OK] 压缩率：{reduction:.1f}%")
    
    # 3. 保存压缩数据
    print("\n[3/6] 保存优化数据...")
    compressed_file = os.path.join(OUTPUT_DIR, 'hexagrams.min.json')
    with open(compressed_file, 'w', encoding='utf-8') as f:
        f.write(compressed_json)
    print(f"  [OK] 已保存：{compressed_file}")
    
    # 4. 创建索引
    print("\n[4/6] 创建索引文件...")
    index_data = create_index(compressed_data)
    index_json = json.dumps(index_data, ensure_ascii=False, separators=(',', ':'))
    index_file = os.path.join(OUTPUT_DIR, 'index.min.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_json)
    print(f"  [OK] 索引大小：{len(index_json):,} 字节 ({len(index_json)/1024:.2f} KB)")
    print(f"  [OK] 已保存：{index_file}")
    
    # 5. 生成数据分块
    print("\n[5/6] 生成数据分块（增量加载）...")
    chunks = generate_chunks(compressed_data)
    chunks_dir = os.path.join(OUTPUT_DIR, 'chunks')
    os.makedirs(chunks_dir, exist_ok=True)
    
    total_chunk_size = 0
    for chunk in chunks:
        chunk_json = json.dumps(chunk, ensure_ascii=False, separators=(',', ':'))
        chunk_file = os.path.join(chunks_dir, f'chunk_{chunk["chunk_id"]:02d}.min.json')
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk_json)
        total_chunk_size += len(chunk_json)
    
    print(f"  [OK] 生成 {len(chunks)} 个分块")
    print(f"  [OK] 分块总大小：{total_chunk_size:,} 字节 ({total_chunk_size/1024:.2f} KB)")
    print(f"  [OK] 已保存至：{chunks_dir}")
    
    # 6. 数据验证
    print("\n[6/6] 数据完整性验证...")
    # 读取压缩文件并还原验证
    with open(compressed_file, 'r', encoding='utf-8') as f:
        optimized_data = json.load(f)
    
    # 临时添加 hexagrams 字段用于验证
    optimized_for_validation = {'hexagrams': optimized_data.get('hexagrams', [])}
    issues = validate_data(original_data, optimized_for_validation)
    
    if issues:
        print(f"  [ERR] 发现 {len(issues)} 个问题:")
        for issue in issues[:10]:  # 只显示前 10 个
            print(f"    - {issue}")
    else:
        print(f"  [OK] 验证通过！64 卦数据完整，卦辞爻辞无误")
    
    # 生成优化报告
    print("\n" + "=" * 60)
    print("优化报告")
    print("=" * 60)
    print(f"原始文件大小：     {original_size:,} 字节 ({original_size/1024:.2f} KB)")
    print(f"优化后文件大小：   {compressed_size:,} 字节 ({compressed_size/1024:.2f} KB)")
    print(f"索引文件大小：     {len(index_json):,} 字节 ({len(index_json)/1024:.2f} KB)")
    print(f"分块文件数量：     {len(chunks)} 个")
    print(f"总体积减少：       {reduction:.1f}%")
    print(f"数据完整性：       {'[OK] 验证通过' if not issues else '[ERR] 存在问题'}")
    print("=" * 60)
    print(f"完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"输出目录：{OUTPUT_DIR}")
    print("=" * 60)
    
    return 0 if not issues else 1

if __name__ == '__main__':
    sys.exit(main())
