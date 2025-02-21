import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from config import CONFIG

class Logger:
    def __init__(self):
        self.log_dir = "./logs"
        self._setup_logger()
        self.handle_uncaught_exception()

    # 在Logger类中添加
    def handle_uncaught_exception(self):
        """处理未捕获的异常"""
        def exception_handler(exc_type, exc_value, exc_traceback):
            # 让全局异常处理程序处理
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        
        # 设置全局异常处理
        sys.excepthook = exception_handler

    def _setup_logger(self):
        """配置日志系统"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 创建主日志记录器
        self.logger = logging.getLogger("bond_collector")
        self.logger.setLevel(logging.DEBUG)

        # 日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # 文件处理器（按天轮转）
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join(self.log_dir, "bond_collector.log"),
            when="midnight",
            backupCount=30,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)

        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

# 单例日志实例
logger = Logger().get_logger()