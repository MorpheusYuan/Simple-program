import pytest
from utils import ScheduleManager
from datetime import datetime, time

def test_is_trading_time():
    # 测试交易时间
    trading_time = time(10, 0)  # 上午交易时间
    assert ScheduleManager.is_trading_time(trading_time)

    # 测试非交易时间
    non_trading_time = time(12, 0)  # 午休时间
    assert not ScheduleManager.is_trading_time(non_trading_time)