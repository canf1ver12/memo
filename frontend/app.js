const API = "/api/v1/memos";
const PAGE_SIZE = 10;

const state = { page: 0, total: 0, search: "", isCompleted: "" };

const $ = (id) => document.getElementById(id);
const form = $("memo-form");
const list = $("memo-list");
const tpl = $("memo-item");

async function request(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(formatError(data, res.status));
  return data;
}

function formatError(data, status) {
  const detail = data && data.detail;
  if (Array.isArray(detail)) {
    return detail.map((d) => `${d.loc.slice(1).join(".")}: ${d.msg}`).join("；");
  }
  if (typeof detail === "string") return detail;
  return `HTTP ${status}`;
}

// SQLite 的 CURRENT_TIMESTAMP 是 UTC 但不帶時區，補上 Z 避免被當成本地時間
function parseUtc(value) {
  return new Date(/[zZ]|[+-]\d{2}:\d{2}$/.test(value) ? value : `${value}Z`);
}

function showError(el, message) {
  el.textContent = message;
  el.hidden = !message;
}

async function checkHealth() {
  const el = $("health");
  try {
    const data = await request("/health");
    el.textContent = `● ${data.database}`;
    el.className = "health ok";
  } catch {
    el.textContent = "● 無法連線";
    el.className = "health bad";
  }
}

async function loadMemos() {
  const params = new URLSearchParams({
    skip: state.page * PAGE_SIZE,
    limit: PAGE_SIZE,
  });
  if (state.search) params.set("search", state.search);
  if (state.isCompleted) params.set("is_completed", state.isCompleted);

  try {
    const data = await request(`${API}/?${params}`);
    // 刪除最後一筆後該頁可能變空，退回上一頁
    if (data.items.length === 0 && state.page > 0 && data.total > 0) {
      state.page -= 1;
      return loadMemos();
    }
    state.total = data.total;
    renderList(data.items);
    showError($("list-error"), "");
  } catch (err) {
    showError($("list-error"), `載入失敗：${err.message}`);
  }
}

function renderList(items) {
  list.replaceChildren(...items.map(renderItem));
  $("empty").hidden = items.length > 0;

  const pages = Math.max(1, Math.ceil(state.total / PAGE_SIZE));
  $("page-info").textContent = `第 ${state.page + 1} / ${pages} 頁 · 共 ${state.total} 筆`;
  $("prev-btn").disabled = state.page === 0;
  $("next-btn").disabled = state.page + 1 >= pages;
}

function renderItem(memo) {
  const li = tpl.content.firstElementChild.cloneNode(true);
  li.classList.toggle("done", memo.is_completed);
  li.querySelector(".title").textContent = memo.title;
  li.querySelector(".content").textContent = memo.content || "";

  const badge = li.querySelector(".badge");
  badge.textContent = `P${memo.priority}`;
  badge.classList.add(`p${memo.priority}`);

  const meta = li.querySelector(".meta");
  meta.dateTime = memo.updated_at;
  meta.textContent = `更新於 ${parseUtc(memo.updated_at).toLocaleString("zh-TW")}`;

  const toggle = li.querySelector(".toggle");
  toggle.checked = memo.is_completed;
  toggle.addEventListener("change", async () => {
    try {
      await request(`${API}/${memo.id}`, {
        method: "PATCH",
        body: JSON.stringify({ is_completed: toggle.checked }),
      });
      loadMemos();
    } catch (err) {
      toggle.checked = !toggle.checked;
      showError($("list-error"), `更新失敗：${err.message}`);
    }
  });

  li.querySelector(".edit").addEventListener("click", () => startEdit(memo));
  li.querySelector(".delete").addEventListener("click", async () => {
    if (!confirm(`確定刪除「${memo.title}」？`)) return;
    try {
      await request(`${API}/${memo.id}`, { method: "DELETE" });
      if (String(memo.id) === $("memo-id").value) resetForm();
      loadMemos();
    } catch (err) {
      showError($("list-error"), `刪除失敗：${err.message}`);
    }
  });
  return li;
}

function startEdit(memo) {
  $("memo-id").value = memo.id;
  $("title").value = memo.title;
  $("content").value = memo.content || "";
  $("priority").value = String(memo.priority);
  $("is-completed").checked = memo.is_completed;
  $("form-title").textContent = `編輯備忘錄 #${memo.id}`;
  $("submit-btn").textContent = "儲存";
  $("cancel-btn").hidden = false;
  showError($("form-error"), "");
  $("title").focus();
}

function resetForm() {
  form.reset();
  $("memo-id").value = "";
  $("form-title").textContent = "新增備忘錄";
  $("submit-btn").textContent = "新增";
  $("cancel-btn").hidden = true;
  showError($("form-error"), "");
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = $("memo-id").value;
  const content = $("content").value.trim();
  const payload = {
    title: $("title").value.trim(),
    content: content || null,
    priority: Number($("priority").value),
    is_completed: $("is-completed").checked,
  };

  try {
    if (id) {
      await request(`${API}/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
    } else {
      await request(`${API}/`, { method: "POST", body: JSON.stringify(payload) });
      state.page = 0;
    }
    resetForm();
    loadMemos();
  } catch (err) {
    showError($("form-error"), err.message);
  }
});

$("cancel-btn").addEventListener("click", resetForm);

let searchTimer;
$("search").addEventListener("input", (e) => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    state.search = e.target.value.trim();
    state.page = 0;
    loadMemos();
  }, 300);
});

$("filter").addEventListener("change", (e) => {
  state.isCompleted = e.target.value;
  state.page = 0;
  loadMemos();
});

$("prev-btn").addEventListener("click", () => {
  state.page -= 1;
  loadMemos();
});
$("next-btn").addEventListener("click", () => {
  state.page += 1;
  loadMemos();
});

checkHealth();
loadMemos();
