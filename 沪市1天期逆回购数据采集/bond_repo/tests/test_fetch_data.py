import pytest
from main import fetch_data
from config import CONFIG

def test_fetch_data():
    # 模拟正常情况
    data = fetch_data()
    assert data is not None
    assert len(data) >= 11  # 至少需要 11 个字段

    # 模拟 API 请求失败
    original_url = CONFIG['api_url']
    CONFIG['api_url'] = "http://invalid.url"
    data = fetch_data()
    assert data is None
    CONFIG['api_url'] = original_url  # 恢复原始配置