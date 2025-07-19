# 匯入必要套件
import time  # 用來做簡單的延遲操作（如 sleep）

import pandas as pd  # 用來處理表格資料（DataFrame）
from google.cloud import bigquery  # Google BigQuery 客戶端
from loguru import logger  # 優雅的日誌工具，取代 print 輸出


def create_taiwan_stock_price_table(client):
    """
    建立 BigQuery 中名為 `taiwan_stock_price` 的資料表，
    並設定欄位格式與時間分區（以日期欄位分區）。
    """
    # 定義資料表的 schema（欄位名稱、資料型態與是否必填）
    schema = [
        # 股票代號
        bigquery.SchemaField("StockID", "STRING", mode="REQUIRED"),
        # 成交股數
        bigquery.SchemaField("TradeVolume", "INTEGER", mode="REQUIRED"),
        # 成交筆數
        bigquery.SchemaField("Transaction", "INTEGER", mode="REQUIRED"),
        # 成交金額
        bigquery.SchemaField("TradeValue", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("Open", "FLOAT", mode="REQUIRED"),  # 開盤價
        bigquery.SchemaField("Max", "FLOAT", mode="REQUIRED"),  # 最高價
        bigquery.SchemaField("Min", "FLOAT", mode="REQUIRED"),  # 最低價
        bigquery.SchemaField("Close", "FLOAT", mode="REQUIRED"),  # 收盤價
        bigquery.SchemaField("Change", "FLOAT", mode="REQUIRED"),  # 漲跌價差
        bigquery.SchemaField("Date", "DATE", mode="REQUIRED"),
    ]

    # 建立 BigQuery 的 Table 物件，指定 dataset 與 table 名稱
    table = bigquery.Table(
        "high-transit-465916-a6.TaiwanStock.taiwan_stock_price",
        schema=schema,
    )

    # 設定以 "Date" 欄位作為時間分區，每日一區，並強制查詢時加上分區條件
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="Date",
        require_partition_filter=True,
    )

    # 嘗試建立資料表，若已存在則捕捉錯誤並記錄 log
    try:
        client.create_table(table)
        logger.info("client.create_table")  # 建立成功時輸出 log
        time.sleep(1)  # 小延遲，避免過快觸發後續操作
    except:
        logger.info("table already exists")  # 已存在則記錄訊息


if __name__ == "__main__":
    # 初始化 BigQuery 客戶端
    client = bigquery.Client()

    # 建立資料表（若已存在會略過）
    create_taiwan_stock_price_table(client)
    # 下載資料並讀取
    df = pd.read_csv(
        "https://github.com/FinMind/FinMindBook/releases/download/data/taiwan_stock_price.csv"
    )
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    # 將讀入的資料輸出至 log
    logger.info(f"upload \n{df}")
    # 使用 job config 明確指定 schema（可選）
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # 可改成 WRITE_TRUNCATE
    )

    logger.info("Uploading to BigQuery...")
    table_id = "high-transit-465916-a6.TaiwanStock.taiwan_stock_price"
    load_job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )
    logger.info("Upload success.")
