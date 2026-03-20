#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易占卜历史记录模块
Zhouyi Divination - History Management

功能：
- 占卜记录保存（SQLite）
- 历史记录查询
- 记录删除与管理
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class DivinationHistory:
    """
    占卜历史管理器
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化数据库
        
        Args:
            db_path: 数据库文件路径，默认在项目 data 目录下
        """
        if db_path is None:
            # 默认数据库路径
            data_dir = Path(__file__).parent / 'data'
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / 'divination_history.db'
        
        self.db_path = Path(db_path)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # 创建占卜记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS divinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                method TEXT NOT NULL,
                lines TEXT NOT NULL,
                hexagram_name TEXT,
                transformed_name TEXT,
                mutual_name TEXT,
                moving_lines TEXT,
                question TEXT,
                notes TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON divinations(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_method ON divinations(method)')
        
        conn.commit()
        conn.close()
    
    def save_record(self, method: str, lines: List[int], 
                    hexagram_name: str = '', transformed_name: str = '',
                    mutual_name: str = '', moving_lines: List[int] = None,
                    question: str = '', notes: str = '') -> int:
        """
        保存占卜记录
        
        Args:
            method: 起卦方法（铜钱/蓍草/数字/时间）
            lines: 六爻列表
            hexagram_name: 本卦名称
            transformed_name: 变卦名称
            mutual_name: 互卦名称
            moving_lines: 动爻位置列表
            question: 所问之事
            notes: 备注
            
        Returns:
            记录 ID
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO divinations 
            (timestamp, method, lines, hexagram_name, transformed_name, 
             mutual_name, moving_lines, question, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            method,
            json.dumps(lines),
            hexagram_name,
            transformed_name,
            mutual_name,
            json.dumps(moving_lines or []),
            question,
            notes
        ))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_all_records(self, limit: int = 100) -> List[Dict]:
        """
        获取所有记录
        
        Args:
            limit: 返回记录数量限制
            
        Returns:
            记录列表
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM divinations 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        records = []
        for row in cursor.fetchall():
            record = dict(row)
            record['lines'] = json.loads(record['lines'])
            record['moving_lines'] = json.loads(record['moving_lines'])
            records.append(record)
        
        conn.close()
        return records
    
    def query_by_method(self, method: str) -> List[Dict]:
        """
        按起卦方法查询记录
        
        Args:
            method: 起卦方法
            
        Returns:
            记录列表
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM divinations 
            WHERE method = ?
            ORDER BY timestamp DESC
        ''', (method,))
        
        records = []
        for row in cursor.fetchall():
            record = dict(row)
            record['lines'] = json.loads(record['lines'])
            record['moving_lines'] = json.loads(record['moving_lines'])
            records.append(record)
        
        conn.close()
        return records
    
    def query_by_date(self, start_date: str, end_date: str = None) -> List[Dict]:
        """
        按日期范围查询记录
        
        Args:
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期，默认与开始日期相同
            
        Returns:
            记录列表
        """
        if end_date is None:
            end_date = start_date
        
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM divinations 
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp DESC
        ''', (start_date + ' 00:00:00', end_date + ' 23:59:59'))
        
        records = []
        for row in cursor.fetchall():
            record = dict(row)
            record['lines'] = json.loads(record['lines'])
            record['moving_lines'] = json.loads(record['moving_lines'])
            records.append(record)
        
        conn.close()
        return records
    
    def get_record_by_id(self, record_id: int) -> Optional[Dict]:
        """
        根据 ID 获取单条记录
        
        Args:
            record_id: 记录 ID
            
        Returns:
            记录字典或 None
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM divinations WHERE id = ?', (record_id,))
        row = cursor.fetchone()
        
        if row:
            record = dict(row)
            record['lines'] = json.loads(record['lines'])
            record['moving_lines'] = json.loads(record['moving_lines'])
        else:
            record = None
        
        conn.close()
        return record
    
    def delete_record(self, record_id: int) -> bool:
        """
        删除记录
        
        Args:
            record_id: 记录 ID
            
        Returns:
            是否删除成功
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM divinations WHERE id = ?', (record_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_statistics(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            统计字典
        """
        conn = sqlite3.connect(str(self.db_path))
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
        
        # 最近占卜时间
        cursor.execute('SELECT MAX(timestamp) FROM divinations')
        last_divination = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'methods': methods,
            'last_divination': last_divination
        }
    
    def clear_all(self) -> bool:
        """
        清空所有记录
        
        Returns:
            是否清空成功
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM divinations')
        conn.commit()
        
        count = cursor.rowcount
        conn.close()
        
        return count >= 0


def display_history_menu(history: DivinationHistory):
    """
    显示历史记录菜单
    
    Args:
        history: 历史记录管理器实例
    """
    while True:
        print("\n" + "=" * 50)
        print("        📜 历史记录管理")
        print("=" * 50)
        print("  1. 查看最近记录")
        print("  2. 按起卦方法查询")
        print("  3. 按日期查询")
        print("  4. 查看单条记录")
        print("  5. 查看统计信息")
        print("  6. 删除记录")
        print("  7. 清空所有记录")
        print("  0. 返回主菜单")
        print("=" * 50)
        
        choice = input("请选择：").strip()
        
        if choice == '1':
            # 查看最近记录
            limit = input("显示最近多少条记录？[10] ").strip()
            limit = int(limit) if limit.isdigit() else 10
            records = history.get_all_records(limit)
            display_records(records)
            
        elif choice == '2':
            # 按方法查询
            print("\n起卦方法：1.铜钱 2.蓍草 3.数字 4.时间")
            method_map = {'1': '铜钱', '2': '蓍草', '3': '数字', '4': '时间'}
            method_choice = input("请选择：").strip()
            method = method_map.get(method_choice, '铜钱')
            records = history.query_by_method(method)
            display_records(records)
            
        elif choice == '3':
            # 按日期查询
            start = input("开始日期（YYYY-MM-DD）：").strip()
            end = input("结束日期（YYYY-MM-DD，留空同开始日期）：").strip()
            if not end:
                end = None
            records = history.query_by_date(start, end)
            display_records(records)
            
        elif choice == '4':
            # 查看单条
            record_id = input("请输入记录 ID：").strip()
            if record_id.isdigit():
                record = history.get_record_by_id(int(record_id))
                if record:
                    display_single_record(record)
                else:
                    print("❌ 未找到该记录")
            else:
                print("❌ 无效的 ID")
                
        elif choice == '5':
            # 统计信息
            stats = history.get_statistics()
            print("\n📊 统计信息")
            print(f"  总记录数：{stats['total']}")
            print(f"  最后占卜：{stats['last_divination'] or '无'}")
            print("  各方法使用次数：")
            for method, count in stats['methods'].items():
                print(f"    {method}: {count}次")
                
        elif choice == '6':
            # 删除记录
            record_id = input("请输入要删除的记录 ID：").strip()
            if record_id.isdigit():
                confirm = input(f"确认删除记录 {record_id}？(y/n)：").strip().lower()
                if confirm == 'y':
                    if history.delete_record(int(record_id)):
                        print("✅ 删除成功")
                    else:
                        print("❌ 删除失败")
            else:
                print("❌ 无效的 ID")
                
        elif choice == '7':
            # 清空所有
            confirm = input("⚠️  确认清空所有历史记录？此操作不可恢复！(y/n)：").strip().lower()
            if confirm == 'y':
                if history.clear_all():
                    print("✅ 已清空所有记录")
                else:
                    print("❌ 清空失败")
                    
        elif choice == '0':
            break
        else:
            print("❌ 无效选择")


def display_records(records: List[Dict]):
    """
    显示记录列表
    
    Args:
        records: 记录列表
    """
    if not records:
        print("\n📭 暂无记录")
        return
    
    print(f"\n📜 共 {len(records)} 条记录")
    print("-" * 70)
    
    for record in records[:10]:  # 最多显示 10 条
        print(f"ID: {record['id']:3d} | {record['timestamp']} | {record['method']:4s} | "
              f"{record['hexagram_name']:8s} → {record['transformed_name']:8s}")
        if record['question']:
            print(f"       问：{record['question'][:40]}...")
    
    if len(records) > 10:
        print(f"       ... 还有 {len(records) - 10} 条记录，请查询查看")


def display_single_record(record: Dict):
    """
    显示单条记录详情
    
    Args:
        record: 记录字典
    """
    print("\n" + "=" * 60)
    print(f"📜 占卜记录 #{record['id']}")
    print("=" * 60)
    print(f"时间：{record['timestamp']}")
    print(f"方法：{record['method']}")
    print(f"所问：{record['question'] or '未记录'}")
    print(f"六爻：{record['lines']}")
    print(f"本卦：{record['hexagram_name']}")
    print(f"变卦：{record['transformed_name']}")
    print(f"互卦：{record['mutual_name']}")
    print(f"动爻：{record['moving_lines']}")
    if record['notes']:
        print(f"备注：{record['notes']}")
    print("=" * 60)


# 测试代码
if __name__ == '__main__':
    print("测试历史记录模块")
    history = DivinationHistory()
    
    # 保存测试记录
    test_id = history.save_record(
        method='铜钱',
        lines=[7, 8, 9, 6, 7, 8],
        hexagram_name='水火既济',
        transformed_name='火水未济',
        mutual_name='火水未济',
        moving_lines=[3, 4],
        question='测试问题',
        notes='测试备注'
    )
    print(f"保存测试记录，ID: {test_id}")
    
    # 查询记录
    records = history.get_all_records()
    print(f"共 {len(records)} 条记录")
    
    # 统计信息
    stats = history.get_statistics()
    print(f"统计：{stats}")
