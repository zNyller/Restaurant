import pytest
from unittest.mock import MagicMock

from mesa import Mesa
from cliente import Cliente
from cardapio import Cardapio


def test_mesa_comeca_livre():
    mesa = Mesa(numero=1)
    assert mesa.esta_livre() is True


def test_liberar_mesa_reseta_estado():
    mesa = Mesa(numero=1)
    mesa.ocupada = True
    mesa.cliente = "qualquer coisa"
    mesa.pedido = "qualquer coisa"

    mesa.liberar()

    assert mesa.esta_livre() is True
    assert mesa.cliente is None
    assert mesa.pedido is None


def test_receber_cliente_ocupa_mesa():
    mesa = Mesa(numero=1)
    cliente = Cliente(nome="Ana")
    cardapio = Cardapio()

    mesa.receber(cliente, cardapio, garcom=None)

    assert mesa.esta_livre() is False
    assert mesa.cliente is cliente
    assert cliente.esta_sentado() is True

"""
Fixtures: parando de repetir Arrange

Repare que em quase todo teste acima você recria Mesa, Cliente e Cardapio do zero. 
Isso é repetição (e code smell, SOLID e testes se cruzam aqui). 
Fixtures resolvem isso.
"""

@pytest.fixture
def cardapio():
    return Cardapio()

@pytest.fixture
def mesa_livre():
    return Mesa(numero=1)

@pytest.fixture
def cliente_sentado(mesa_livre, cardapio):
    """Cliente já sentado numa mesa, pronto para testes de pedido."""
    cliente = Cliente(nome="Ana")
    garcom_falso = MagicMock()
    mesa_livre.receber(cliente, cardapio, garcom=garcom_falso)
    return cliente


def test_realizar_pedido_notifica_garcom():
    cliente_sentado.atualizar(minutos=10)
    cliente_sentado.mesa.garcom.notificar_pedido.assert_called_once_with(cliente_sentado)