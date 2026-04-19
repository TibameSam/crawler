# 這是「去重複版本」的 producer
# 差別在: 對應的 task 在寫入 MySQL 時會用 on_duplicate_key_update
# 避免同一筆資料重複 insert 造成主鍵衝突
from crawler.tasks_crawler_finmind_duplicate import crawler_finmind_duplicate

# .s() 建立 signature, 再用 apply_async 指定 queue
# 這裡同樣示範多佇列分流 (twse / tpex)
# 發送到 twse 的 queue
task_2330 = crawler_finmind_duplicate.s(stock_id="2330")
task_2330.apply_async(queue="twse")  # 發送任務
print("send task_2330 task")
# 發送到 tpex 的 queue
task_00679b = crawler_finmind_duplicate.s(stock_id="00679B")  # 美債
task_00679b.apply_async(queue="tpex")  # 發送任務
print("send task_00679b task")
