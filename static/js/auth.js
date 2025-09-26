const form = document.querySelector(".auth_form");

form.addEventListener("submit", async (e) => {
    e.preventDefault(); 
    const payload = {
        username: form.username.value,
        password: form.password.value
    };
    try {
        const response = await fetch("/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            throw new Error(`Ошибка ${response.status}`);
        }
        const data = await response.json();
        console.log("Успешный логин:", data);
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
    } catch (err) {
        console.error("Ошибка при запросе:", err);
    }
});