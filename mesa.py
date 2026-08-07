from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cardapio import Cardapio
    from cliente import Cliente
    from pedido import Pedido
    from garcom import Garcom

class Mesa:
    def __init__(self, numero: int) -> None:
        self.numero = numero
        self.ocupada = False
        self.cardapio: Cardapio = None
        self.cliente: Cliente = None
        self.garcom: Garcom = None
        self.pedido: Pedido = None


    @property
    def esta_livre(self) -> bool:
        return not self.ocupada


    def receber(self, cliente: Cliente, cardapio: Cardapio, garcom: Garcom) -> None:
        """Configura a mesa como ocupada e registra o cliente que está nela."""
        self.ocupada = True
        self.cliente= cliente
        self.cardapio = cardapio
        self.garcom = garcom
        self.cliente.sentar()
        self.cliente.ocupar(self)


    def chamar_garcom(self) -> None:
        """Notifica o garçom que há um pedido a ser feito."""
        self.garcom.notificar_pedido(self.cliente)


    def registrar_pedido(self, pedido: Pedido) -> None:
        """Vincula o pedido à mesa, e avisa o cliente que pode aguardar."""
        self.pedido = pedido
        self.pedido.vincular(self)
        self.cliente.aguardar_pedido()


    def receber_pedido(self) -> None:
        """Avisa o cliente que pode consumir."""
        self.cliente.consumir()


    def liberar(self) -> None:
        """Configura a mesa como liberada, remove o cliente e o pedido que estava nela."""
        self.ocupada = False
        self.cliente = None
        self.pedido = None