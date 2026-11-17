"""備忘錄資料庫存取層 (CRUD).

本模組由新人負責從無到有進行設計與實作。
"""

# TODO: [新人任務 2]
# 請在此實作備忘錄資料庫存取函式：
# 1. get_memo: 根據 ID 查詢單筆備忘錄
# 2. get_memos: 查詢備忘錄清單（支援分頁 skip/limit、完成狀態 is_completed 篩選、關鍵字 search 搜尋）
# 3. create_memo: 建立一筆新備忘錄並存入資料庫
# 4. update_memo: 部分更新備忘錄內容 (PATCH)
# 5. delete_memo: 刪除指定的備忘錄

from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from app.models.memo import Memo
from app.schemas.memo import MemoCreate, MemoUpdate


def create_memo(db: Session, memo_in: MemoCreate) -> Memo:
    data = memo_in.model_dump()
    memo = Memo(**data)
    db.add(memo)
    db.commit()
    db.refresh(memo)
    return memo


def get_memo_by_id(db: Session, memo_id: int) -> Memo | None:
    memo = db.get(Memo, memo_id)
    return memo


def delete_memo(db: Session, memo_id: int) -> bool:
    be_deleted_memo = get_memo_by_id(db, memo_id)
    if be_deleted_memo is None:
        return False

    db.delete(be_deleted_memo)
    db.commit()
    return True


def get_memos(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    is_completed: bool | None = None,
    search: str | None = None,
) -> tuple[int, list[Memo]]:
    stmt = select(Memo)

    if is_completed is not None:
        stmt = stmt.where(Memo.is_completed == is_completed)
    if search:
        stmt = stmt.where(
            or_(Memo.title.contains(search), Memo.content.contains(search))
        )

    total_num = db.scalar(select(func.count()).select_from(stmt.subquery()))

    stmt = stmt.offset(skip)
    stmt = stmt.limit(limit)
    stmt = stmt.order_by(Memo.id)

    items = db.scalars(stmt).all()

    return total_num, list(items)


def update_memo(db: Session, db_memo: Memo, memo_in: MemoUpdate) -> Memo:
    update_content = memo_in.model_dump(exclude_unset=True)  # 只拿有動的欄位

    for key, value in update_content.items():
        setattr(db_memo, key, value)

    db.commit()
    db.refresh(db_memo)

    return db_memo
