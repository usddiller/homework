document.addEventListener("DOMContentLoaded", () => {
  const loginBtn   = document.getElementById("login-btn");
  const loginModal = document.getElementById("loginModal");
  const cancelBtn  = document.getElementById("login-cancel");
  const form       = document.getElementById("login-form");
  const errorBox   = document.getElementById("error-box");

  // открыть модалку по кнопке в хедере
  if (loginBtn && loginModal) {
    loginBtn.addEventListener("click", (e) => {
      // если это <a>, гасим переход по href
      e.preventDefault();
      loginModal.showModal();
    });
  }

  // закрыть по крестику
  if (cancelBtn && loginModal) {
    cancelBtn.addEventListener("click", (e) => {
      e.preventDefault();
      loginModal.close();
    });
  }

  // сабмит формы
  if (form && loginModal) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = form.username.value.trim();
      const password = form.password.value;

      if (!username || !password) {
        return showError("Заполните логин и пароль");
      }

      try {
        const resp = await fetch("/api/token/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        if (!resp.ok) {
          const err = await resp.json().catch(() => ({}));
          return showError(err.detail || "Неверные учетные данные");
        }

        const data = await resp.json();
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        loginModal.close();
        window.location.reload(); // или window.location.href = "/profile/";
      } catch (e) {
        showError("Ошибка соединения с сервером");
      }
    });
  }

  function showError(msg) {
    if (!errorBox) return;
    errorBox.textContent = msg;
    errorBox.classList.remove("hidden");
  }
});
