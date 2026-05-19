#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNKI 热点数据库管理模块
负责数据库连接、数据对比、入库更新等操作
"""

import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple
import json


class CNKIDatabase:
    """CNKI 热点数据库管理类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.conn = None
        self.today = date.today()
    
    def connect(self) -> bool:
        """建立数据库连接"""
        try:
            db_config = self.config['database']
            self.conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password']
            )
            return True
        except Exception as e:
            print(f"数据库连接失败：{e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    # ==================== 论文数据处理 ====================
    
    def get_article_status(self, file_id: str) -> Optional[Dict[str, Any]]:
        """获取论文当前状态"""
        if not self.conn:
            return None
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM cnki_article_hotspot WHERE file_id = %s
            """, (file_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def update_article_hotspot(self, article: Dict[str, Any], scope: str):
        """更新或插入论文热榜数据"""
        if not self.conn:
            return
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # 检查是否已存在
            cur.execute("SELECT * FROM cnki_article_hotspot WHERE file_id = %s", (article['file_id'],))
            existing = cur.fetchone()
            
            if existing:
                # 更新现有记录
                self._update_existing_article(cur, article, scope, dict(existing))
            else:
                # 插入新记录
                self._insert_new_article(cur, article, scope)
    
    def _insert_new_article(self, cur, article: Dict[str, Any], scope: str):
        """插入新论文记录"""
        if scope == 'week':
            cur.execute("""
                INSERT INTO cnki_article_hotspot (
                    file_id, title, source, pub_date, pdsi_score, first_author, subject,
                    title_link, author_link, navi_link,
                    week_rank, week_pdsi, week_first_date, week_last_date,
                    week_consecutive, week_total_days, week_status,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (
                article['file_id'], article['title'], article['source'],
                article['pub_date'] or None, article['pdsi_score'],
                article['first_author'], article['subject'],
                article['title_link'], article['author_link'], article['navi_link'],
                article['rank'], article['pdsi_score'], self.today, self.today,
                1, 1, 'new'
            ))
        else:  # month
            cur.execute("""
                INSERT INTO cnki_article_hotspot (
                    file_id, title, source, pub_date, pdsi_score, first_author, subject,
                    title_link, author_link, navi_link,
                    month_rank, month_pdsi, month_first_date, month_last_date,
                    month_consecutive, month_total_days, month_status,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (
                article['file_id'], article['title'], article['source'],
                article['pub_date'] or None, article['pdsi_score'],
                article['first_author'], article['subject'],
                article['title_link'], article['author_link'], article['navi_link'],
                article['rank'], article['pdsi_score'], self.today, self.today,
                1, 1, 'new'
            ))
    
    def _update_existing_article(self, cur, article: Dict[str, Any], scope: str, existing: Dict[str, Any]):
        """更新现有论文记录"""
        if scope == 'week':
            # 判断状态
            if existing['week_rank'] is not None:
                # 持续在榜
                status = 'continuing'
                consecutive = (existing['week_consecutive'] or 0) + 1
                total_days = (existing['week_total_days'] or 0) + 7
            else:
                # 卷土重来
                status = 'returning'
                consecutive = 1
                total_days = (existing['week_total_days'] or 0) + 7
            
            cur.execute("""
                UPDATE cnki_article_hotspot SET
                    week_rank = %s, week_pdsi = %s, week_last_date = %s,
                    week_consecutive = %s, week_total_days = %s, week_status = %s,
                    updated_at = NOW()
                WHERE file_id = %s
            """, (
                article['rank'], article['pdsi_score'], self.today,
                consecutive, total_days, status,
                article['file_id']
            ))
        else:  # month
            if existing['month_rank'] is not None:
                status = 'continuing'
                consecutive = (existing['month_consecutive'] or 0) + 1
                total_days = (existing['month_total_days'] or 0) + 30
            else:
                status = 'returning'
                consecutive = 1
                total_days = (existing['month_total_days'] or 0) + 30
            
            cur.execute("""
                UPDATE cnki_article_hotspot SET
                    month_rank = %s, month_pdsi = %s, month_last_date = %s,
                    month_consecutive = %s, month_total_days = %s, month_status = %s,
                    updated_at = NOW()
                WHERE file_id = %s
            """, (
                article['rank'], article['pdsi_score'], self.today,
                consecutive, total_days, status,
                article['file_id']
            ))
    
    def mark_dropped_articles(self, current_file_ids: List[str], scope: str):
        """标记下榜的论文"""
        if not self.conn:
            return
        
        rank_field = f'{scope}_rank'
        status_field = f'{scope}_status'
        
        with self.conn.cursor() as cur:
            # 找出不在当前榜单中的论文
            if current_file_ids:
                placeholders = ','.join(['%s'] * len(current_file_ids))
                cur.execute(f"""
                    UPDATE cnki_article_hotspot SET
                        {rank_field} = NULL,
                        {status_field} = 'dropped',
                        updated_at = NOW()
                    WHERE {rank_field} IS NOT NULL AND file_id NOT IN ({placeholders})
                """, current_file_ids)
            else:
                # 如果当前榜单为空，标记所有为下榜
                cur.execute(f"""
                    UPDATE cnki_article_hotspot SET
                        {rank_field} = NULL,
                        {status_field} = 'dropped',
                        updated_at = NOW()
                    WHERE {rank_field} IS NOT NULL
                """)
    
    def record_article_history(self, articles: List[Dict[str, Any]], scope: str):
        """记录论文历史快照"""
        if not self.conn or not articles:
            return
        
        with self.conn.cursor() as cur:
            values = []
            for article in articles:
                # 获取当前状态
                existing = self.get_article_status(article['file_id'])
                is_new = existing is None
                is_returning = False
                if existing:
                    rank_field = f'{scope}_rank'
                    is_returning = existing.get(rank_field) is None
                
                values.append((
                    article['file_id'],
                    self.today,
                    scope,
                    article['rank'],
                    article['pdsi_score'],
                    is_new,
                    is_returning,
                    False
                ))
            
            execute_values(cur, """
                INSERT INTO cnki_article_history (
                    file_id, snapshot_date, scope, rank_position, pdsi_score,
                    is_new, is_returning, is_dropped
                ) VALUES %s
                ON CONFLICT (file_id, snapshot_date, scope) DO NOTHING
            """, values)
    
    # ==================== 热词数据处理 ====================
    
    def get_keyword_status(self, keyword_id: str) -> Optional[Dict[str, Any]]:
        """获取热词当前状态"""
        if not self.conn:
            return None
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM cnki_keyword_hotspot WHERE keyword_id = %s
            """, (keyword_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def update_keyword_hotspot(self, keyword: Dict[str, Any], scope: str):
        """更新或插入热词数据"""
        if not self.conn:
            return
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM cnki_keyword_hotspot WHERE keyword_id = %s", (keyword['keyword_id'],))
            existing = cur.fetchone()
            
            if existing:
                self._update_existing_keyword(cur, keyword, scope, dict(existing))
            else:
                self._insert_new_keyword(cur, keyword, scope)
    
    def _insert_new_keyword(self, cur, keyword: Dict[str, Any], scope: str):
        """插入新热词记录"""
        related_words = ','.join(keyword.get('related_words', '').split(';')[:10]) if keyword.get('related_words') else None
        similar_words = ','.join(keyword.get('similar_words', '').split(';')[:10]) if keyword.get('similar_words') else None
        
        if scope == 'week':
            cur.execute("""
                INSERT INTO cnki_keyword_hotspot (
                    keyword_id, keyword,
                    week_rank, week_hot, week_rate, week_first_date, week_last_date,
                    week_consecutive, week_total_days, week_status,
                    week_related_words, week_similar_words,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (
                keyword['keyword_id'], keyword['keyword'],
                int(keyword['keyword_id']) + 1, keyword['hot'], keyword['rate'],
                self.today, self.today, 1, 1, 'new',
                related_words, similar_words
            ))
        else:  # month
            cur.execute("""
                INSERT INTO cnki_keyword_hotspot (
                    keyword_id, keyword,
                    month_rank, month_hot, month_rate, month_first_date, month_last_date,
                    month_consecutive, month_total_days, month_status,
                    month_related_words, month_similar_words,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (
                keyword['keyword_id'], keyword['keyword'],
                int(keyword['keyword_id']) + 1, keyword['hot'], keyword['rate'],
                self.today, self.today, 1, 1, 'new',
                related_words, similar_words
            ))
    
    def _update_existing_keyword(self, cur, keyword: Dict[str, Any], scope: str, existing: Dict[str, Any]):
        """更新现有热词记录"""
        if scope == 'week':
            if existing['week_rank'] is not None:
                status = 'continuing'
                consecutive = (existing['week_consecutive'] or 0) + 1
                total_days = (existing['week_total_days'] or 0) + 7
            else:
                status = 'returning'
                consecutive = 1
                total_days = (existing['week_total_days'] or 0) + 7
            
            cur.execute("""
                UPDATE cnki_keyword_hotspot SET
                    week_rank = %s, week_hot = %s, week_rate = %s, week_last_date = %s,
                    week_consecutive = %s, week_total_days = %s, week_status = %s,
                    week_related_words = %s, week_similar_words = %s,
                    updated_at = NOW()
                WHERE keyword_id = %s
            """, (
                int(keyword['keyword_id']) + 1, keyword['hot'], keyword['rate'], self.today,
                consecutive, total_days, status,
                keyword.get('related_words'), keyword.get('similar_words'),
                keyword['keyword_id']
            ))
        else:  # month
            if existing['month_rank'] is not None:
                status = 'continuing'
                consecutive = (existing['month_consecutive'] or 0) + 1
                total_days = (existing['month_total_days'] or 0) + 30
            else:
                status = 'returning'
                consecutive = 1
                total_days = (existing['month_total_days'] or 0) + 30
            
            cur.execute("""
                UPDATE cnki_keyword_hotspot SET
                    month_rank = %s, month_hot = %s, month_rate = %s, month_last_date = %s,
                    month_consecutive = %s, month_total_days = %s, month_status = %s,
                    month_related_words = %s, month_similar_words = %s,
                    updated_at = NOW()
                WHERE keyword_id = %s
            """, (
                int(keyword['keyword_id']) + 1, keyword['hot'], keyword['rate'], self.today,
                consecutive, total_days, status,
                keyword.get('related_words'), keyword.get('similar_words'),
                keyword['keyword_id']
            ))
    
    def mark_dropped_keywords(self, current_keyword_ids: List[str], scope: str):
        """标记下榜的热词"""
        if not self.conn:
            return
        
        rank_field = f'{scope}_rank'
        status_field = f'{scope}_status'
        
        with self.conn.cursor() as cur:
            if current_keyword_ids:
                placeholders = ','.join(['%s'] * len(current_keyword_ids))
                cur.execute(f"""
                    UPDATE cnki_keyword_hotspot SET
                        {rank_field} = NULL,
                        {status_field} = 'dropped',
                        updated_at = NOW()
                    WHERE {rank_field} IS NOT NULL AND keyword_id NOT IN ({placeholders})
                """, current_keyword_ids)
            else:
                cur.execute(f"""
                    UPDATE cnki_keyword_hotspot SET
                        {rank_field} = NULL,
                        {status_field} = 'dropped',
                        updated_at = NOW()
                    WHERE {rank_field} IS NOT NULL
                """)
    
    def record_keyword_history(self, keywords: List[Dict[str, Any]], scope: str):
        """记录热词历史快照"""
        if not self.conn or not keywords:
            return
        
        with self.conn.cursor() as cur:
            values = []
            for keyword in keywords:
                existing = self.get_keyword_status(keyword['keyword_id'])
                is_new = existing is None
                is_returning = False
                if existing:
                    rank_field = f'{scope}_rank'
                    is_returning = existing.get(rank_field) is None
                
                values.append((
                    keyword['keyword_id'],
                    keyword['keyword'],
                    self.today,
                    scope,
                    int(keyword['keyword_id']) + 1,
                    keyword['hot'],
                    keyword['rate'],
                    is_new,
                    is_returning,
                    False
                ))
            
            execute_values(cur, """
                INSERT INTO cnki_keyword_history (
                    keyword_id, keyword, snapshot_date, scope, rank_position,
                    hot_value, rate_value, is_new, is_returning, is_dropped
                ) VALUES %s
                ON CONFLICT (keyword_id, snapshot_date, scope) DO NOTHING
            """, values)
    
    # ==================== 查询方法 ====================
    
    def get_top_articles(self, scope: str = 'week', limit: int = 10) -> List[Dict[str, Any]]:
        """获取 TOP 论文"""
        if not self.conn:
            return []
        
        rank_field = f'{scope}_rank'
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"""
                SELECT * FROM cnki_article_hotspot
                WHERE {rank_field} IS NOT NULL
                ORDER BY {rank_field}
                LIMIT %s
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]
    
    def get_top_keywords(self, scope: str = 'week', limit: int = 10) -> List[Dict[str, Any]]:
        """获取 TOP 热词"""
        if not self.conn:
            return []
        
        rank_field = f'{scope}_rank'
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"""
                SELECT * FROM cnki_keyword_hotspot
                WHERE {rank_field} IS NOT NULL
                ORDER BY {rank_field}
                LIMIT %s
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]
    
    def get_dominating_articles(self, min_consecutive: int = 3) -> List[Dict[str, Any]]:
        """获取霸榜论文"""
        if not self.conn:
            return []
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM cnki_article_hotspot
                WHERE week_consecutive >= %s OR month_consecutive >= %s
                ORDER BY GREATEST(week_consecutive, month_consecutive) DESC
            """, (min_consecutive, min_consecutive))
            return [dict(row) for row in cur.fetchall()]
    
    def get_newcomer_articles(self) -> List[Dict[str, Any]]:
        """获取新上榜论文"""
        if not self.conn:
            return []
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM cnki_article_hotspot
                WHERE week_status = 'new' OR month_status = 'new'
                ORDER BY COALESCE(week_rank, 999), COALESCE(month_rank, 999)
            """)
            return [dict(row) for row in cur.fetchall()]
    
    def get_returning_articles(self) -> List[Dict[str, Any]]:
        """获取卷土重来论文"""
        if not self.conn:
            return []
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM cnki_article_hotspot
                WHERE week_status = 'returning' OR month_status = 'returning'
                ORDER BY COALESCE(week_rank, 999), COALESCE(month_rank, 999)
            """)
            return [dict(row) for row in cur.fetchall()]
    
    def record_crawl_log(self, scope: str, stats: Dict[str, int], status: str = 'success', error_message: str = None):
        """记录抓取日志"""
        if not self.conn:
            return
        
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cnki_crawl_log (
                    scope, article_count, keyword_count,
                    new_articles, returning_articles, dropped_articles,
                    new_keywords, returning_keywords, dropped_keywords,
                    status, error_message
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                scope,
                stats.get('article_count', 0),
                stats.get('keyword_count', 0),
                stats.get('new_articles', 0),
                stats.get('returning_articles', 0),
                stats.get('dropped_articles', 0),
                stats.get('new_keywords', 0),
                stats.get('returning_keywords', 0),
                stats.get('dropped_keywords', 0),
                status,
                error_message
            ))
    
    def commit(self):
        """提交事务"""
        if self.conn:
            self.conn.commit()
    
    def rollback(self):
        """回滚事务"""
        if self.conn:
            self.conn.rollback()


if __name__ == '__main__':
    # 测试代码
    import json
    import os
    
    config_path = os.path.expanduser('~/.openclaw/skills/cnki-hotspot/config/config.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
        
        db = CNKIDatabase(config)
        if db.connect():
            print("数据库连接成功")
            
            # 测试查询
            top_articles = db.get_top_articles('week', 5)
            print(f"\n周榜 TOP5 论文:")
            for article in top_articles:
                print(f"  {article['week_rank']}. {article['title']}")
            
            db.close()
        else:
            print("数据库连接失败")
    else:
        print("配置文件不存在，请先初始化")
