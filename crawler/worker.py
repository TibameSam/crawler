from celery import Celery
from loguru import logger
from crawler.config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    WORKER_ACCOUNT,
    WORKER_PASSWORD,
)

logger.info(
    f"""
    RABBITMQ_HOST: {RABBITMQ_HOST}
    RABBITMQ_HOST: {RABBITMQ_PORT}
    RABBITMQ_HOST: {WORKER_ACCOUNT}
    RABBITMQ_HOST: {WORKER_PASSWORD}
"""
)
app = Celery(
    "task",
    # 只包含 tasks.py 裡面的程式, 才會成功執行
    include=[
        "crawler.tasks",
        "crawler.tasks_crawler_finmind",
        "crawler.tasks_crawler_finmind_duplicate",
    ],
    # 連線到 rabbitmq,
    # pyamqp://user:password@127.0.0.1:5672/
    # 帳號密碼都是 worker
    broker=f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/",
)
