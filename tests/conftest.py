from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.main import app
from app.models.base import Base

# 使用 SQLite In-Memory 資料庫進行自動化測試，並透過 StaticPool 共用同一個連線池
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """每次測試前建立所有資料表，測試結束後自動清理。"""
    # 建立全新資料表結構
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # 清除資料表
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """提供掛載測試資料庫依賴的 FastAPI TestClient。"""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    # 覆寫 FastAPI 的 get_db 依賴項為測試用 session
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # 測試完成後清理 override
    app.dependency_overrides.clear()
