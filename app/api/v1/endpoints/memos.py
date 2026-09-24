from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.crud_memo import create_memo, get_memo_by_id, delete_memo
from app.models.memo import Memo
from app.schemas.memo import MemoCreate, MemoResponse

router = APIRouter()

# TODO: [新人任務 3]
# 請在此設計並實作備忘錄系統的 RESTful API 路由端點：
# 1. POST / (201 Created) - 建立新備忘錄
# 2. GET / (200 OK) - 取得備忘錄分頁清單（支援 skip, limit, is_completed, search 查詢參數）
# 3. GET /{id} (200 OK) - 取得指定 ID 備忘錄（不存在回傳 404）
# 4. PATCH /{id} (200 OK) - 部分更新指定 ID 備忘錄（不存在回傳 404）
# 5. DELETE /{id} (204 No Content) - 刪除指定 ID 備忘錄（不存在回傳 404）


@router.post("/", response_model=MemoResponse, status_code=status.HTTP_201_CREATED)
def create(memo_in: MemoCreate, db: Session = Depends(get_db)) -> Memo:
    return create_memo(db, memo_in)


@router.get("/{memo_id}", response_model=MemoResponse, status_code=status.HTTP_200_OK)
def read(memo_id: int, db: Session = Depends(get_db)) -> Memo:
    searched_memo = get_memo_by_id(db, memo_id)
    if searched_memo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found"
        )
    return searched_memo


@router.delete("/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(memo_id: int, db: Session = Depends(get_db)) -> None:
    is_deleted = delete_memo(db, memo_id)
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found"
        )
