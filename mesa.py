from typing import TYPE_CHECKING
from cardapio import Cardapio

if TYPE_CHECKING:
    from cliente import Cliente
    from pedido import Pedido
    from garcom import Garcom

class Mesa:
    def __init__(self, numero: int):
        self.numero = numero
        self.ocupada = False
        self.cardapio: Cardapio = None
        self.cliente: "Cliente" = None
        self.garcom: "Garcom" = None
        self.pedido: "Pedido" = None
        self.pedido_registrado = False
        self.pedido_recebido = False


    def esta_livre(self) -> bool:
        return not self.ocupada


    def receber(self, cliente: "Cliente", cardapio: Cardapio, garcom: "Garcom") -> None:
        """Configura a mesa como ocupada e registra o cliente que está nela."""
        self.ocupada = True
        self.cliente = cliente
        self.cardapio = cardapio
        self.garcom = garcom
        self.cliente.sentar()
        self.cliente.ocupar(self)


    def registrar_pedido(self, pedido: "Pedido") -> None:
        """Registra e vincula o pedido feito à mesa atual."""
        self.pedido = pedido
        self.pedido_registrado = True
        self.pedido.vincular(self)


    def registrou_pedido(self) -> bool:
        return self.pedido_registrado


    def receber_pedido(self):
        self.pedido_recebido = True


    def recebeu_pedido(self) -> bool:
        return self.pedido_recebido


    def liberar(self) -> None:
        """Configura a mesa como liberada, remove o cliente e o pedido que estava nela."""
        self.ocupada = False
        self.cliente = None
        self.pedido = None