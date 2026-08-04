from salao import Salao
from cozinha import Cozinha
from cardapio import Cardapio
from cliente import Cliente
from pedido import Pedido

class Garcom:
    def __init__(
            self, 
            salao: Salao, 
            cozinha: Cozinha, 
            cardapio: Cardapio
        ) -> None:
        self.salao = salao
        self.cozinha = cozinha
        self.cardapio = cardapio
        self.clientes: list[Cliente] = []
        self.fila_pedidos: list[Cliente] = []
        self.pedidos: list[Pedido] = []


    def atualizar(self) -> None:
        self._coletar_pedidos()
        self._entregar_pedidos()


    def notificar_pedido(self, cliente: Cliente) -> None:
        """Registra na fila que este cliente está pronto para ter o pedido coletado."""
        self.fila_pedidos.append(cliente)


    def _coletar_pedidos(self) -> None:
        while self.fila_pedidos:
            cliente = self.fila_pedidos.pop(0)
            pedido = cliente.comunicar_pedido()

            print(f"Anotando o pedido...")
            print(
                f"O cliente pediu {pedido.prato.nome} e {pedido.bebida.nome}, "
                f"no valor total de R${pedido.valor:.2f} "
                f"\nTempo estimado: {pedido.prato.tempo}min"
            )

            self.pedidos.append(pedido)
            self._enviar_para_cozinha(pedido)


    def _enviar_para_cozinha(self, pedido: Pedido) -> None:
        self.cozinha.receber_pedido(pedido)
        print("Enviando o pedido à cozinha...")


    def _entregar_pedidos(self) -> None:
        for pedido in self.pedidos:
            if pedido.esta_pronto():
                pedido.entregar()