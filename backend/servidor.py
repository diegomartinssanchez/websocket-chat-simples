import os
import asyncio
import tornado.web
import tornado.websocket
import tornado.ioloop
from logging import Logger

from shared.protocol import ChatMessage
from shared.logger import configurar_logger, obter_logger

log_servidor: Logger = obter_logger("Servidor")

class ChatHandler(tornado.websocket.WebSocketHandler):
    entrada_ativa: bool

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self) -> None:
        log_servidor.info("Conectado com um cliente WebSocket!")
        self.entrada_ativa = True
        # Inicia a leitura assíncrona do terminal - agenda na IOLoop
        tornado.ioloop.IOLoop.current().add_callback(self.ler_terminal)

    def on_message(self, message: str | bytes) -> None:
        if not message:
            return
        msg_recebida: ChatMessage = ChatMessage.decodificar(message)
        obter_logger(msg_recebida.remetente).info(msg_recebida.conteudo)

    def on_close(self) -> None:
        self.entrada_ativa = False
        log_servidor.info("Conexão encerrada pelo cliente.")

    async def ler_terminal(self) -> None:
        """ Rotina que lê o terminal do servidor de forma concorrente, sem matar o WebSocket """
        while self.entrada_ativa:
            try:
                texto: str = await asyncio.to_thread(input, "> ")
                if not self.entrada_ativa:
                    break
                if texto.lower() == 'sair':
                    self.close()
                    break
                if texto.strip():
                    msg_envio: ChatMessage = ChatMessage(remetente="Servidor", conteudo=texto)
                    await self.write_message(msg_envio.codificar())
            except EOFError:
                break
            except Exception as e:
                log_servidor.error(f"Erro no terminal do servidor: {e}")
                break

def iniciar_servidor() -> None:
    dir_atual: str = os.path.dirname(os.path.abspath(__file__))
    dir_web: str = os.path.join(dir_atual, "..", "cliente_web")
    
    app: tornado.web.Application = tornado.web.Application([
        (r"/chat", ChatHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": dir_web, "default_filename": "index.html"}),
    ])
    porta: int = 8080
    app.listen(porta)
    log_servidor.info(f"Escutando porta {porta} em ws://localhost:{porta}/chat")
    log_servidor.info(f"🚀 Interface Web GUI rodando em http://localhost:{porta}")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    configurar_logger()
    iniciar_servidor()
