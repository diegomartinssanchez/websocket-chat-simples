import { connect, sendMessage } from './websocket.js';
import { addMessage } from './ui.js';

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const texto = messageInput.value.trim();

        if (texto) {
            const payload = sendMessage("Web Client", texto);
            if (payload) {
                messageInput.value = "";
            }
        }
    });

    connect();
});
