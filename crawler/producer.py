# Producer (生產者): 負責把任務送進 RabbitMQ 佇列
# 對應的 Consumer (消費者) 就是 worker.py 啟動的 Celery worker
# 流程: producer.py → RabbitMQ (訊息佇列) → worker 取出並執行任務

# 從 tasks.py 匯入 crawler 這個 Celery task 函式
# 注意這裡不是直接呼叫函式, 而是把它當作「任務」送出去
from crawler.tasks import crawler

# .delay() 是 Celery 提供的快捷方法, 用來「非同步」派送任務
# 寫 crawler.delay(x=0) 等同於 crawler.apply_async(kwargs={"x": 0})
# 呼叫後會立刻回傳, 任務會被丟到 RabbitMQ, 等 worker 拿去執行
# 如果改成 crawler(x=0) 則會在本地「同步」執行, 失去分散式的意義
crawler.delay(x=0)
