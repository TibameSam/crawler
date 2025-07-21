import pandas as pd
import requests
from sqlalchemy import create_engine  # 建立資料庫連線的工具（SQLAlchemy）
from sqlalchemy import BigInteger, Column, Date, Float, MetaData, String, Table
from sqlalchemy.dialects.mysql import (
    insert,
)  # 專用於 MySQL 的 insert 語法，可支援 on_duplicate_key_update

from crawler.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT
from crawler.worker import app


def upload_data_to_mysql_duplicate(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/tibame"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    # 定義資料表結構，對應到 MySQL 中的 stock_price_table 表
    metadata = MetaData()
    stock_price_table = Table(
        "TaiwanStockPrice_duplicate",  # 資料表名稱
        metadata,
        Column("stock_id", String(50), primary_key=True),  # 主鍵 stock_id 欄位
        Column("date", Date, primary_key=True),
        Column("Trading_Volume", BigInteger),
        Column("Trading_money", BigInteger),
        Column("open", Float),
        Column("max", Float),
        Column("min", Float),
        Column("close", Float),
        Column("spread", Float),
        Column("Trading_turnover", BigInteger),
    )
    # ✅ 自動建立資料表（如果不存在才建立）
    metadata.create_all(engine)
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
            }
        )

        # 執行 SQL 語句，寫入資料庫
        with engine.begin() as conn:
            conn.execute(update_stmt)


# 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
@app.task()
def crawler_finmind_duplicate(stock_id):
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": "2024-01-01",
        "end_date": "2025-06-17",
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()
    if resp.status_code == 200:
        df = pd.DataFrame(data["data"])
        print(df)
        # print("upload db")
        upload_data_to_mysql_duplicate(df)
    else:
        print(data["msg"])
