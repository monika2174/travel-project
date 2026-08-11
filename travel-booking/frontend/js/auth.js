function getToken() {
  return localStorage.getItem("token");
}

function setAuth(data) {
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("role", data.role);
  localStorage.setItem("user_id", data.user_id);
  localStorage.setItem("full_name", data.full_name);
}

function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}

function requireAuth(roles = null) {
  const token = getToken();
  if (!token) {
    window.location.href = "login.html";
    return false;
  }
  if (roles && !roles.includes(localStorage.getItem("role"))) {
    alert("Access denied for your role.");
    window.location.href = "index.html";
    return false;
  }
  return true;
}

function updateNavAuth() {
  const authButtons = document.getElementById("authButtons");
  if (!authButtons) return;
  const token = getToken();
  if (token) {
    const name = localStorage.getItem("full_name") || "User";
    const role = localStorage.getItem("role");
    authButtons.innerHTML = `
      <span class="text-white me-3 d-none d-md-inline">Hi, ${name}</span>
      <a href="dashboard.html" class="btn btn-outline-light btn-sm me-2">Dashboard</a>
      <button class="btn btn-danger btn-sm" onclick="logout()">Logout</button>
    `;
  }
}

document.addEventListener("DOMContentLoaded", updateNavAuth);
