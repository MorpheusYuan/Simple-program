#### 新增功能
1. **日志系统**：
   - 添加了日志记录功能，支持按天分割日志文件。
   - 日志级别分为 DEBUG、INFO、WARNING 和 ERROR。
   - 日志文件存储在 `./logs` 目录下，保留最近 30 天的日志。

2. **数据验证机制**：
   - 添加了数据验证功能，确保 API 返回的数据格式正确。
   - 验证内容包括字段完整性、数据类型和数值范围。

3. **测试模式**：
   - 支持手动切换测试模式（通过 `config.py` 中的 `test_mode['enabled']` 配置）。
   - 测试模式下，数据保存到 `test_bond_data.db`，并忽略交易日和交易时间的检查。

4. **交易日处理优化**：
   - 在交易日 15:30 后，程序会记录当日汇总日志（运行时间、数据条数、API 请求次数）。
   - 程序在交易日 15:30 后正常终止，不会错误地继续运行。

5. **工具方法**：
   - 添加了 `wait_seconds()` 方法，支持指定等待时间。
   - 添加了 `wait_until_afternoon()` 方法，支持午休时间等待到下午开盘。

#### 修复问题
1. **测试模式自动切换问题**：
   - 移除了根据交易时间自动切换测试模式的逻辑，改为手动控制。

2. **数据验证失败问题**：
   - 修复了数据类型验证失败的问题，支持科学计数法和浮点数。

#### 更新功能特性
```markdown
## 功能特性
- [x] 交易日自动判断
- [x] 交易时间段定时采集（9:30-11:30，13:00-15:30）
- [x] 每分钟采集一次数据
- [x] 数据存储到SQLite数据库
- [x] 日志记录系统（支持按天分割和日志轮转）
- [x] 数据验证机制（字段完整性、数据类型、数值范围）
- [x] 测试模式（手动切换，数据保存到测试数据库）
- [x] 当日汇总日志（运行时间、数据条数、API 请求次数）
- [ ] 邮件通知功能（群辉DSM自带，无需开发）

更新项目结构
## 项目结构
    ```bash
    bond-repo-collector/
    ├── config.py # 配置文件
    ├── main.py # 主程序
    ├── start.sh # 启动脚本
    ├── requirements.txt # 依赖库
    ├── trading_days.py # 交易日判断
    ├── utils.py # 工具函数
    ├── data_validator.py # 数据验证
    ├── database_manager.py # 数据库管理
    ├── logger.py # 日志系统
    ├── data/ # 数据库目录
    └── logs/ # 日志目录

## 查看数据：
    正式数据：
    ```bash
    sqlite3 data/bond_data.db "SELECT * FROM bond_data;"
    测试数据：
    ```bash
    sqlite3 data/test_bond_data.db "SELECT * FROM bond_data;"

## 切换测试模式：
    修改 config.py 中的 test_mode['enabled'] 为 True 或 False。

————————
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
    ```bash
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
    ```bash
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