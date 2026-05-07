# 匯入必要套件
import pandas as pd  # 用來處理資料表（DataFrame）
from loguru import logger  # 日誌工具，用來輸出 log 訊息
from sqlalchemy import create_engine  # 建立資料庫連線的工具（SQLAlchemy）

if __name__ == "__main__":
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    address = "mysql+pymysql://root:test@127.0.0.1:3306/mydb"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)

    # 建立一個空的 DataFrame 並加入一個欄位 column_1，內容是 0~9
    df = pd.DataFrame()
    df["column_1"] = [i for i in range(10)]  # 產生 0~9 數字
    logger.info(f"upload \n{df}")
    # 將 DataFrame 上傳至 MySQL 資料庫中的 test_upload 資料表
    # if_exists="replace" 表示如果資料表已存在，將其覆蓋
    # index=False 表示不上傳索引欄位
    df.to_sql(
        "test_upload",
        con=engine,
        if_exists="replace",
        index=False,
    )

    # 上傳成功後，輸出 log 訊息
    logger.info("upload success")
