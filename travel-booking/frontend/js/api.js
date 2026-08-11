async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    logout();
    throw new Error("Unauthorized");
  }

  let data = {};
  const text = await res.text();
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { detail: text };
  }

  if (!res.ok) {
    const msg = Array.isArray(data.detail)
      ? data.detail.map((d) => d.msg || d).join(", ")
      : data.detail || "Request failed";
    throw new Error(msg);
  }
  return data;
}

function starsHtml(rating) {
  let html = "";
  for (let i = 1; i <= 5; i++) {
    html += `<i class="bi bi-star${i <= rating ? "-fill" : ""}"></i>`;
  }
  return html;
}
