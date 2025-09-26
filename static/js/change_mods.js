document.addEventListener("DOMContentLoaded", () => {
  const loginModal = document.getElementById("loginModal");
  const registerModal = document.getElementById("registerModal");

  const openRegisterBtn = document.getElementById("open-register");
  const openLoginBtn = document.getElementById("open-login");

  // открыть регистрацию из логина
  if (openRegisterBtn) {
    openRegisterBtn.addEventListener("click", () => {
      loginModal.close();
      registerModal.showModal();
    });
  }

  // открыть логин из регистрации
  if (openLoginBtn) {
    openLoginBtn.addEventListener("click", () => {
      registerModal.close();
      loginModal.showModal();
    });
  }
});
