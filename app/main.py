from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.api import api_router
from app.core.config import settings
from app.database import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """應用程式生命週期管理：在啟動時自動建立資料庫表（若尚未建立）。"""
    # 建立所有繼承 Base 的資料表（適用於 SQLite/開發環境快速開箱即用）
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    description="NCCUpass 政大通 - 備忘錄系統後端 API 服務 (Starter Template)",
    version="1.0.0",
)


# 根路徑歡迎端點
@app.get("/", tags=["Health"])
def root() -> dict:
    """服務根路徑歡迎訊息。"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs_url": "/docs",
        "version": "1.0.0",
    }


# 服務與資料庫連線健康檢查端點
@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)) -> dict:
    """健康檢查端點：確認服務狀態與資料庫連線是否正常。"""
    try:
        # 執行輕量查詢驗證資料庫連線
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": f"disconnected: {exc}",
                "service": settings.PROJECT_NAME,
            },
        )

    return {
        "status": "ok",
        "database": db_status,
        "service": settings.PROJECT_NAME,
    }


# 掛載 API v1 路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 掛載前端靜態頁面（http://localhost:8000/app/）
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.is_dir():
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
