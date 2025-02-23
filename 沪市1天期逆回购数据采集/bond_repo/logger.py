import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
from config import CONFIG

class Logger:
    def __init__(self):
        self.log_dir = "./logs"
        self._setup_logger()

    def _check_write_permission(self):
        """检查日志目录的写权限"""
        try:
            test_file = os.path.join(self.log_dir, "test.log")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except PermissionError:
            return False
        except Exception as e:
            self.logger.error(f"检查写权限失败: {str(e)}", exc_info=True)
            return False

    def _setup_logger(self):
        """配置日志系统"""
        try:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir, mode=0o755)  # 确保目录有写权限

            # 检查写权限
            if not self._check_write_permission():
                raise PermissionError(f"没有写权限: {self.log_dir}")

            # 创建主日志记录器
            self.logger = logging.getLogger("bond_collector")
            self.logger.setLevel(logging.DEBUG)

            # 日志格式
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            # 按文件大小轮转（最大 10MB，保留 5 个备份）
            file_handler = RotatingFileHandler(
                filename=os.path.join(self.log_dir, "bond_collector.log"),
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,  # 保留 5 个备份
                encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)

            # 按时间轮转（每天一个文件，保留 7 天）
            time_handler = TimedRotatingFileHandler(
                filename=os.path.join(self.log_dir, "bond_collector.log"),
                when="midnight",  # 每天午夜轮转
                backupCount=7,  # 保留 7 天
                encoding="utf-8"
            )
            time_handler.setFormatter(formatter)
            time_handler.setLevel(logging.INFO)
            self.logger.addHandler(time_handler)

            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(console_handler)

        except PermissionError as e:
            # 如果权限不足，使用备用日志目录
            self.log_dir = "/tmp/bond_repo_logs"
            os.makedirs(self.log_dir, exist_ok=True)
            self._setup_logger()  # 重新初始化日志系统
        except Exception as e:
            self.logger.error(f"初始化日志系统失败: {str(e)}", exc_info=True)

    def get_logger(self):
        return self.logger

# 单例日志实例
logger = Logger().get_logger()