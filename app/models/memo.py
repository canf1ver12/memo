from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Boolean, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Memo(Base):
    """備忘錄資料庫模型 (SQLAlchemy ORM Model)

    對應資料表：memos
    """

    __tablename__ = "memos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="備忘錄唯一識別碼"
    )
    title: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True, comment="備忘錄標題"
    )
    content: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="備忘錄詳細內文"
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否已完成標記"
    )
    priority: Mapped[int] = mapped_column(
        Integer, default=3, nullable=False, comment="優先順序 (1: 低 ~ 5: 高)"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="建立時間",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="最後更新時間",
    )

    def __repr__(self) -> str:
        return f"<Memo id={self.id} title={self.title!r} is_completed={self.is_completed}>"


# =============================================================================
# 等效 SQL DDL（可直接複製至 SQLite / MySQL 執行建立相同結構的資料表）
# =============================================================================
#
# ── SQLite ────────────────────────────────────────────────────────────────────
#
# CREATE TABLE IF NOT EXISTS memos (
#     id           INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
#     title        VARCHAR(100) NOT NULL,
#     content      TEXT,
#     is_completed BOOLEAN  NOT NULL DEFAULT 0,
#     priority     INTEGER  NOT NULL DEFAULT 3,
#     created_at   DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
#     updated_at   DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
# );
#
# CREATE INDEX IF NOT EXISTS ix_memos_title ON memos (title);
#
# ── MySQL ─────────────────────────────────────────────────────────────────────
#
# CREATE TABLE IF NOT EXISTS memos (
#     id           INT          NOT NULL AUTO_INCREMENT COMMENT '備忘錄唯一識別碼',
#     title        VARCHAR(100) NOT NULL                COMMENT '備忘錄標題',
#     content      TEXT                                 COMMENT '備忘錄詳細內文',
#     is_completed TINYINT(1)   NOT NULL DEFAULT 0      COMMENT '是否已完成標記',
#     priority     INT          NOT NULL DEFAULT 3       COMMENT '優先順序 (1: 低 ~ 5: 高)',
#     created_at   DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
#                                                        COMMENT '建立時間',
#     updated_at   DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
#                               ON UPDATE CURRENT_TIMESTAMP(6)
#                                                        COMMENT '最後更新時間',
#     PRIMARY KEY (id),
#     INDEX ix_memos_title (title)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#
