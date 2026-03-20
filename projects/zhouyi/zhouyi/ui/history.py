#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史记录管理模块
History Management Module

使用 SQLite 存储占卜历史记录
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class HistoryManager:
    """占卜历史记录管理器"""
    
    def __init__(self, db_path: str = None):
        """
        初始化历史记录管理器
        
        Args:
            db_path: 数据库文件路径，默认在项目 data 目录
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent / 'data' / 'divination_history.db'
        
        self.db_path = str(db_path)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS divinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                method TEXT NOT NULL,
                lines TEXT NOT NULL,
                transformed_lines TEXT,
                hexagram_name TEXT,
                question TEXT,
                note TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_record(self, method: str, lines: List[int], 
                   transformed_lines: Optional[List[int]] = None,
                   hexagram_name: str = "",
                   question: str = "",
                   note: str = "") -> int:
        """
        添加占卜记录
        
        Args:
            method: 起卦方法（铜钱/蓍草/数字/时间）
            lines: 六爻列表
            transformed_lines: 变卦六爻
            hexagram_name: 卦名
            question: 占问事项
            note: 备注
        
        Returns:
            记录 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO divinations 
            (timestamp, method, lines, transformed_lines, hexagram_name, question, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            method,
            json.dumps(lines),
            json.dumps(transformed_lines) if transformed_lines else None,
            hexagram_name,
            question,
            note
        ))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_records(self, limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        获取历史记录
        
        Args:
            limit: 返回记录数
            offset: 偏移量
        
        Returns:
            记录列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM divinations 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            record = {
                'id': row['id'],
                'timestamp': row['timestamp'],
                'method': row['method'],
                'lines': json.loads(row['lines']),
                'transformed_lines': json.loads(row['transformed_lines']) if row['transformed_lines'] else None,
                'hexagram_name': row['hexagram_name'],
                'question': row['question'],
                'note': row['note']
            }
            records.append(record)
        
        return records
    
    def get_record_by_id(self, record_id: int) -> Optional[Dict]:
        """
        根据 ID 获取记录
        
        Args:
            record_id: 记录 ID
        
        Returns:
            记录字典，不存在则返回 None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM divinations WHERE id = ?', (record_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'timestamp': row['timestamp'],
                'method': row['method'],
                'lines': json.loads(row['lines']),
                'transformed_lines': json.loads(row['transformed_lines']) if row['transformed_lines'] else None,
                'hexagram_name': row['hexagram_name'],
                'question': row['question'],
                'note': row['note']
            }
        return None
    
    def delete_record(self, record_id: int) -> bool:
        """
        删除记录
        
        Args:
            record_id: 记录 ID
        
        Returns:
            是否删除成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM divinations WHERE id = ?', (record_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def search_records(self, keyword: str) -> List[Dict]:
        """
        搜索记录
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的记录列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM divinations 
            WHERE question LIKE ? OR hexagram_name LIKE ? OR note LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            record = {
                'id': row['id'],
                'timestamp': row['timestamp'],
                'method': row['method'],
                'lines': json.loads(row['lines']),
                'transformed_lines': json.loads(row['transformed_lines']) if row['transformed_lines'] else None,
                'hexagram_name': row['hexagram_name'],
                'question': row['question'],
                'note': row['note']
            }
            records.append(record)
        
        return records
    
    def get_statistics(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            统计字典
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总记录数
        cursor.execute('SELECT COUNT(*) FROM divinations')
        total = cursor.fetchone()[0]
        
        # 各方法使用次数
        cursor.execute('''
            SELECT method, COUNT(*) as count 
            FROM divinations 
            GROUP BY method
        ''')
        methods = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total': total,
            'methods': methods
        }
    
    def clear_all(self) -> bool:
        """
        清空所有记录
        
        Returns:
            是否清空成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM divinations')
        conn.commit()
        conn.close()
        
        return True
