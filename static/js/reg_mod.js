document.addEventListener("DOMContentLoaded", () => {
  const regBtn = document.getElementById("reg-btn");
  const regModal = document.getElementById("registerModal");
  const cancelBtn = document.getElementById("register-cancel");
  const regForm = document.getElementById("register-form");

  // открыть модалку
  regBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    regModal.showModal();
  });

  // закрыть модалку
  cancelBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    regModal.close();
  });

  // сабмит формы
  regForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(regForm);

    try {
      const resp = await fetch("/api/v1/registration/", {
        method: "POST",
        body: formData,
      });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        alert("Ошибка: " + (err.detail || resp.status));
        return;
      }

      alert("Регистрация успешна!");
      regModal.close();
      // window.location.reload(); // если нужно
    } catch (err) {
      alert("Ошибка соединения: " + err);
    }
  });
});
