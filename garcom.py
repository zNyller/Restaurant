from recepcao import Recepcao
from salao import Salao
from cozinha import Cozinha
from cardapio import Cardapio
from mesa import Mesa
from cliente import Cliente
from pedido import Pedido

class Garcom:
    def __init__(
            self, 
            recepcao: Recepcao, 
            salao: Salao, 
            cozinha: Cozinha, 
            cardapio: Cardapio
        ) -> None:
        self.recepcao = recepcao 
        self.salao = salao
        self.cozinha = cozinha
        self.cardapio = cardapio
        self.clientes: list[Cliente] = []
        self.pedidos: list[Pedido] = []


    def atualizar(self) -> None:
        self._coletar_pedidos()
        self._entregar_pedidos()


    def _coletar_pedidos(self) -> None:
        for cliente in self.recepcao.clientes:
            if cliente.quer_pedir():
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


    def _entregar_pedidos(self) -> None:
        for pedido in self.pedidos:
            if pedido.esta_pronto():
                pedido.entregar()