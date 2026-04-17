# crawler

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
