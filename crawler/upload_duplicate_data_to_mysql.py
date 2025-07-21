# 匯入 SQLAlchemy 所需模組
# 匯入 pandas 並建立一個 DataFrame，模擬要寫入的資料
import pandas as pd
from sqlalchemy import (
    Column,
    Date,
    Float,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.dialects.mysql import (
    insert,
)  # 專用於 MySQL 的 insert 語法，可支援 on_duplicate_key_update

from crawler.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT

# 建立連接到 MySQL 的資料庫引擎（記得把帳號密碼換成你自己的）
engine = create_engine(
    f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/tibame"
)

# 開啟連線
conn = engine.connect()

# 定義資料表結構，對應到 MySQL 中的 test_duplicate 表
metadata = MetaData()
stock_price_table = Table(
    "test_duplicate",  # 資料表名稱
    metadata,
    Column("stock_id", String(50), primary_key=True),  # 主鍵 stock_id 欄位
    Column("date", Date, primary_key=True),
    Column("price", Float),
)
# ✅ 自動建立資料表（如果不存在才建立）
metadata.create_all(engine)

df = pd.DataFrame(
    [
        # 模擬 5 筆重複資料
        {"stock_id": "2330", "date": "2025-06-25", "price": 1000},
        {"stock_id": "2330", "date": "2025-06-25", "price": 1001},
        {"stock_id": "2330", "date": "2025-06-25", "price": 1002},
        {"stock_id": "2330", "date": "2025-06-25", "price": 1003},
        {"stock_id": "2330", "date": "2025-06-25", "price": 1004},
    ]
)

# 遍歷 DataFrame 的每一列資料
for _, row in df.iterrows():
    # 使用 SQLAlchemy 的 insert 語句建立插入語法
    insert_stmt = insert(stock_price_table).values(**row.to_dict())

    # 加上 on_duplicate_key_update 的邏輯：
    # 若主鍵重複（id 已存在），就更新 name 與 score 欄位為新值
    update_stmt = insert_stmt.on_duplicate_key_update(
        **{
            col.name: insert_stmt.inserted[col.name]
            for col in stock_price_table.columns
            if col.name != "id"
        }
    )

    # 執行 SQL 語句，寫入資料庫
    with engine.begin() as conn:
        conn.execute(update_stmt)
