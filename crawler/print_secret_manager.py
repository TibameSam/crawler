# 匯入 Google Cloud Secret Manager 的 Python 用戶端
from google.cloud import secretmanager


# 定義一個函式，用來取得特定專案中的 secret 值
def get_secret_value(project_id: str, secret_id: str):
    # 建立 Secret Manager 的客戶端
    client = secretmanager.SecretManagerServiceClient()

    # 使用 secret_path 組出 secret 的完整路徑（非版本）
    # e.g. projects/PROJECT_ID/secrets/SECRET_ID
    parent = client.secret_path(project_id, secret_id)

    # 取得該 secret 的所有版本（通常最新的是第一個）
    secret_versions = [
        version.name for version in client.list_secret_versions(parent=parent)
    ]

    # 這裡只取第一個版本（即最新版本）
    secret_versions = secret_versions[0]

    # 存取這個 secret 版本的內容
    secret_value = client.access_secret_version(name=secret_versions)

    # 印出原始 secret 資訊（包含 metadata）
    print(f"secret_value:\n{secret_value}")

    # 解碼後印出 secret 真正的文字內容（通常是密碼或 API 金鑰）
    print(f"{secret_id}: {secret_value.payload.data.decode('UTF-8')}")

    # 回傳解碼後的 secret 值
    return secret_value.payload.data.decode("UTF-8")


# 主程式區塊，用來測試 secret 取得功能
if __name__ == "__main__":
    get_secret_value(project_id="135556101349", secret_id="mysql_password")
