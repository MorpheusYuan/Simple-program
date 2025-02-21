import datetime
import time

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
    def wait_until_next_minute():
        """等待到下一分钟开始"""
        now = datetime.datetime.now()
        next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
        sleep_seconds = (next_minute - now).total_seconds()
        time.sleep(sleep_seconds)