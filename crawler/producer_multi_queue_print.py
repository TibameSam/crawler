# 教學用版本: 多佇列 (multi queue) + 只印出不寫入資料庫
# 讓學生同時學到兩個觀念:
#   1. 多佇列分流 (twse / tpex)
#   2. 任務只印出, 方便觀察 worker 收到什麼
from crawler.tasks_crawler_finmind import crawler_finmind_print

# .s() = signature, 將 task 和參數「綁定」成一個可派送的物件
# 這樣就能更彈性地指定 queue、重試策略等進階設定
# 發送到 twse 的 queue
task_2330 = crawler_finmind_print.s(stock_id="2330")
# apply_async(queue=...) 可以指定任務要送到哪個 queue
# 對應的 worker 啟動時要加 -Q twse 才會消費 twse queue
task_2330.apply_async(queue="twse")  # 發送任務
print("send task_2330 task")
# 發送到 tpex 的 queue
task_00679b = crawler_finmind_print.s(stock_id="00679B")  # 美債
task_00679b.apply_async(queue="tpex")  # 發送任務
print("send task_00679b task")
