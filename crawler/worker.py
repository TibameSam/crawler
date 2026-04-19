# Celery 是分散式任務佇列 (Distributed Task Queue)
# 可以把耗時的工作丟到背景 worker 執行, 不會卡住主程式
from celery import Celery

# loguru 是比標準 logging 更好用的日誌套件, 不用繁瑣設定就能直接用
from loguru import logger

# 從 config.py 讀取 RabbitMQ 連線資訊
# RabbitMQ 是訊息中介 (message broker), Celery 透過它派送任務給 worker
from crawler.config import (
    RABBITMQ_HOST,      # RabbitMQ 主機位址, ex: localhost
    RABBITMQ_PORT,      # RabbitMQ 通訊埠, 預設 5672
    WORKER_ACCOUNT,     # 連線到 RabbitMQ 的帳號
    WORKER_PASSWORD,    # 連線到 RabbitMQ 的密碼
)

# 印出目前讀到的環境變數, 方便除錯確認設定是否正確載入
logger.info(
    f"""
    RABBITMQ_HOST: {RABBITMQ_HOST}
    RABBITMQ_PORT: {RABBITMQ_PORT}
    WORKER_ACCOUNT: {WORKER_ACCOUNT}
    WORKER_PASSWORD: {WORKER_PASSWORD}
"""
)

# 建立 Celery app 實例, "task" 是這個應用程式的名稱
app = Celery(
    "task",
    # include: 告訴 Celery 要載入哪些 Python 模組裡的 task
    # 只有列在這裡的模組, 裡面用 @app.task 裝飾的函式才會被註冊為可執行任務
    include=[
        "crawler.tasks",                            # 一般任務
        "crawler.tasks_crawler_finmind",            # FinMind 爬蟲任務
        "crawler.tasks_crawler_finmind_duplicate",  # FinMind 重複資料檢查任務
    ],
    # broker: 指定訊息中介的連線網址, Celery 會把任務送到這裡排隊
    # 格式: pyamqp://帳號:密碼@主機:埠號/
    # 例如: pyamqp://worker:worker@127.0.0.1:5672/
    broker=f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/",
)
