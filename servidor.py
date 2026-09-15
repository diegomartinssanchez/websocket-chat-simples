import asyncio
import sys
from logging import Logger

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from logger import obter_logger
from protocolo import ChatMessage

log_servidor: Logger = obter_logger("Servidor")


class ChatHandler(WebSocketHandler):
    entrada_ativa: bool
    salas: dict[str, set["ChatHandler"]] = {}

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self) -> None:
        self.sala: str = self.get_argument("sala", "geral")
        self.entrada_ativa = True

        self.__class__.salas.setdefault(self.sala, set()).add(self)
        log_servidor.info("Conectado com um cliente WebSocket na sala '%s'!", self.sala)

        if sys.stdin and sys.stdin.isatty():
            IOLoop.current().add_callback(self.ler_terminal)

    def on_message(self, message: str | bytes) -> None:
        if not message:
            return

        msg_recebida: ChatMessage = ChatMessage.decodificar(message)
        obter_logger(msg_recebida.remetente).info(msg_recebida.conteudo)
        self.broadcast_para_sala(msg_recebida)

    def on_close(self) -> None:
        self.entrada_ativa = False
        if hasattr(self, "sala"):
            conexoes = self.__class__.salas.get(self.sala, set())
            conexoes.discard(self)
            if not conexoes:
                self.__class__.salas.pop(self.sala, None)
        log_servidor.info("Conexão encerrada pelo cliente na sala '%s'.", getattr(self, "sala", "desconhecida"))

    def broadcast_para_sala(self, mensagem: ChatMessage) -> None:
        for cliente in list(self.__class__.salas.get(self.sala, set())):
            try:
                if cliente is self or cliente.ws_connection is not None:
                    cliente.write_message(mensagem.codificar())
            except Exception as e:
                log_servidor.error(f"Erro ao encaminhar mensagem na sala '{self.sala}': {e}")

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
                    self.broadcast_para_sala(msg_envio)
            except EOFError:
                break
            except Exception as e:
                log_servidor.error(f"Erro no terminal do servidor: {e}")
                break
