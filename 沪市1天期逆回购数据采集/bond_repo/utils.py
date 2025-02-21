import time
import datetime
from logger import logger

class ScheduleManager:
    @staticmethod
    def is_trading_time():
        """判断当前是否在交易时间内"""
        now = datetime.datetime.now()
        current_time = now.time()
        
        # 上午交易时段
        morning_start = datetime.time(9, 30)
        morning_end = datetime.time(11, 30)
        
        # 下午交易时段
        afternoon_start = datetime.time(13, 0)
        afternoon_end = datetime.time(15, 30)
        
        return ((morning_start <= current_time <= morning_end) or 
                (afternoon_start <= current_time <= afternoon_end))

    @staticmethod
    def is_midday_break():
        """判断当前是否是午休时间（11:30-13:00）"""
        now = datetime.datetime.now()
        current_time = now.time()
        midday_start = datetime.time(11, 30)
        midday_end = datetime.time(13, 0)
        return midday_start <= current_time < midday_end

    @staticmethod
    def wait_until_afternoon():
        """等待到下午开盘时间（13:00）"""
        now = datetime.datetime.now()
        afternoon_start = now.replace(hour=13, minute=0, second=0, microsecond=0)
        
        # 如果当前时间已经超过 13:00，等待到明天的 13:00
        if now >= afternoon_start:
            afternoon_start += datetime.timedelta(days=1)
            
        sleep_seconds = (afternoon_start - now).total_seconds()
        logger.info(f"等待 {sleep_seconds:.2f} 秒直到下午开盘...")
        time.sleep(sleep_seconds)

    @staticmethod
    def wait_seconds(seconds):
        """等待指定秒数"""
        logger.debug(f"等待 {seconds} 秒...")
        time.sleep(seconds)

    @staticmethod
    def wait_until_next_minute():
        """等待到下一分钟开始"""
        now = datetime.datetime.now()
        next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
        sleep_seconds = (next_minute - now).total_seconds()
        logger.debug(f"等待 {sleep_seconds:.2f} 秒直到下一分钟...")
        time.sleep(sleep_seconds)

    @staticmethod
    def is_trading_day():
        """判断当前是否为交易日"""
        from trading_days import TradingDayChecker
        return TradingDayChecker.is_trading_day()