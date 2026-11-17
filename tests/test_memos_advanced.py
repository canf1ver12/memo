from fastapi import status
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def seed_memos(client: TestClient) -> list[dict]:
    memos = [
        {"title": "德文相關", "content": "複習單字", "is_completed": True},
        {"title": "OS", "content": "寫OS作業及複習", "is_completed": False},
        {"title": "專案", "content": "收集資料", "is_completed": False},
        {"title": "買東西", "content": "買馬克杯", "is_completed": False},
    ]
    created = []

    for memo in memos:
        response = client.post("/api/v1/memos/", json=memo)
        assert response.status_code == status.HTTP_201_CREATED
        created.append(response.json())
    return created


def test_list_without_params(client: TestClient, seed_memos: list[dict]) -> None:
    response = client.get("/api/v1/memos/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 4
    assert len(data["items"]) == 4


def test_list_with_params(client: TestClient, seed_memos: list[dict]) -> None:
    response = client.get("/api/v1/memos/", params={"limit": 2})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 4
    assert len(data["items"]) == 2


def test_list_pages_do_not_overlap(client: TestClient, seed_memos: list[dict]) -> None:
    page1 = client.get("/api/v1/memos/", params={"skip": 0, "limit": 2}).json()["items"]
    page2 = client.get("/api/v1/memos/", params={"skip": 2, "limit": 2}).json()["items"]
    ids1 = {memo["id"] for memo in page1}
    ids2 = {memo["id"] for memo in page2}
    assert ids1.isdisjoint(ids2)  # 兩頁沒有重複
    assert len(ids1 | ids2) == 4  # 加起來 = 4


def test_list_skip_all(client: TestClient, seed_memos: list[dict]) -> None:
    response = client.get("/api/v1/memos/", params={"skip": 4})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 4
    assert data["items"] == []


def test_list_empty_base(client: TestClient) -> None:
    response = client.get("/api/v1/memos/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_filter_completed_true(client: TestClient, seed_memos: list[dict]) -> None:
    response = client.get("/api/v1/memos/", params={"is_completed": True})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "德文相關"


def test_filter_completed_false(client: TestClient, seed_memos: list[dict]) -> None:
    response = client.get("/api/v1/memos/", params={"is_completed": False})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 3
    assert all(memo["is_completed"] is False for memo in data["items"])


@pytest.mark.parametrize(
    ("keyword", "expected_titles"),
    [
        ("OS", {"OS"}),
        ("馬克杯", {"買東西"}),
        ("複習", {"德文相關", "OS"}),
        ("xyz", set()),
    ],
)
def test_search(
    client: TestClient,
    seed_memos: list[dict],
    keyword: str,
    expected_titles: set[str],
) -> None:
    response = client.get("/api/v1/memos/", params={"search": keyword})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == len(expected_titles)
    assert {memo["title"] for memo in data["items"]} == expected_titles


def test_search_empty_string_returns_all(
    client: TestClient, seed_memos: list[dict]
) -> None:
    response = client.get("/api/v1/memos/", params={"search": ""})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 4


def test_filter_and_search_combined(client: TestClient, seed_memos: list[dict]) -> None:
    response = client.get(
        "/api/v1/memos/", params={"is_completed": False, "search": "複習"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "OS"


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"limit": 101},
        {"skip": -1},
        {"limit": "abc"},
        {"is_completed": "abc"},
    ],
)
def test_list_invalid_params(client: TestClient, params: dict) -> None:
    response = client.get("/api/v1/memos/", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_only_sent_fields(client: TestClient, seed_memos: list[dict]) -> None:
    original = seed_memos[1]  # 拿OS的
    response = client.patch(
        f"/api/v1/memos/{original['id']}", json={"is_completed": True}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["is_completed"] is True
    assert data["title"] == original["title"]
    assert data["content"] == original["content"]
    assert data["priority"] == original["priority"]


def test_update_content_to_null(client: TestClient, seed_memos: list[dict]) -> None:
    memo_id = seed_memos[2]["id"]
    response = client.patch(f"/api/v1/memos/{memo_id}", json={"content": None})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["content"] is None


@pytest.mark.parametrize(
    "payload",
    [
        {"title": None},
        {"title": ""},
        {"is_completed": None},
        {"priority": None},
        {"priority": 99},
    ],
)
def test_update_invalid_payload(
    client: TestClient, seed_memos: list[dict], payload: dict
) -> None:
    memo_id = seed_memos[3]["id"]
    response = client.patch(f"/api/v1/memos/{memo_id}", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_not_found(client: TestClient) -> None:
    response = client.patch("/api/v1/memos/99", json={"is_completed": True})
    assert response.status_code == status.HTTP_404_NOT_FOUND
