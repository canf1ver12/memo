"""備忘錄系統自動化測試 (pytest).

本測試模組由新人負責從無到有進行撰寫。
"""

# TODO: [新人任務 4]
# 請在此使用 pytest 與 client fixture (TestClient) 撰寫備忘錄系統測試案例：
# 1. test_create_memo: 測試 POST /api/v1/memos 建立備忘錄與資料完整性
# 2. test_read_memos_list: 測試 GET /api/v1/memos 列表、分頁、is_completed 篩選與 search 搜尋
# 3. test_read_memo_by_id: 測試 GET /api/v1/memos/{id} 查詢特定備忘錄與 404 異常處理
# 4. test_update_memo: 測試 PATCH /api/v1/memos/{id} 部分更新欄位與 404 異常處理
# 5. test_delete_memo: 測試 DELETE /api/v1/memos/{id} 刪除備忘錄與刪除後再次查詢回傳 404
