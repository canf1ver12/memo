from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依賴注入項：取得資料庫 Session。

    在請求處理開始時開啟 Session，並在請求結束後自動關閉釋放連線。

    Yields:
        Session: SQLAlchemy 資料庫 Session 實例
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
