        document.querySelectorAll(".user-card").forEach(card => {
            card.addEventListener("click", async () => {
                const userId = card.dataset.userId;
                console.log("Открываю профиль:", userId);

                try {
                    const response = await fetch(`/api/v1/users/${userId}/`, {
                        headers: {
                            "Authorization": `Bearer ${access}`
                        }
                    });

                    if (!response.ok) {
                        throw new Error(`Ошибка ${response.status}`);
                    }

                    const userData = await response.json();
                    console.log("Детали пользователя:", userData);

                    // тут можешь перерисовать usersBlock под подробный профиль
                    usersBlock.innerHTML = `
                        <div class="p-4 border rounded-xl bg-white shadow">
                            <div class="flex items-center gap-4">
                                <div class="w-20 h-20 rounded-full overflow-hidden bg-gray-200">
                                    ${userData.avatar 
                                        ? `<img src="${userData.avatar}" alt="${userData.username}" class="w-full h-full object-cover">`
                                        : `<span class="flex items-center justify-center w-full h-full h-full text-gray-500">👤</span>`
                                    }
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold">${userData.username}</h2>
                                    <p class="text-gray-600">${userData.first_name} ${userData.last_name}</p>
                                </div>
                            </div>
                            <div class="mt-4">
                                <p class="text-gray-700">Email: ${userData.email ?? "не указан"}</p>
                                <p class="text-gray-700">ID: ${userData.id}</p>
                            </div>
                        </div>
                    `;
                } catch (err) {
                    console.error("Ошибка при получении пользователя:", err);
                }
            });
        });
