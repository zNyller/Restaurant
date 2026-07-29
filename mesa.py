from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cliente import Cliente
    from pedido import Pedido

class Mesa:
    def __init__(self, numero: int):
        self.numero = numero
        self.ocupada = False
        self.cliente = None
        self.pedido = None


    def esta_livre(self) -> bool:
        return not self.ocupada


    def ocupar(self, cliente: "Cliente") -> None:
        """Configura a mesa como ocupada e registra o cliente que está nela."""
        self.ocupada = True
        self.cliente = cliente


    def registrar_pedido(self, pedido: "Pedido") -> None:
        """Registra e vincula o pedido feito à mesa atual."""
        self.pedido = pedido


    def liberar(self) -> None:
        """Configura a mesa como liberada, remove o cliente e o pedido que estava nela."""
        self.ocupada = False
        self.cliente = None
        self.pedido = None