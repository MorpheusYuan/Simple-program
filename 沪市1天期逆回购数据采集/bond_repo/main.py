import requests
import sqlite3
import datetime
import time
from config import CONFIG
from trading_days import TradingDayChecker
from utils import ScheduleManager
import sys

def create_connection():
    """创建数据库连接"""
    return sqlite3.connect(CONFIG['db_path'])

def init_db():
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
        deal_amount INTEGER,
        buy_amount INTEGER,
        sell_amount INTEGER
    )
    """
    with create_connection() as conn:
        conn.execute(create_table_sql)
        conn.commit()

def fetch_data():
    """从新浪API获取数据"""
    for attempt in range(CONFIG['retry_times']):
        try:
            print(f"正在请求API... 尝试次数：{attempt + 1}")
            response = requests.get(
                CONFIG['api_url'],
                headers=CONFIG['headers'],
                timeout=CONFIG['timeout']
            )
            response.encoding = 'gbk'  # 新浪API使用GBK编码
            
            # 打印状态码用于调试
            print(f"HTTP状态码：{response.status_code}")
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"API请求失败，状态码：{response.status_code}")
                time.sleep(1)  # 等待1秒后重试
                continue
                
            # 打印原始响应用于调试
            print("API响应内容：", response.text)
            
            # 更健壮的解析方式
            if '="' not in response.text:
                print("API返回格式异常")
                continue
                
            data_str = response.text.split('="')[1].strip('";\n')
            data = data_str.split(',')
            
            # 验证数据完整性
            if len(data) < 10:
                print(f"数据字段不足，实际获取字段数：{len(data)}")
                continue
                
            return data
            
        except Exception as e:
            print(f"数据获取失败: {str(e)}")
            time.sleep(1)  # 等待1秒后重试
            
    return None

def save_to_db(data):
    """保存数据到数据库"""
    insert_sql = """
    INSERT INTO bond_data VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_data = (timestamp,) + tuple(data[:10])
    
    try:
        with create_connection() as conn:
            conn.execute(insert_sql, db_data)
            conn.commit()
        print(f"{timestamp} 数据保存成功")
        return True
    except sqlite3.IntegrityError:
        print("重复数据，跳过保存")
        return False

def main_loop():
    """主循环"""
    init_db()  # 初始化数据库
    
    while True:
        # 检查是否在交易时间
        if not ScheduleManager.is_trading_time():
            print("当前不在交易时间，程序结束")
            break
            
        # 采集数据
        raw_data = fetch_data()
        if raw_data and len(raw_data) >= 10:
            save_to_db(raw_data)
        else:
            print("获取到无效数据，等待重试")
            
        # 等待到下一分钟
        ScheduleManager.wait_until_next_minute()

if __name__ == "__main__":
    print("程序启动")
    
    # 检查是否为交易日
    if not TradingDayChecker.is_trading_day():
        print(f"{datetime.date.today()} 不是交易日，程序正常结束")
        sys.exit(0)
        
    try:
        main_loop()
    except KeyboardInterrupt:
        print("程序被手动终止")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
    finally:
        print("程序结束")