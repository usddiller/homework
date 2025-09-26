document.addEventListener("DOMContentLoaded", () => {
    const btn1 = document.getElementById("btn1");
    const btn2 = document.getElementById("btn2");
    const access = localStorage.getItem("access");

    if (access) {
        btn1.textContent = "Профиль";
        btn1.id = "profile-btn";
        btn1.href = "/profile/";
      
        btn2.textContent = "Выйти";
        btn2.id = "logout-btn";
    } else {
        btn1.textContent = "Войти";
        btn1.id = "login-btn";
  
        btn2.textContent = "Регистрация";
        btn2.id = "reg-btn";
    }

    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", (e) => {
            e.preventDefault();
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            window.location.href = "/"; // редирект на главную
        });
    }
});