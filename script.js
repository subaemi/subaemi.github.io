const openLoginPanelBtn = document.getElementById('openLoginPanel');
const loginPanel = document.getElementById('loginPanel');
const closePanelBtn = document.querySelector('.close-panel');
const loginForm = document.getElementById('loginForm');
const messageContainer = document.getElementById('messageContainer');

openLoginPanelBtn.addEventListener('click', () => {
    loginPanel.classList.add('active');
});

closePanelBtn.addEventListener('click', () => {
    loginPanel.classList.remove('active');
});

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    messageContainer.innerHTML = ''; // Очищаем предыдущие сообщения

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('YOUR_SERVER_ENDPOINT', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            messageContainer.innerHTML = '<p style="color:green;">Успешный вход!</p>';
            // Перенаправление на другую страницу после успешного входа
            window.location.href = 'success.html'; // Замените 'success.html' на нужную страницу
        } else {
            messageContainer.innerHTML = `<p style="color:red;">${data.message || 'Ошибка входа'}</p>`;
        }
    } catch (error) {
        messageContainer.innerHTML = `<p style="color:red;">Ошибка: ${error.message}</p>`;
    }
});