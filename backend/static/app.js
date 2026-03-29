function $(id) {
  return document.getElementById(id);
}

const TOKEN_KEY = "sw_access_token";
const REFRESH_KEY = "sw_refresh_token";
const USER_KEY = "sw_user";

function setOut(el, data) {
  el.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setAuth({ access, refresh, user }) {
  if (access) localStorage.setItem(TOKEN_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
  renderAuthState();
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(USER_KEY);
  renderAuthState();
}

function getUser() {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function renderAuthState() {
  const token = getAccessToken();
  const user = getUser();

  if (token) {
    $("authState").textContent = "Logged in";
    $("logoutBtn").disabled = false;
    $("whoami").textContent = user ? `User: ${user.email} (id=${user.id})` : "User: (unknown)";
  } else {
    $("authState").textContent = "Logged out";
    $("logoutBtn").disabled = true;
    $("whoami").textContent = "";
  }
}

async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = getAccessToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const resp = await fetch(path, {
    ...options,
    headers,
  });

  let data;
  const contentType = resp.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    data = await resp.json();
  } else {
    data = await resp.text();
  }

  if (!resp.ok) {
    const msg = typeof data === "string" ? data : data.detail || JSON.stringify(data);
    throw new Error(`${resp.status} ${resp.statusText}: ${msg}`);
  }

  return data;
}

function bindForms() {
  $("logoutBtn").addEventListener("click", () => {
    clearAuth();
  });

  $("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    setOut($("registerOut"), "");

    const form = e.currentTarget;
    const payload = {
      email: form.email.value,
      password: form.password.value,
    };

    try {
      const data = await apiFetch("/api/accounts/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setOut($("registerOut"), data);
    } catch (err) {
      setOut($("registerOut"), String(err));
    }
  });

  $("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    setOut($("loginOut"), "");

    const form = e.currentTarget;
    const payload = {
      email: form.email.value,
      password: form.password.value,
    };

    try {
      const data = await apiFetch("/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      setAuth({ access: data.access, refresh: data.refresh, user: data.user });
      setOut($("loginOut"), data);
    } catch (err) {
      setOut($("loginOut"), String(err));
    }
  });

  $("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    setOut($("uploadOut"), "");

    const form = e.currentTarget;
    const fd = new FormData();
    if (!form.image.files[0]) {
      setOut($("uploadOut"), "Pick an image first.");
      return;
    }

    fd.append("image", form.image.files[0]);
    if (form.clothing_type.value) fd.append("clothing_type", form.clothing_type.value);
    if (form.color.value) fd.append("color", form.color.value);

    try {
      const data = await apiFetch("/api/wardrobe/items/upload/", {
        method: "POST",
        body: fd,
      });
      setOut($("uploadOut"), data);
    } catch (err) {
      setOut($("uploadOut"), String(err));
    }
  });

  $("recommendBtn").addEventListener("click", async () => {
    setOut($("recommendOut"), "");
    try {
      const data = await apiFetch("/api/wardrobe/recommend/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      setOut($("recommendOut"), data);
    } catch (err) {
      setOut($("recommendOut"), String(err));
    }
  });

  $("ratingForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    setOut($("ratingOut"), "");

    const form = e.currentTarget;
    const payload = {
      outfit_id: Number(form.outfit_id.value),
      rating: Number(form.rating.value),
    };

    try {
      const data = await apiFetch("/api/wardrobe/ratings/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setOut($("ratingOut"), data);
    } catch (err) {
      setOut($("ratingOut"), String(err));
    }
  });
}

renderAuthState();
bindForms();
