import pytest
from trading_days import TradingDayChecker
from datetime import datetime, date

def test_is_trading_day():
    # 测试交易日
    trading_day = date(2023, 10, 10)  # 假设这是一个交易日
    assert TradingDayChecker.is_trading_day(trading_day)

    # 测试非交易日
    non_trading_day = date(2023, 10, 1)  # 假设这是一个非交易日
    assert not TradingDayChecker.is_trading_day(non_trading_day)