-- ============================================
-- CNKI 学术热点数据库表结构
-- ============================================

-- 1. 论文热榜主表（当前最新状态）
CREATE TABLE IF NOT EXISTS cnki_article_hotspot (
    file_id VARCHAR(256) PRIMARY KEY,
    title TEXT NOT NULL,
    source VARCHAR(256),
    pub_date DATE,
    pdsi_score DECIMAL(10,2),
    first_author VARCHAR(256),
    subject VARCHAR(64),
    title_link TEXT,
    author_link TEXT,
    navi_link TEXT,
    
    -- 周榜状态
    week_rank INT,
    week_pdsi DECIMAL(10,2),
    week_first_date DATE,
    week_last_date DATE,
    week_consecutive INT DEFAULT 0,
    week_total_days INT DEFAULT 0,
    week_status VARCHAR(32) DEFAULT 'new',  -- new/continuing/returning
    
    -- 月榜状态
    month_rank INT,
    month_pdsi DECIMAL(10,2),
    month_first_date DATE,
    month_last_date DATE,
    month_consecutive INT DEFAULT 0,
    month_total_days INT DEFAULT 0,
    month_status VARCHAR(32) DEFAULT 'new',
    
    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 热词榜主表（当前最新状态）
CREATE TABLE IF NOT EXISTS cnki_keyword_hotspot (
    keyword_id VARCHAR(64) PRIMARY KEY,
    keyword TEXT NOT NULL,
    
    -- 周榜状态
    week_rank INT,
    week_hot INT,
    week_rate INT,
    week_first_date DATE,
    week_last_date DATE,
    week_consecutive INT DEFAULT 0,
    week_total_days INT DEFAULT 0,
    week_status VARCHAR(32) DEFAULT 'new',
    week_related_words TEXT,
    week_similar_words TEXT,
    
    -- 月榜状态
    month_rank INT,
    month_hot INT,
    month_rate INT,
    month_first_date DATE,
    month_last_date DATE,
    month_consecutive INT DEFAULT 0,
    month_total_days INT DEFAULT 0,
    month_status VARCHAR(32) DEFAULT 'new',
    month_related_words TEXT,
    month_similar_words TEXT,
    
    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 论文热榜历史快照（每次抓取的记录）
CREATE TABLE IF NOT EXISTS cnki_article_history (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(256) NOT NULL,
    snapshot_date DATE NOT NULL,
    scope VARCHAR(32) NOT NULL,  -- 'week' or 'month'
    rank_position INT,
    pdsi_score DECIMAL(10,2),
    is_new BOOLEAN DEFAULT FALSE,
    is_returning BOOLEAN DEFAULT FALSE,
    is_dropped BOOLEAN DEFAULT FALSE,  -- 是否下榜
    
    UNIQUE(file_id, snapshot_date, scope)
);

-- 4. 热词榜历史快照（每次抓取的记录）
CREATE TABLE IF NOT EXISTS cnki_keyword_history (
    id SERIAL PRIMARY KEY,
    keyword_id VARCHAR(64) NOT NULL,
    keyword TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    scope VARCHAR(32) NOT NULL,  -- 'week' or 'month'
    rank_position INT,
    hot_value INT,
    rate_value INT,
    is_new BOOLEAN DEFAULT FALSE,
    is_returning BOOLEAN DEFAULT FALSE,
    is_dropped BOOLEAN DEFAULT FALSE,
    
    UNIQUE(keyword_id, snapshot_date, scope)
);

-- 5. 抓取任务日志
CREATE TABLE IF NOT EXISTS cnki_crawl_log (
    id SERIAL PRIMARY KEY,
    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scope VARCHAR(32),  -- week/month/all
    article_count INT DEFAULT 0,
    keyword_count INT DEFAULT 0,
    new_articles INT DEFAULT 0,
    returning_articles INT DEFAULT 0,
    dropped_articles INT DEFAULT 0,
    new_keywords INT DEFAULT 0,
    returning_keywords INT DEFAULT 0,
    dropped_keywords INT DEFAULT 0,
    status VARCHAR(32) DEFAULT 'success',
    error_message TEXT
);

-- 6. 网络搜索分析缓存
CREATE TABLE IF NOT EXISTS cnki_search_analysis (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    search_date DATE NOT NULL,
    search_query TEXT,
    search_results TEXT,  -- JSON 格式存储搜索结果
    analysis_summary TEXT,
    
    UNIQUE(keyword, search_date)
);

-- 索引优化
CREATE INDEX IF NOT EXISTS idx_article_week_rank ON cnki_article_hotspot(week_rank) WHERE week_rank IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_article_month_rank ON cnki_article_hotspot(month_rank) WHERE month_rank IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_article_week_status ON cnki_article_hotspot(week_status);
CREATE INDEX IF NOT EXISTS idx_article_month_status ON cnki_article_hotspot(month_status);
CREATE INDEX IF NOT EXISTS idx_article_week_consecutive ON cnki_article_hotspot(week_consecutive DESC);
CREATE INDEX IF NOT EXISTS idx_article_month_consecutive ON cnki_article_hotspot(month_consecutive DESC);

CREATE INDEX IF NOT EXISTS idx_keyword_week_rank ON cnki_keyword_hotspot(week_rank) WHERE week_rank IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_keyword_month_rank ON cnki_keyword_hotspot(month_rank) WHERE month_rank IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_keyword_week_status ON cnki_keyword_hotspot(week_status);
CREATE INDEX IF NOT EXISTS idx_keyword_month_status ON cnki_keyword_hotspot(month_status);

CREATE INDEX IF NOT EXISTS idx_article_history_date ON cnki_article_history(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_article_history_scope ON cnki_article_history(scope);
CREATE INDEX IF NOT EXISTS idx_keyword_history_date ON cnki_keyword_history(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_keyword_history_scope ON cnki_keyword_history(scope);

CREATE INDEX IF NOT EXISTS idx_crawl_log_time ON cnki_crawl_log(crawl_time DESC);

-- 视图：霸榜文章（连续上榜≥3 周）
CREATE OR REPLACE VIEW v_article_dominating AS
SELECT * FROM cnki_article_hotspot
WHERE week_consecutive >= 3 OR month_consecutive >= 3;

-- 视图：黑马新上榜
CREATE OR REPLACE VIEW v_article_newcomers AS
SELECT * FROM cnki_article_hotspot
WHERE week_status = 'new' OR month_status = 'new';

-- 视图：卷土重来
CREATE OR REPLACE VIEW v_article_returning AS
SELECT * FROM cnki_article_hotspot
WHERE week_status = 'returning' OR month_status = 'returning';

-- 视图：热词霸榜
CREATE OR REPLACE VIEW v_keyword_dominating AS
SELECT * FROM cnki_keyword_hotspot
WHERE week_consecutive >= 3 OR month_consecutive >= 3;
