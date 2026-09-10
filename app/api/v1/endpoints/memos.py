from fastapi import APIRouter

router = APIRouter()

# TODO: [新人任務 3]
# 請在此設計並實作備忘錄系統的 RESTful API 路由端點：
# 1. POST / (201 Created) - 建立新備忘錄
# 2. GET / (200 OK) - 取得備忘錄分頁清單（支援 skip, limit, is_completed, search 查詢參數）
# 3. GET /{id} (200 OK) - 取得指定 ID 備忘錄（不存在回傳 404）
# 4. PATCH /{id} (200 OK) - 部分更新指定 ID 備忘錄（不存在回傳 404）
# 5. DELETE /{id} (204 No Content) - 刪除指定 ID 備忘錄（不存在回傳 404）
