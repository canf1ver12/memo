# Memo Service

一個以 FastAPI 實作的備忘錄 RESTful API，附帶一個免建置的網頁前端。

- 後端：建立、查詢、部分更新、刪除備忘錄，列表支援分頁、完成狀態篩選與關鍵字搜尋
- 前端：純 HTML/CSS/JS，由 FastAPI 直接掛載，啟動後端即可使用
- 測試：pytest 搭配 SQLite in-memory 資料庫，每個測試自動隔離

---

## 技術棧

- **語言**：Python 3.11+
- **Web 框架**：FastAPI >= 0.110.0
- **ASGI 伺服器**：Uvicorn
- **ORM**：SQLAlchemy 2.0+（Mapped Declarative）
- **資料庫**：
  - 開發環境：SQLite（開箱即用）
  - 測試環境：SQLite in-memory（自動隔離）
- **資料驗證與設定**：Pydantic v2 + pydantic-settings
- **測試**：pytest、httpx
- **前端**：HTML、CSS、JavaScript（無框架、無建置流程）

---

## 專案結構

```text
memo/
├── .env.example             # 環境變數設定範例
├── .gitignore
├── requirements.txt         # Python 套件相依清單
├── README.md
├── app/
│   ├── main.py              # FastAPI 實例、生命週期、路由註冊、health check、前端掛載
│   ├── database.py          # SQLAlchemy Engine 與 SessionLocal
│   ├── core/
│   │   └── config.py        # Settings（讀取 DATABASE_URL、API_V1_STR 等）
│   ├── api/
│   │   ├── deps.py          # get_db dependency
│   │   └── v1/
│   │       ├── api.py       # 整合 v1 路由
│   │       └── endpoints/
│   │           └── memos.py # 備忘錄 API endpoints
│   ├── models/
│   │   ├── base.py          # SQLAlchemy Declarative Base
│   │   └── memo.py          # Memo ORM model
│   ├── schemas/
│   │   └── memo.py          # Pydantic request / response schemas
│   └── crud/
│       └── crud_memo.py     # 資料庫存取層（CRUD）
├── frontend/
│   ├── index.html           # 前端頁面
│   ├── style.css            # 樣式（支援深色模式）
│   └── app.js               # 呼叫 API、渲染列表、表單處理
└── tests/
    ├── conftest.py          # SQLite in-memory 測試 DB 與 TestClient fixture
    ├── test_health.py       # 根路徑與 health check 測試
    ├── test_memos.py        # 建立、查詢、刪除測試
    └── test_memos_advanced.py # 分頁、篩選、搜尋與部分更新測試
```

---

## 快速開始

### 1. 建立並啟用 Python 虛擬環境

**Windows (PowerShell)：**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux：**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安裝相依套件

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 設定環境變數

設定由 `pydantic-settings` 統一管理（定義於 `app/core/config.py`），啟動時會自動讀取根目錄的 `.env` 覆蓋預設值。

```bash
cp .env.example .env
```

Windows (PowerShell) 請改用 `Copy-Item .env.example .env`。

| 變數名稱 | 預設值 | 說明 |
| :--- | :--- | :--- |
| `PROJECT_NAME` | 見 `app/core/config.py` | 專案名稱，用於根路徑訊息與 Swagger / OpenAPI 文件標題 |
| `API_V1_STR` | `/api/v1` | API v1 路由前綴（例如 `/api/v1/memos`） |
| `DATABASE_URL` | `sqlite:///./sql_app.db` | 資料庫連線字串，支援 SQLite、PostgreSQL、MySQL 等 SQLAlchemy URL |

沒有建立 `.env` 也能啟動，會直接使用 `config.py` 的預設值（本地 SQLite）。

### 4. 啟動開發伺服器

```bash
uvicorn app.main:app --reload
```

啟動後可以開啟：

| 頁面 | 網址 |
| :--- | :--- |
| 前端頁面 | http://127.0.0.1:8000/app/ |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| Health check | http://127.0.0.1:8000/health |
| 根路徑 | http://127.0.0.1:8000/ |

### 5. 執行測試

```bash
pytest
```

需要詳細輸出時：
```bash
pytest -v -s
```

---

## 前端

前端位於 `frontend/`，由 `app/main.py` 透過 FastAPI `StaticFiles` 掛載在 `/app`，與 API 同源，因此不需要設定 CORS，也不需要 `npm install`。

功能：

- 新增、編輯、刪除備忘錄，勾選切換完成狀態
- 關鍵字搜尋（輸入停頓 300ms 後送出）
- 依完成狀態篩選
- 分頁，每頁 10 筆
- 顯示後端回傳的驗證錯誤，以及 `/health` 連線狀態
- 跟隨系統設定切換深色模式

SQLite 的 `CURRENT_TIMESTAMP` 是 UTC 但不帶時區資訊，前端會補上 `Z` 再轉成本地時間顯示。

---

## API 規格

- **Base URL**：`http://localhost:8000/api/v1`
- **Content-Type**：`application/json; charset=utf-8`

### 欄位

| 欄位 | 型別 | 說明 |
| :--- | :--- | :--- |
| `id` | integer | 唯一識別碼，自動產生 |
| `title` | string | 必填，1 到 100 字 |
| `content` | string \| null | 選填，詳細內容 |
| `priority` | integer | 1（低）到 5（高），預設 `3` |
| `is_completed` | boolean | 預設 `false` |
| `created_at` | datetime | 建立時間（UTC） |
| `updated_at` | datetime | 最後更新時間（UTC） |

### 1. 建立備忘錄

- **Endpoint**：`POST /memos/`
- **Status Code**：`201 Created`
- **Request Body**：
  ```json
  {
    "title": "期末專案討論",
    "content": "討論後端架構設計與 ER Model",
    "priority": 4
  }
  ```
- **Response**：
  ```json
  {
    "id": 10,
    "title": "期末專案討論",
    "content": "討論後端架構設計與 ER Model",
    "priority": 4,
    "is_completed": false,
    "created_at": "2026-09-07T14:30:00",
    "updated_at": "2026-09-07T14:30:00"
  }
  ```

### 2. 查詢備忘錄列表

- **Endpoint**：`GET /memos/`
- **Status Code**：`200 OK`
- **Query Parameters**：
  - `skip`（整數，預設 `0`）：跳過前幾筆
  - `limit`（整數，預設 `20`，範圍 1 到 100）：取得筆數
  - `is_completed`（布林值，選填）：`true` 或 `false`
  - `search`（字串，選填）：搜尋標題或內容關鍵字
- **Response**：
  ```json
  {
    "total": 1,
    "items": [
      {
        "id": 10,
        "title": "期末專案討論",
        "content": "討論後端架構設計與 ER Model",
        "priority": 4,
        "is_completed": false,
        "created_at": "2026-09-07T14:30:00",
        "updated_at": "2026-09-07T14:30:00"
      }
    ]
  }
  ```

### 3. 取得單筆備忘錄

- **Endpoint**：`GET /memos/{id}`
- **Status Code**：`200 OK`，找不到時回傳 `404 Not Found`
- **Response**：與建立備忘錄的回應格式相同

### 4. 部分更新備忘錄

- **Endpoint**：`PATCH /memos/{id}`
- **Status Code**：`200 OK`，找不到時回傳 `404 Not Found`
- **Request Body**：所有欄位皆選填，只更新有傳入的欄位。`title`、`priority`、`is_completed` 不可設為 `null`（回傳 `422`）。
  ```json
  {
    "is_completed": true,
    "priority": 2
  }
  ```
- **Response**：更新後的完整備忘錄

### 5. 刪除備忘錄

- **Endpoint**：`DELETE /memos/{id}`
- **Status Code**：`204 No Content`，找不到時回傳 `404 Not Found`
- **Response**：無 body
