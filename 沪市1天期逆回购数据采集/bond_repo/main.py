import sys
import logging
from logger import logger

try:
    logger.info("日志系统初始化开始")
except:
    # 如果日志系统初始化失败，使用基本日志配置
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.warning("使用备用日志配置")

# 全局异常处理
def handle_exception(exc_type, exc_value, exc_traceback):
    """处理未捕获的异常"""
    if issubclass(exc_type, KeyboardInterrupt):
        logger.info("程序被手动中断")
        sys.exit(0)
    logger.error("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

logger.info("日志系统初始化完成")

import requests
import sqlite3
import datetime
import time
from config import CONFIG
from trading_days import TradingDayChecker
from utils import ScheduleManager
from data_validator import DataValidator
from database_manager import DatabaseManager

# 初始化数据库管理器
db_manager = DatabaseManager()

def init_db():
    """初始化数据库"""
    db_manager.init_db()

def fetch_data():
    """从新浪API获取数据"""
    for attempt in range(CONFIG['retry_times']):
        try:
            logger.debug(f"正在请求API... 尝试次数：{attempt + 1}")
            response = requests.get(
                CONFIG['api_url'],
                headers=CONFIG['headers'],
                timeout=CONFIG['timeout']
            )
            response.encoding = 'gbk'
            
            logger.debug(f"HTTP状态码：{response.status_code}")
            
            if response.status_code != 200:
                logger.warning(f"API请求失败，状态码：{response.status_code}")
                time.sleep(1)
                continue
                
            logger.debug("API响应内容：" + response.text)
            
            if '="' not in response.text:
                logger.warning("API返回格式异常")
                continue
                
            data_str = response.text.split('="')[1].strip('";\n')
            data = data_str.split(',')
            
            # 数据验证
            is_valid, message = DataValidator.validate(data)
            if not is_valid:
                logger.error(f"数据验证失败: {message}")
                logger.debug(f"原始数据: {data}")
                continue
                
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求失败: {str(e)}", exc_info=True)
            time.sleep(1)
        except Exception as e:
            logger.error(f"数据获取失败: {str(e)}", exc_info=True)
            time.sleep(1)
            
    logger.error("数据获取重试次数用尽")
    return None

def save_to_db(data):
    """保存数据到数据库"""
    insert_sql = """
    INSERT INTO bond_data VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_data = (timestamp,) + tuple(data[:11])  # 包含证券代码
    
    try:
        with db_manager.get_connection() as conn:
            conn.execute(insert_sql, db_data)
            conn.commit()
        logger.info(f"{timestamp} 数据保存成功")
        return True
    except sqlite3.IntegrityError:
        logger.warning("重复数据，跳过保存")
        return False
    except sqlite3.Error as e:
        logger.error(f"数据库操作失败: {str(e)}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"保存数据时发生未知错误: {str(e)}", exc_info=True)
        return False

def main_loop():
    """主循环"""
    init_db()  # 初始化数据库
    
    # 初始化统计变量
    start_time = time.time()
    data_count = 0
    api_request_count = 0
    
     # 如果是交易日，等待到交易时间
    if TradingDayChecker.is_trading_day():
        logger.info("当前是交易日，等待到交易时间...")
        while not ScheduleManager.is_trading_time():
            time.sleep(30)  # 每30秒检查一次
    else:
        logger.info(f"{datetime.date.today()} 不是交易日，程序正常结束")
        return

    while True:
        # 检查是否在交易时间
        if not ScheduleManager.is_trading_time():
            # 如果是午休时间（11:30-13:00），等待到下午开盘
            if ScheduleManager.is_midday_break():
                logger.info("当前是午休时间，等待到下午开盘...")
                ScheduleManager.wait_until_afternoon()
                continue
            else:
                # 交易日结束（15:30 后），记录汇总日志
                if ScheduleManager.is_trading_day():
                    running_time = time.time() - start_time
                    logger.info(
                        f"当日汇总 - 运行时间: {running_time:.2f}秒, "
                        f"获取数据: {data_count}条, "
                        f"API请求次数: {api_request_count}次"
                    )
                logger.info("当前不在交易时间，程序结束")
                break
                
        # 采集数据
        raw_data = fetch_data()
        api_request_count += 1  # 记录 API 请求次数
        
        if raw_data and len(raw_data) >= 10:
            if save_to_db(raw_data):
                data_count += 1  # 记录成功获取的数据条数
        else:
            logger.warning("获取到无效数据，等待重试")
            
        # 等待 60 秒
        ScheduleManager.wait_until_next_minute()

if __name__ == "__main__":
    logger.info("程序启动")
    
    # 初始化数据库管理器
    db_manager = DatabaseManager()
    
    # 如果是正式模式，检查是否为交易日
    if not db_manager.is_test_mode:
        if not TradingDayChecker.is_trading_day():
            logger.info(f"{datetime.date.today()} 不是交易日，程序正常结束")
            sys.exit(0)
    
    try:
        # 主循环
        while True:
            # 如果是正式模式，检查是否在交易时间
            if not db_manager.is_test_mode and not ScheduleManager.is_trading_time():
                logger.info("当前不在交易时间，程序结束")
                break
                
            # 采集数据
            raw_data = fetch_data()
            if raw_data and len(raw_data) >= 10:
                save_to_db(raw_data)
            else:
                logger.warning("获取到无效数据，等待重试")
                
            # 等待 30 秒
            ScheduleManager.wait_seconds(30)
            
    except KeyboardInterrupt:
        logger.info("程序被手动终止")
    except SystemExit:
        logger.info("程序正常退出")
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}", exc_info=True)
    finally:
        logger.info("程序结束")