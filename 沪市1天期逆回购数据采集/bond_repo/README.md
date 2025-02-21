# 沪市一天期国债逆回购204001数据采集系统

## 项目概述
本项目是NAS上的python脚本，用于定时采集上海证券交易所国债逆回购（204001）的交易数据（计划持续1年，共67500条数据），并将数据存储到SQLite数据库中，为后续分析提供数据支持。API接口用免费的新浪财经接口，请求间隔60s。

## 功能特性
- [x] 交易日自动判断
- [x] 交易时间段定时采集（9:30-11:30，13:00-15:30）
- [x] 每分钟采集一次数据
- [x] 数据存储到SQLite数据库
- [ ] 日志记录系统（开发中）
- [ ] 异常通知功能（开发中）

## 系统要求
- Python 3.9+
- SQLite3
- 群辉NAS（支持其他Linux系统）

## 安装步骤

1. 克隆仓库：
    ```bash
    git clone https://github.com/your_username/bond-repo-collector.git
    cd bond-repo-collector

2. 安装依赖：
    ```bash
    pip install -r requirements.txt

3. 创建必要目录：
    ```bash
    mkdir -p data logs

4. 设置定时任务：
    在群辉DSM中设置定时任务
    每天9:15运行start.sh
    确保python路径正确

项目结构
bond-repo-collector/
├── config.py         # 配置文件
├── main.py           # 主程序
├── start.sh          # 启动脚本
├── requirements.txt  # 依赖库
├── trading_days.py   # 交易日判断
├── utils.py          # 工具函数
├── data/             # 数据库目录
└── logs/             # 日志目录

配置文件说明
    编辑config.py配置以下参数：
    api_url: 数据接口地址
    db_path: 数据库路径
    timeout: 请求超时时间
    retry_times: 重试次数
    headers: HTTP请求头

使用说明
    1. 手动运行：
        ```bash
        ./start.sh
    2. 查看数据：
        ```bash
        sqlite3 data/bond_data.db

许可证
MIT License