import os
import tornado.testing
import tornado.web
import tornado.websocket
import json
from backend.servidor import ChatHandler
import asyncio

class TestWebSocketServer(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        # Moca o diretório web para o StaticFileHandler
        dir_atual = os.path.dirname(os.path.abspath(__file__))
        dir_web = os.path.join(dir_atual, "..", "cliente_web")
        return tornado.web.Application([
            (r"/chat", ChatHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": dir_web, "default_filename": "index.html"}),
        ])

    @tornado.testing.gen_test
    async def test_websocket_conexao(self):
        ws_url = "ws://localhost:" + str(self.get_http_port()) + "/chat"
        ws_client = await tornado.websocket.websocket_connect(ws_url)
        
        payload = json.dumps({"remetente": "TestClient", "conteudo": "Ping"})
        await ws_client.write_message(payload)
        
        ws_client.close()
        assert True, "Conexão de teste finalizou limpa"
