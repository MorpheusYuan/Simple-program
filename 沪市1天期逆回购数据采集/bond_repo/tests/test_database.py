import pytest
import sqlite3
from main import save_to_db, init_db
from database_manager import DatabaseManager

def test_save_to_db():
    # 初始化数据库
    db_manager = DatabaseManager()
    db_manager.init_db()

    # 测试数据
    test_data = ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"]

    # 保存数据
    assert save_to_db(test_data)

    # 验证数据是否保存
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bond_data")
        rows = cursor.fetchall()
        assert len(rows) > 0