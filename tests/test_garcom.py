import pytest
from unittest.mock import Mock

from garcom import Garcom
from cozinha import Cozinha

def test_recebe_pedido():
    cozinha = Cozinha()
    garcom = Garcom(cozinha)

    garcom._exibir_pedido = Mock()
    cliente = Mock()
    pedido = Mock()

    cliente.comunicar_pedido.return_value = pedido

    garcom.notificar_pedido(cliente)
    garcom.coletar_pedidos()

    assert pedido in garcom.pedidos_em_andamento


@pytest.fixture
def garcom_com_pedido_anotado():
    cozinha = Cozinha()
    garcom = Garcom(cozinha)
    
    garcom._mostrar_pedido = Mock()
    cliente = Mock()
    pedido = Mock()

    cliente.comunicar_pedido.return_value = pedido

    garcom.notificar_pedido(cliente)
    garcom.coletar_pedidos()

    return garcom


def test_envia_pedido_para_cozinha(garcom_com_pedido_anotado):
    pedido = garcom_com_pedido_anotado.pedidos_em_andamento[0]

    garcom_com_pedido_anotado.cozinha.receber_pedido = Mock()

    garcom_com_pedido_anotado._enviar_para_cozinha(pedido)

    garcom_com_pedido_anotado.cozinha.receber_pedido.assert_called_once_with(pedido)