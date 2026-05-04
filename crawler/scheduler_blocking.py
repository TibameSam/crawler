# 匯入 APScheduler 的排程器（阻塞式）
from apscheduler.schedulers.blocking import BlockingScheduler

# 匯入 loguru 進行清晰的 log 紀錄
from loguru import logger

# 匯入 Celery 任務（假設你用的是非同步任務）
from crawler.tasks_crawler_finmind import crawler_finmind


# 測試用排程任務：印出 hello world（每 5 秒執行一次）
def hello_world():
    logger.info("========================hello_world=====================")


# 實際任務：發送多檔股票資料抓取任務
def send_crawler_stock_price_task():
    # 一次發送多支股票代碼，讓 Celery 處理
    for stock_id in ["2330", "0050", "2317", "0056", "00713"]:
        logger.info(stock_id)  # 印出目前處理的股票代碼
        crawler_finmind.delay(
            stock_id=stock_id
        )  # 非同步觸發任務（使用 Celery）


def main():
    # 建立背景排程器，設定時區為 Asia/Taipei
    scheduler = BlockingScheduler(
        timezone="Asia/Taipei",
    )
    # 新增 hello_world 任務，每 5 秒執行一次
    scheduler.add_job(
        id="hello_world",  # 任務 ID（唯一識別）
        func=hello_world,  # 要執行的函式
        trigger="cron",  # 使用 cron 式排程
        hour="*",  # 每小時
        minute="*",  # 每分鐘
        day_of_week="*",  # 每天
        # day_of_week="1-5",  # 週一到週五執行
        # day_of_week="0,1,3,5",  # 週日、週一、週三、週五執行
        second="*/5",  # 每 5 秒執行一次
        coalesce=True,  # 如果錯過排程，只執行一次（避免重複執行）
    )
    # 新增爬蟲任務，每 12 小時整點執行一次
    scheduler.add_job(
        id="send_crawler_stock_price_task",
        func=send_crawler_stock_price_task,
        trigger="cron",
        hour="*/12",  # 每 12 小時
        minute="0",  # 整點
        day_of_week="*",  # 每天
        second="0",  # 整點
        coalesce=True,
    )
    logger.info(
        "send_crawler_stock_price_task add scheduler"
    )  # log 記錄啟用排程
    scheduler.start()  # 啟動排程器


if __name__ == "__main__":
    main()
