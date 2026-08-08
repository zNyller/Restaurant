from unittest.mock import MagicMock
from cliente import Cliente, Status

def test_realizar_pedido_chama_garcom():
    cliente = Cliente(nome="Ana")

    mesa_falsa = MagicMock()
    mesa_falsa.cardapio.prato_aleatorio.return_value = MagicMock(nome="Costela ao molho", tempo=20)
    mesa_falsa.cardapio.bebida_aleatoria.return_value = MagicMock(nome="Refrigerante")

    cliente._mesa = mesa_falsa
    cliente._status = Status.SENTOU

    cliente._realizar_pedido()

    # Verifica se o cliente de fato notificou a mesa
    mesa_falsa.chamar_garcom.assert_called_once()
    assert cliente._pedido is not None