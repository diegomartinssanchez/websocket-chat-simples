const wsUrl = `ws://${window.location.host}/chat`;
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const statusIndicator = document.getElementById("status-indicator");
const statusText = document.getElementById("status-text");

let ws;

function connect() {
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        statusIndicator.classList.add("connected");
        statusText.textContent = "Conexão Instanciada";
        addMessage("Sistema", "Conexão estabalecida com o Tornado via WebSockets nativos.", "servidor");
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            // Mensagens vindas do socket sempre pintamos à esquerda como "servidor" no layout
            addMessage(data.remetente, data.conteudo, "servidor");
        } catch (e) {
            console.error("Erro ao fazer o parse da mensagem JSON", e);
        }
    };

    ws.onclose = () => {
        statusIndicator.classList.remove("connected");
        statusText.textContent = "Offline (Tentando reconectar...)";
        addMessage("Sistema", "Conexão perdida. Reconectando em 3 Segundos...", "servidor");
        setTimeout(connect, 3000);
    };

    ws.onerror = (error) => {
        console.error("Erro capturado no Canal WebSocket:", error);
    };
}

function addMessage(remetente, conteudo, tipo) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${tipo}`;

    const senderDiv = document.createElement("div");
    senderDiv.className = "sender";
    senderDiv.textContent = remetente;

    const contentDiv = document.createElement("div");
    contentDiv.className = "content";
    contentDiv.textContent = conteudo;

    msgDiv.appendChild(senderDiv);
    msgDiv.appendChild(contentDiv);

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
}

chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const texto = messageInput.value.trim();

    if (texto && ws && ws.readyState === WebSocket.OPEN) {
        const payload = {
            remetente: "Web Client",
            conteudo: texto
        };

        ws.send(JSON.stringify(payload));

        addMessage(payload.remetente, payload.conteudo, "cliente");
        messageInput.value = "";
    }
});

connect();
