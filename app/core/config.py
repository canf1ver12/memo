from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """應用程式設定管理類別，自動讀取環境變數與 .env 檔案。"""

    # 專案名稱
    PROJECT_NAME: str = "政大通備忘錄系統"

    # API 路由前綴
    API_V1_STR: str = "/api/v1"

    # 資料庫連線字串（預設使用本地 SQLite 便於快速測試開發）
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# 實例化設定物件供全域匯入使用
settings = Settings()

