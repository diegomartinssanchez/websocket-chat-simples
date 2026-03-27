# WebSocket Chat (Tornado Assíncrono)

A mesma base didática do chat interativo, mas agora utilizando o protocolo **WebSocket** em conjunto com o framework de alta performance **Tornado**! 

Ele introduz o modelo de **Duplex Completo (Assíncrono)**; o que significa que diferentemente do modelo sequencial travado, **ninguém precisa aguardar pela resposta do outro**. O recebimento de rede e o console local rodam paralelamente sem bloqueios.

## 📌 Arquitetura

O chat agora é gerido num formato orientado a eventos no clássico Loop (`IOLoop`):
- O **Tornado Web** (`tornado.web.Application`) instanciou um *Handler* persistente (`/chat`) na especificação WebSocket.
- O Terminal do servidor e do cliente rodam uma *coroutine* poderosa (`asyncio.to_thread`) que lê o teclado simultaneamente à placa de rede.
- O payload de protocolo agora codifica os bytes numa `String` limpa em memória ao invés de bytes transientes.

## 📂 Estrutura de Arquivos

* **`backend/`**: Contém o `servidor.py`, que roda o servidor WebSocket Tornado.
* **`clientes/console.py`**: O cliente Python Terminal em si usando `websocket_connect()`.
* **`clientes/web/`**: A bela Interface Gráfica Glassmorphism provida pelo próprio Tornado no Root URL.

## 🚀 Como Executar

### 1. Instale o Tornado
Se ainda não possuir, instale o único requerimento mapeado no ecossistema atual:
```bash
pip install -r requirements.txt
```

### 2. Inicie o Servidor e o Client
Com a nova arquitetura de pacotes e a presença do `__init__.py`, executamos a partir da raiz do repositório garantindo que as bibliotecas cruzem de forma correta (`-m`).

**Terminal 1:**
```bash
python -m backend.servidor
```
**Terminal 2:** Abra o navegador em `http://localhost:8080/` OU execute a CLI local:
```bash
python -m clientes.console
```

## 🧪 Validando a Qualidade (Testes)

O framework de testes está suportado via `pytest` com Mocks de terminal de rede. O sistema cobre todos os eventos base (Conexão, Decodificação e Mensageria Assíncrona).

Para executa-los localmente:
```bash
pip install pytest pytest-cov pytest-asyncio
pytest tests/ --cov=backend --cov=clientes.console
```
*A GitHub Action implementada atestará o Deploy Continuamente após cada envio `Push` pro main.*
