import os
from logging import Logger

import tornado.ioloop
import tornado.web

from logger import configurar_logger, obter_logger
from servidor import ChatHandler

log_servidor: Logger = obter_logger("Servidor")

def iniciar_servidor() -> None:
    dir_atual: str = os.path.dirname(os.path.abspath(__file__))
    dir_web: str = os.path.join(dir_atual, "clientes", "web")
    
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
