"""
SQLite 数据库管理
"""
import sqlite3
import os

DATABASE_PATH = "podcasts.db"

def get_db_connection():
    """
    获取数据库连接
    
    返回:
        sqlite3.Connection: 数据库连接对象
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 允许通过列名访问
    return conn

def init_db():
    """
    初始化数据库
    
    创建 episodes 表（如果不存在）
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建 episodes 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            audio_path TEXT NOT NULL,
            image_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f"✅ 数据库已初始化: {DATABASE_PATH}")

def reset_db():
    """
    重置数据库（删除并重新创建）
    
    警告：这会删除所有数据！
    """
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f"🗑️  数据库已删除: {DATABASE_PATH}")
    
    init_db()
    print("✅ 数据库已重置")

if __name__ == "__main__":
    # 测试数据库初始化
    init_db()

