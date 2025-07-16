# 匯入必要套件
import pandas as pd  # 用來處理資料表（DataFrame）
from loguru import logger  # 日誌工具，用來輸出 log 訊息
from sqlalchemy import create_engine  # 建立資料庫連線的工具（SQLAlchemy）
from crawler.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT

if __name__ == "__main__":
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/mydb"
    )

    # 建立連線（可用於 Pandas、原生 SQL 操作）
    connect = engine.connect()

    # 建立一個空的 DataFrame 並加入一個欄位 column_1，內容是 0~9
    df = pd.read_csv(
        "https://github.com/FinMind/FinMindBook/releases/download/data/taiwan_stock_price.csv"
    )
    logger.info(f"upload \n{df}")
    # 將 DataFrame 上傳至 MySQL 資料庫中的 test_upload 資料表
    # if_exists="replace" 表示如果資料表已存在，將其覆蓋
    # index=False 表示不上傳索引欄位
    df.to_sql(
        "taiwan_stock_price",
        con=connect,
        if_exists="replace",
        index=False,
    )

    # 上傳成功後，輸出 log 訊息
    logger.info("upload success")
