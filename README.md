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

從 `.env.example` 複製一份 `.env`：

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

> **提示**：預設的 `.env` 配置使用 SQLite (`sqlite:///./sql_app.db`)，啟動時會自動建立資料庫檔案，無須額外安裝 MySQL 即可直接開發。

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


## 💡 開發規範與建議

1. **型別標註 (Type Hints)**：所有函式參數與回傳值均需標註清晰型別。
2. **錯誤處理**：在 Router 層找不到資源時，一律使用 `raise HTTPException(status_code=404, detail="...")`。
3. **資料庫交易**：在 CRUD 層進行 `db.commit()` 與 `db.refresh()`，並由依賴注入 `get_db()` 在請求結束時關閉連線。
4. **測試覆蓋**：每次新增功能後，務必執行 `pytest` 確保所有測試案例皆能綠燈通過！
