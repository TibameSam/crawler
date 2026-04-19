# 多佇列 (multi queue) 範例:
# Celery 預設只有一條 queue, 所有 task 都排在一起
# 但實務上常需要依「任務類型」分流, 例如:
#   twse queue: 處理上市股票
#   tpex queue: 處理上櫃股票
# 這樣可以針對不同 queue 啟動專門的 worker, 避免互相搶資源
from crawler.tasks_crawler_finmind import crawler_finmind

# .s() = signature, 將 task 和參數「綁定」成一個可派送的物件
# 這樣就能更彈性地指定 queue、重試策略等進階設定
# 發送到 twse 的 queue
task_2330 = crawler_finmind.s(stock_id="2330")
# apply_async(queue=...) 可以指定任務要送到哪個 queue
# 對應的 worker 啟動時要加 -Q twse 才會消費 twse queue
task_2330.apply_async(queue="twse")  # 發送任務
print("send task_2330 task")
# 發送到 tpex 的 queue
task_00679b = crawler_finmind.s(stock_id="00679B")  # 美債
task_00679b.apply_async(queue="tpex")  # 發送任務
print("send task_00679b task")
