# 從 worker.py 匯入 Celery app 實例
# 所有的 task 都要透過 app 來註冊, 才能被 Celery worker 識別
from crawler.worker import app


# @app.task() 是 Celery 的裝飾器 (decorator)
# 有了這個裝飾器, 普通的 Python 函式就會變成「可派送的任務」
# 沒有裝飾的函式只能在本地呼叫, 無法透過 RabbitMQ 派送
@app.task()
def crawler(x):
    # 這裡只是示範, 實際專案會在這裡執行爬蟲邏輯
    print("crawler")
    print("upload db")
    # task 的回傳值可以透過 AsyncResult.get() 取得 (若有設定 result backend)
    return x
