# NCCUpass Memo Service (政大通備忘錄系統 API) 🚀

歡迎來到 **國立政治大學 政大通（NCCUpass）** 後端團隊！
這是一個專門為後端新人打造的 Onboarding 實戰任務基底專案（Starter Template）。

本專案已經預先為你配置好了 **FastAPI 應用骨架、SQLAlchemy 2.0 ORM、Pydantic 設定管理、SQLite In-Memory 測試環境** 等基礎設施。你的任務是專注於實作與完善 **Pydantic Schemas、CRUD 資料庫存取層、API 路由端點與自動化測試案例**。

---

## 🛠 技術棧規格

- **語言**：Python 3.11+
- **Web 框架**：FastAPI >= 0.110.0
- **ASGI 伺服器**：Uvicorn
- **ORM / 資料庫**：SQLAlchemy 2.0+ (Mapped Declarative)
- **資料庫**：
  - 開發環境：SQLite（開箱即用）
  - 測試環境：SQLite In-Memory（自動隔離）
- **資料驗證與設定**：Pydantic v2 + Pydantic Settings
- **測試框架**：pytest, httpx

---

## 📁 專案目錄架構

```text
nccupass-memo-service/
├── .env.example             # 環境變數設定範例
├── .gitignore               # Git 忽略檔案清單
├── requirements.txt         # 專案套件相依清單
├── README.md                # 專案說明與任務指引文件
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 實例、生命週期、路由註冊、Health check
│   ├── database.py          # SQLAlchemy Engine 與 SessionLocal
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Settings 類別 (讀取 DATABASE_URL, API_V1_STR 等)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # get_db 依賴注入項
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py       # 整合所有 v1 模組路由
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── memos.py # 備忘錄 API 路由端點
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py          # SQLAlchemy Declarative Base
│   │   └── memo.py          # Memo SQLAlchemy ORM 資料庫模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── memo.py          # Pydantic 資料驗證與轉換模型
│   └── crud/
│       ├── __init__.py
│       └── crud_memo.py     # 資料庫存取層函式 (CRUD)
└── tests/
    ├── __init__.py
    ├── conftest.py          # SQLite in-memory 測試 DB 與 TestClient Fixture
    ├── test_health.py       # 健康檢查測試端點
    └── test_memos.py        # 備忘錄 API 實戰測試案例
```

---

## ⚡ 快速開始 (Quickstart)

### 1. 建立並啟用 Python 虛擬環境

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2. 安裝相依套件

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. 設定環境變數

本專案使用 `pydantic-settings` 統一管理設定（定義於 `app/core/config.py`），在應用程式啟動時會自動讀取根目錄下的 `.env` 檔案以覆蓋預設值。

從 `.env.example` 複製一份 `.env`：

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

#### ⚙️ 環境變數清單與說明

| 變數名稱 | 預設值 | 說明 |
| :--- | :--- | :--- |
| `PROJECT_NAME` | `政大通備忘錄系統` | 專案名稱，用於 API 根目錄訊息與 Swagger / OpenAPI 文件標題 |
| `API_V1_STR` | `/api/v1` | API v1 路由前綴（例如 `/api/v1/memos`） |
| `DATABASE_URL` | `sqlite:///./sql_app.db` | 資料庫連線字串。支援 SQLite、PostgreSQL、MySQL 等 SQLAlchemy 連線 URL |

> 💡 **補充說明**：
> - **開箱即用**：若未建立 `.env` 檔案，專案仍會自動採用 `config.py` 中的預設值（使用本地 SQLite 資料庫），不會造成啟動失敗。
> - **環境隔離**：在不同環境（如本機開發、測試機或正式部署）切換資料庫或修改設定時，只需調整 `.env` 檔案，無須修改任何 Python 程式碼。


---

### 4. 啟動開發伺服器

```bash
uvicorn app.main:app --reload
```

伺服器啟動後即可存取：
- **服務首頁**：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **健康檢查**：[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **互動式 API 文件 (Swagger UI)**：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc API 文件**：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 5. 執行自動化測試

```bash
pytest
```

若需輸出詳細資訊：
```bash
pytest -v -s
```

---

## 🎯 新人實戰任務與待實作檔案清單

專案已預先建置好資料庫模型（`app/models/memo.py`）與測試環境配置（`tests/conftest.py`）。新手需依序完成以下 4 個核心檔案的實作：

| 任務編號 | 待實作檔案 | 職責與實作內容 |
| :---: | :--- | :--- |
| **任務 1** | [`app/schemas/memo.py`](file:///d:/ProgramingProject/NCCUpass/nccupass-memo-service/app/schemas/memo.py) | **Pydantic Schemas 定義**：定義 `MemoBase`, `MemoCreate`, `MemoUpdate`, `MemoResponse`, `MemoListResponse` 模型與欄位驗證。 |
| **任務 2** | [`app/crud/crud_memo.py`](file:///d:/ProgramingProject/NCCUpass/nccupass-memo-service/app/crud/crud_memo.py) | **資料庫存取層 (CRUD)**：實作 `create_memo`, `get_memo`, `get_memos`（支援分頁、完成狀態篩選、關鍵字搜尋）、`update_memo`, `delete_memo`。 |
| **任務 3** | [`app/api/v1/endpoints/memos.py`](file:///d:/ProgramingProject/NCCUpass/nccupass-memo-service/app/api/v1/endpoints/memos.py) | **API 路由端點**：實作 RESTful API 端點（`POST /`, `GET /`, `GET /{id}`, `PATCH /{id}`, `DELETE /{id}`），搭配 HTTP 狀態碼與 404 異常處理。 |
| **任務 4** | [`tests/test_memos.py`](file:///d:/ProgramingProject/NCCUpass/nccupass-memo-service/tests/test_memos.py) | **自動化測試案例**：使用 `pytest` 與 `client` (TestClient) 撰寫新增、查詢、更新、刪除及邊界情況（404 等）之測試案例。 |

### 🛠️ 建議實作流程

```text
[步驟 1] app/schemas/memo.py      ➔ 定義資料輸入與輸出結構 (Pydantic)
   ⬇
[步驟 2] app/crud/crud_memo.py    ➔ 撰寫 SQLAlchemy 資料庫查詢與操作邏輯
   ⬇
[步驟 3] app/api/v1/endpoints/memos.py ➔ 串接 Router、依賴注入 (get_db) 與 HTTP 錯誤處理
   ⬇
[步驟 4] tests/test_memos.py      ➔ 撰寫測試案例並執行 pytest 驗證所有測試綠燈
```

---

## 📋 備忘錄系統 API 規格書 (API Specification)

- **Base URL**：`http://localhost:8000/api/v1`
- **Content-Type**：`application/json; charset=utf-8`

### 1. 建立備忘錄
- **Endpoint**: `POST /memos`
- **Status Code**: `201 Created`
- **Request Body**:
  ```json
  {
    "title": "資結期末專案討論",
    "content": "討論後端架構設計與 ER Model",
    "priority": 4
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": 10,
    "title": "資結期末專案討論",
    "content": "討論後端架構設計與 ER Model",
    "priority": 4,
    "is_completed": false,
    "created_at": "2026-09-07T14:30:00Z",
    "updated_at": "2026-09-07T14:30:00Z"
  }
  ```

---

### 2. 查詢備忘錄列表 (分頁與過濾)
- **Endpoint**: `GET /memos`
- **Status Code**: `200 OK`
- **Query Parameters**:
  - `skip` (整數，預設 `0`)：跳過前幾筆
  - `limit` (整數，預設 `20`，最大 `100`)：取得筆數
  - `is_completed` (布林值，選填)：`true` 或 `false`
  - `search` (字串，選填)：搜尋標題或內容關鍵字
- **Response (200 OK)**:
  ```json
  {
    "total": 1,
    "items": [
      {
        "id": 10,
        "title": "資結期末專案討論",
        "content": "討論後端架構設計與 ER Model",
        "priority": 4,
        "is_completed": false,
        "created_at": "2026-09-07T14:30:00Z",
        "updated_at": "2026-09-07T14:30:00Z"
      }
    ]
  }
  ```

---

### 3. 取得單筆備忘錄
- **Endpoint**: `GET /memos/{id}`
- **Path Parameter**: `id` (整數)
- **Status Code**: `200 OK`（找不到時回傳 `404 Not Found`）
- **Response (200 OK)**:
  ```json
  {
    "id": 10,
    "title": "資結期末專案討論",
    "content": "討論後端架構設計與 ER Model",
    "priority": 4,
    "is_completed": false,
    "created_at": "2026-09-07T14:30:00Z",
    "updated_at": "2026-09-07T14:30:00Z"
  }
  ```

---

### 4. 更新備忘錄 (部分更新)
- **Endpoint**: `PATCH /memos/{id}`
- **Path Parameter**: `id` (整數)
- **Status Code**: `200 OK`（找不到時回傳 `404 Not Found`）
- **Request Body** (所有欄位皆選填):
  ```json
  {
    "is_completed": true,
    "priority": 2
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "id": 10,
    "title": "資結期末專案討論",
    "content": "討論後端架構設計與 ER Model",
    "priority": 2,
    "is_completed": true,
    "created_at": "2026-09-07T14:30:00Z",
    "updated_at": "2026-09-07T15:10:00Z"
  }
  ```

---

### 5. 刪除備忘錄
- **Endpoint**: `DELETE /memos/{id}`
- **Path Parameter**: `id` (整數)
- **Status Code**: `204 No Content`（找不到時回傳 `404 Not Found`）
- **Response**: 無回傳 Body

---

## 💡 開發規範與建議

1. **型別標註 (Type Hints)**：所有函式參數與回傳值均需標註清晰型別。
2. **錯誤處理**：在 Router 層找不到資源時，一律使用 `raise HTTPException(status_code=404, detail="...")`。
3. **資料庫交易**：在 CRUD 層進行 `db.commit()` 與 `db.refresh()`，並由依賴注入 `get_db()` 在請求結束時關閉連線。
4. **測試覆蓋**：每次新增功能後，務必執行 `pytest` 確保所有測試案例皆能綠燈通過！

