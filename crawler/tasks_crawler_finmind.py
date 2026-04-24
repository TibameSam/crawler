import pandas as pd
import requests
from sqlalchemy import create_engine  # 建立資料庫連線的工具（SQLAlchemy）

from crawler.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT
from crawler.worker import app


# 教學用: 最簡單版本, 只抓資料並印出, 不上傳資料庫
# 適合剛接觸 Celery 的人, 先確認「任務能被派送、worker 能收到、API 能呼叫」
# 之後再進階到 crawler_finmind (含資料庫寫入)
@app.task()
def crawler_finmind_print(stock_id):
    # FinMind API endpoint, 提供台股歷史股價等免費資料
    url = "https://api.finmindtrade.com/api/v4/data"
    # API 參數: 指定要抓哪個資料集、哪檔股票、日期範圍
    parameter = {
        "dataset": "TaiwanStockPrice",  # 台股日線資料
        "data_id": stock_id,  # 股票代碼, ex: 2330
        "start_date": "2024-01-01",
        "end_date": "2025-06-17",
    }
    # 發送 HTTP GET 請求, 把參數放在 query string
    resp = requests.get(url, params=parameter)
    # 將回傳的 JSON 轉成 Python dict
    data = resp.json()
    # HTTP 200 代表請求成功
    if resp.status_code == 200:
        # data["data"] 是 list of dict, 剛好可以直接轉成 DataFrame
        df = pd.DataFrame(data["data"])
        # 只印出資料, 不做後續處理
        print(df)
    else:
        # 若 API 失敗, 印出錯誤訊息方便排查
        print(data["msg"])


def upload_data_to_mysql(df: pd.DataFrame):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database
    try:
        address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/tibame"

        # 建立 SQLAlchemy 引擎物件
        engine = create_engine(address)

        # 建立連線（可用於 Pandas、原生 SQL 操作）
        connect = engine.connect()

        df.to_sql(
            "TaiwanStockPrice",
            con=connect,
            if_exists="append",
            index=False,
        )
    except Exception as e:
        pass


# 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
@app.task()
def crawler_finmind(stock_id):
    # FinMind API endpoint, 提供台股歷史股價等免費資料
    url = "https://api.finmindtrade.com/api/v4/data"
    # API 參數: 指定要抓哪個資料集、哪檔股票、日期範圍
    parameter = {
        "dataset": "TaiwanStockPrice",  # 台股日線資料
        "data_id": stock_id,  # 股票代碼, ex: 2330
        "start_date": "2024-01-01",
        "end_date": "2025-06-17",
    }
    # 發送 HTTP GET 請求, 把參數放在 query string
    resp = requests.get(url, params=parameter)
    # 將回傳的 JSON 轉成 Python dict
    data = resp.json()
    # HTTP 200 代表請求成功
    if resp.status_code == 200:
        # data["data"] 是 list of dict, 剛好可以直接轉成 DataFrame
        df = pd.DataFrame(data["data"])
        print(df)
        # print("upload db")
        # 將資料寫入 MySQL
        upload_data_to_mysql(df)
    else:
        # 若 API 失敗, 印出錯誤訊息方便排查
        print(data["msg"])
