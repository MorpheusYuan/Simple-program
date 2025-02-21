import datetime
import requests

class TradingDayChecker:
    @staticmethod
    def is_trading_day(date=None):
        """
        判断是否为交易日
        :param date: datetime.date对象，默认为当天
        :return: bool
        """
        if date is None:
            date = datetime.date.today()
            
        # 周末判断
        if date.weekday() >= 5:  # 5=周六, 6=周日
            return False
            
        # 特殊节假日判断（需要更新）
        holidays = TradingDayChecker.get_holidays(date.year)
        if date in holidays:
            return False
            
        return True

    @staticmethod
    def get_holidays(year):
        """
        获取指定年份的节假日列表
        :param year: 年份
        :return: list of datetime.date
        """
        # 这里可以使用第三方API或者维护一个本地节假日列表
        holidays = [
            datetime.date(year, 1, 1),   # 元旦
            datetime.date(year, 1, 28),  # 春节
            datetime.date(year, 1, 29),
            datetime.date(year, 1, 30),
            datetime.date(year, 1, 31),
            datetime.date(year, 2, 3),
            datetime.date(year, 2, 4),
            datetime.date(year, 4, 4),   # 清明节
            datetime.date(year, 5, 1),   # 劳动节
            datetime.date(year, 5, 2),
            datetime.date(year, 5, 5),
            datetime.date(year, 6, 2),  # 端午节
            datetime.date(year, 10, 1), # 国庆中秋
            datetime.date(year, 10, 2),
            datetime.date(year, 10, 3),
            datetime.date(year, 10, 6),
            datetime.date(year, 10, 7),
            datetime.date(year, 10, 8),
        ]
        return holidays