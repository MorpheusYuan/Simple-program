# 基本配置项
CONFIG = {
    "api_url": "http://hq.sinajs.cn/list=sh204001",
    "db_path": "./data/bond_data.db",
    "timeout": 10,  # 请求超时时间
    "retry_times": 3,  # 重试次数
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "http://finance.sina.com.cn/"
    },
    "test_mode": {
        "enabled": False,  # 手动控制测试模式，True 为启用，False 为禁用
        "db_path": "./data/test_bond_data.db",
        "log_suffix": "_test"
    }
}