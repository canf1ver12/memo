from fastapi import APIRouter
from app.api.v1.endpoints import memos

api_router = APIRouter()

# 掛載備忘錄模組路由
api_router.include_router(
    memos.router,
    prefix="/memos",
    tags=["Memos"],
)
