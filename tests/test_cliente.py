import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cliente_console'))
import pytest
from unittest.mock import AsyncMock, patch
import asyncio
from cliente import receber_mensagens, ler_terminal

@pytest.mark.asyncio
async def test_receber_mensagens():
    conexao_mock = AsyncMock()
    # Retorna uma mensagem e depois None simulando fechamento
    conexao_mock.read_message.side_effect = ['{"remetente": "S", "conteudo": "Oi"}', None]
    
    await receber_mensagens(conexao_mock)
    assert conexao_mock.read_message.call_count == 2

@pytest.mark.asyncio
async def test_ler_terminal_sair():
    conexao_mock = AsyncMock()
    # Testa comando 'sair' finalizando a conexao localmente
    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_input:
        mock_input.return_value = 'sair'
        await ler_terminal(conexao_mock)
        conexao_mock.close.assert_called_once()
