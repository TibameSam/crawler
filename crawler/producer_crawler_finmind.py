# Producer: 負責「派送任務」, 把工作丟到 RabbitMQ 給 worker 處理
# 對應的 consumer 就是 tasks_crawler_finmind.py 裡註冊的 crawler_finmind task
from crawler.tasks_crawler_finmind import crawler_finmind

# for 迴圈, 可一次發送多個任務
# 這樣一次就能派送 5 支股票的爬蟲任務到 RabbitMQ
# Celery worker 會從 RabbitMQ 取出任務並平行處理, 比循序執行快很多
for stock_id in ["2330", "0050", "2317", "0056", "00713"]:
    print(stock_id)
    # .delay() 是 Celery 的非同步派送捷徑, 呼叫完會立刻回傳, 不等 task 執行完
    crawler_finmind.delay(stock_id=stock_id)
