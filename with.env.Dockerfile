# 使用 Ubuntu 22.04 作為基礎映像檔
FROM ubuntu:22.04

# 更新套件列表，並安裝 curl 與 ca-certificates（下載 uv 所需）
RUN apt-get update && \
    apt-get install -y curl ca-certificates

# 安裝 uv（用於 Python 虛擬環境和依賴管理）
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# 使用 uv 安裝 Python 3.11
RUN uv python install 3.11

# 建立工作目錄 /crawler
RUN mkdir /crawler

# 將當前目錄（與 Dockerfile 同層）所有內容複製到容器的 /crawler 資料夾
COPY ./crawler /crawler/crawler
COPY ./genenv.py /crawler
COPY ./pyproject.toml /crawler
COPY ./uv.lock /crawler
COPY ./README.md /crawler
COPY ./local.ini /crawler

# 設定容器的工作目錄為 /crawler，後續的指令都在這個目錄下執行
WORKDIR /crawler/

# 根據 uv.lock 安裝所有依賴（確保環境一致性）
RUN uv sync --frozen

# 設定語系環境變數，避免 Python 編碼問題
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# 建立 .env
RUN ENV=DOCKER uv run python genenv.py

# 啟動容器後，預設執行 bash（開啟終端）
CMD ["/bin/bash"]
