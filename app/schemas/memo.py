"""Pydantic 資料驗證與轉換模型 (Schemas).

本模組由新人負責從無到有進行設計與實作。
"""

# TODO: [新人任務 1]
# 請在此定義備忘錄系統所需的 Pydantic 模型：
# 1. MemoBase: 基礎共用屬性模型（例如：title, content, priority, is_completed 等欄位與驗證）
# 2. MemoCreate: 建立備忘錄時的 Request Body 資料模型
# 3. MemoUpdate: 部分更新備忘錄時的 Request Body 資料模型（所有欄位皆應為 Optional）
# 4. MemoResponse: 單筆備忘錄的 API Response 資料模型（需設定 ConfigDict(from_attributes=True)）
# 5. MemoListResponse: 多筆清單與分頁的回應資料模型（包含 total 總筆數與 items 列表）
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator


class MemoBase(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=100, description="title of the memo"
    )
    content: str | None = Field(None, description="content of the memo")
    priority: int = Field(default=3, ge=1, le=5)
    is_completed: bool = False


class MemoCreate(MemoBase):
    pass


class MemoResponse(MemoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class MemoUpdate(BaseModel):
    title: str | None = Field(
        None, min_length=1, max_length=100, description="title of the memo"
    )
    content: str | None = Field(None, description="content of the memo")
    priority: int | None = Field(None, ge=1, le=5)
    is_completed: bool | None = None  # 預設是不改而不是塞新資訊進去

    @field_validator("title", "priority", "is_completed")
    @classmethod
    def check_null(cls, value: str | int | bool | None) -> str | int | bool:
        if value is None:
            raise ValueError("can't be assigned to None")
        return value


class MemoListResponse(BaseModel):
    total: int
    items: list[MemoResponse]
