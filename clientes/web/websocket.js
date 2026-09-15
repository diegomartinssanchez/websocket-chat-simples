import { addMessage, updateRoomLabel, updateStatus } from './ui.js';

const params = new URLSearchParams(window.location.search);
const sala = params.get('sala') || 'geral';
const wsUrl = `ws://${window.location.host}/chat?sala=${encodeURIComponent(sala)}`;
let ws;

export function connect() {
    updateRoomLabel(sala);
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        updateStatus(true, `Conectado na sala "${sala}"`);
        addMessage("Sistema", `Conexão estabelecida com a sala "${sala}" via WebSockets nativos.`, "servidor");
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            addMessage(data.remetente, data.conteudo, "servidor");
        } catch (e) {
            console.error("Erro ao fazer o parse da mensagem JSON", e);
        }
    };

    ws.onclose = () => {
        updateStatus(false, "Offline (Tentando reconectar...)");
        addMessage("Sistema", `Conexão perdida na sala "${sala}". Reconectando em 3 segundos...`, "servidor");
        setTimeout(connect, 3000);
    };

    ws.onerror = (error) => {
        console.error("Erro capturado no Canal WebSocket:", error);
    };
}

export function sendMessage(remetente, texto) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        const payload = {
            remetente: remetente,
            conteudo: texto
        };
        ws.send(JSON.stringify(payload));
        return payload;
    }
    return null;
}
