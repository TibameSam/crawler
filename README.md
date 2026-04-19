# crawler

這是一個「台股資料爬蟲系統」的教學專案，帶你從零學會如何用工業界常見的架構，定期自動抓取股票資料並寫入資料庫。

## 這個專案在做什麼？

簡單來說，整個流程像這樣：

```
排程器 (Scheduler)  →  發送任務 (Producer)  →  RabbitMQ 佇列  →  工人 (Worker) 執行爬蟲  →  寫入 MySQL / BigQuery
```

- **Scheduler（排程器）**：每隔一段時間（例如 12 小時）自動觸發，就像鬧鐘
- **Producer（生產者）**：把「要爬哪支股票」這件任務丟到 RabbitMQ 排隊
- **RabbitMQ（訊息佇列）**：像是任務的「候位區」，讓工人依序領工作
- **Worker（工人）**：從佇列拿任務，呼叫 FinMind API 抓股價資料
- **MySQL / BigQuery**：最終把資料存進資料庫，之後可用來做分析

## 為什麼要這樣設計？

初學者可能會想：「直接寫一個 Python script 一次把所有股票抓下來不就好了嗎？」

是可以，但當你面對以下情境時就會卡住：
- **資料量大**：上千支股票一個一個抓，一台電腦跑一整天還沒跑完
- **需要容錯**：抓到一半某支股票失敗了，整支程式崩潰，前面的白跑
- **需要水平擴展**：想多開幾台機器一起跑，script 架構做不到

所以業界會用 **Celery + RabbitMQ** 這種「分散式任務佇列」架構：任務丟進佇列後，可以多個 worker 同時領任務處理，失敗的任務還能自動重試。

## 使用的技術

| 技術 | 用途 | 為什麼用它 |
| --- | --- | --- |
| Python 3.11 | 主要開發語言 | 爬蟲、資料處理套件最豐富 |
| [uv](https://docs.astral.sh/uv/) | 套件管理 | 比 pip/pipenv 快 10～100 倍 |
| [Celery](https://docs.celeryq.dev/) | 分散式任務佇列 | 讓任務可以分派到多台 worker |
| [RabbitMQ](https://www.rabbitmq.com/) | 訊息中介 (broker) | Celery 依賴它來傳遞任務 |
| [Flower](https://flower.readthedocs.io/) | Celery 監控介面 | 可視化看 worker 狀態與任務 |
| [APScheduler](https://apscheduler.readthedocs.io/) | 排程器 | 定時觸發任務 |
| MySQL | 關聯式資料庫 | 儲存爬回來的股價資料 |
| Google BigQuery | 雲端資料倉儲 | 儲存大量歷史資料供分析 |
| SQLAlchemy | ORM | 用 Python 物件操作資料庫，不用寫純 SQL |
| Docker + Docker Compose | 容器化部署 | 讓服務能一鍵啟動、跨平台執行 |
| Google Cloud Secret Manager | 密碼管理 | 避免帳密寫死在程式碼裡 |

## 資料夾結構速覽

```
crawler/
├── worker.py                         # 建立 Celery app (所有 task 的總入口)
├── tasks.py                          # 範例 task
├── tasks_crawler_finmind.py          # 實際的爬蟲 task (append 模式)
├── tasks_crawler_finmind_duplicate.py # 去重複版本 (upsert 模式)
├── producer.py                       # 最簡單的任務派送範例
├── producer_crawler_finmind.py       # for 迴圈批次派送任務
├── producer_multi_queue.py           # 多佇列分流範例
├── scheduler.py                      # 定時自動派送任務
├── config.py                         # 環境變數集中管理
└── upload_*.py                       # 各種資料上傳腳本 (教學用)
```

## 學習順序建議

如果你是第一次接觸這個專案，建議依序閱讀：

1. `config.py` — 了解環境變數怎麼管理
2. `worker.py` + `tasks.py` — 認識 Celery task 最小範例
3. `producer.py` — 派送第一個任務，親手跑一次
4. `tasks_crawler_finmind.py` — 看真實的爬蟲邏輯
5. `producer_multi_queue.py` — 學習如何分流任務
6. `scheduler.py` — 最後把一切串起來，自動化執行

---

# 環境設定

#### 安裝 uv

    curl -LsSf https://astral.sh/uv/install.sh | sh

#### 安裝 Python 3.11

    uv python install 3.11

#### set uv 虛擬環境

    uv venv --python 3.11

#### 安裝 repo 套件

    uv sync

#### 建立環境變數

    ENV=DEV python genenv.py
    ENV=DOCKER python genenv.py
    ENV=PRODUCTION python genenv.py

#### 排版

    black -l 80 crawler/

# Worker

#### 啟動預設執行 celery 的 queue 的工人

    uv run --env-file=.env celery -A crawler.worker worker --loglevel=info

#### 啟動執行 twse 的 queue 的工人

    uv run --env-file=.env celery -A crawler.worker worker -Q twse,tpex --loglevel=info

# Producer

#### 發送任務

    uv run --env-file=.env python crawler/producer.py

#### for loop 發送多個任務

    uv run --env-file=.env python crawler/producer_crawler_finmind.py

#### 發送任務到不同 queue

    uv run --env-file=.env python crawler/producer_multi_queue.py


# Docker

#### build docker image

    docker build -f Dockerfile -t linsamtw/tibame_crawler:0.0.1 .
    docker build -f Dockerfile -t linsamtw/tibame_crawler:0.0.2 .
    docker build -f with.env.Dockerfile -t linsamtw/tibame_crawler:0.0.3 .
    docker build -f with.env.Dockerfile -t linsamtw/tibame_crawler:0.0.4 .
    docker build -f with.env.Dockerfile -t linsamtw/tibame_crawler:0.0.5 .
    docker build -f with.env.Dockerfile -t linsamtw/tibame_crawler:0.0.6 .
    docker buildx build -f with.env.Dockerfile --platform linux/arm64 -t linsamtw/tibame_crawler:0.0.6.arm64 .
    docker build -f with.env.Dockerfile -t linsamtw/tibame_crawler:0.0.7 .
    docker build -f prod.with.env.Dockerfile -t linsamtw/tibame_crawler:0.0.8.composer .
    docker build -f with.env.Dockerfile -t linsamtw/tibame_crawler:0.0.9 .

#### push docker image

    docker push linsamtw/tibame_crawler:0.0.1
    docker push linsamtw/tibame_crawler:0.0.2
    docker push linsamtw/tibame_crawler:0.0.3
    docker push linsamtw/tibame_crawler:0.0.4
    docker push linsamtw/tibame_crawler:0.0.5
    docker push linsamtw/tibame_crawler:0.0.6
    docker push linsamtw/tibame_crawler:0.0.6.arm64
    docker push linsamtw/tibame_crawler:0.0.7
    docker push linsamtw/tibame_crawler:0.0.8.composer
    docker push linsamtw/tibame_crawler:0.0.9

#### 建立 network

    docker network create my_network

#### 啟動 rabbitmq

    docker compose -f rabbitmq-network.yml up -d

#### 關閉 rabbitmq

    docker compose -f rabbitmq-network.yml down

#### 啟動 mysql

    docker compose -f mysql.yml up -d

#### 關閉 mysql

    docker compose -f mysql.yml down

#### 啟動 worker

    docker compose -f docker-compose-worker-network.yml up -d
    DOCKER_IMAGE_VERSION=0.0.3 docker compose -f docker-compose-worker-network-version.yml up -d
    DOCKER_IMAGE_VERSION=0.0.5 docker compose -f docker-compose-worker-network-version.yml up -d
    DOCKER_IMAGE_VERSION=0.0.6 docker compose -f docker-compose-worker-network-version.yml up -d

#### 關閉 worker

    docker compose -f docker-compose-worker-network.yml down
    DOCKER_IMAGE_VERSION=0.0.3 docker compose -f docker-compose-worker-network-version.yml down
    DOCKER_IMAGE_VERSION=0.0.5 docker compose -f docker-compose-worker-network-version.yml down
    DOCKER_IMAGE_VERSION=0.0.6 docker compose -f docker-compose-worker-network-version.yml down

#### producer 發送任務

    docker compose -f docker-compose-producer-network.yml up -d
    DOCKER_IMAGE_VERSION=0.0.3 docker compose -f docker-compose-producer-network-version.yml up -d
    DOCKER_IMAGE_VERSION=0.0.5 docker compose -f docker-compose-producer-network-version.yml up -d
    DOCKER_IMAGE_VERSION=0.0.6 docker compose -f docker-compose-producer-duplicate-network-version.yml up -d

#### 查看 docker container 狀況

    docker ps -a

#### 啟動 scheduler

    DOCKER_IMAGE_VERSION=0.0.4 docker compose -f docker-compose-scheduler-network-version.yml up -d

#### 關閉 scheduler

    DOCKER_IMAGE_VERSION=0.0.4 docker compose -f docker-compose-scheduler-network-version.yml down

#### 查看 log

    docker logs container_name

#### 下載 taiwan_stock_price.csv

    wget https://github.com/FinMind/FinMindBook/releases/download/data/taiwan_stock_price.csv

#### 上傳 taiwan_stock_price.csv

    uv run --env-file=.env python crawler/upload_taiwan_stock_price_to_mysql.py

#### login
    gcloud auth application-default login

#### set GCP project
    gcloud config set project high-transit-465916-a6

#### 上傳台股股價到 BigQuery
    uv run --env-file=.env python crawler/upload_taiwan_stock_price_to_bigquery.py

#### 輸入 Secret Manager
    uv run --env-file=.env python crawler/print_secret_manager.py
