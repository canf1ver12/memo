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

from fastapi import status
from fastapi.testclient import TestClient


# test memo create func
def test_create_memo(client: TestClient) -> None:
    response = client.post(
        "/api/v1/memos/",
        json={
            "title": "德文考試相關",
            "content": "複習單字",
            "priority": 4,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["title"] == "德文考試相關"
    assert data["content"] == "複習單字"
    assert data["priority"] == 4
    # assert data["priority"] == 5
    assert data["is_completed"] is False

    assert "id" in data
    # assert "it" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_read_memo_by_id(client: TestClient) -> None:
    not_found_response = client.get("/api/v1/memos/1")
    assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    create_response = client.post(
        "/api/v1/memos/",
        json={
            "title": "德文考試相關",
            "content": "複習單字",
            "priority": 4,
        },
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    memo_id = create_response.json()["id"]

    get_response = client.get(f"/api/v1/memos/{memo_id}")
    assert get_response.status_code == status.HTTP_200_OK

    data = get_response.json()

    assert data["title"] == "德文考試相關"
    assert data["content"] == "複習單字"
    assert data["priority"] == 4
    assert data["is_completed"] is False

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

    assert data["id"] == memo_id


def test_delete_memo(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/memos/",
        json={
            "title": "德文考試相關",
            "content": "複習單字",
            "priority": 4,
        },
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    memo_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/memos/{memo_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    check_response = client.get(f"/api/v1/memos/{memo_id}")
    assert check_response.status_code == status.HTTP_404_NOT_FOUND

    not_found_response = client.delete(f"/api/v1/memos/{memo_id}")
    assert not_found_response.status_code == status.HTTP_404_NOT_FOUND
