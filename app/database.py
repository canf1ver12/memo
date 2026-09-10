from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 處理 SQLite 的執行緒檢查參數（若非 SQLite 則無額外參數）
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# 建立 SQLAlchemy Engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# 建立資料庫 Session 工廠
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
