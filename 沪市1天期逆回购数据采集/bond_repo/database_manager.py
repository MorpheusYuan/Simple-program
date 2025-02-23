import sqlite3
from config import CONFIG
from logger import logger

class DatabaseManager:
    def __init__(self):
        self.is_test_mode = CONFIG['test_mode']['enabled']  # 直接读取配置
        self.db_path = self._get_db_path()
        
    def _get_db_path(self):
        """获取数据库路径"""
        if self.is_test_mode:
            logger.info("当前处于测试模式，数据将保存到测试数据库")
            return CONFIG['test_mode']['db_path']
        logger.info("当前处于正式模式，数据将保存到正式数据库")
        return CONFIG['db_path']
        
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
        
    def init_db(self):
        """初始化数据库"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS bond_data (
            timestamp DATETIME PRIMARY KEY,
            current_price REAL,
            open_price REAL,
            close_price REAL,
            high_price REAL,
            low_price REAL,
            bid_price REAL,
            ask_price REAL,
            deal_amount REAL,
            buy_amount REAL,
            sell_amount REAL
        )
        """
        with self.get_connection() as conn:
            conn.execute(create_table_sql)
            conn.commit()