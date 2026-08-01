from salao import Salao
from cozinha import Cozinha
from cardapio import Cardapio
from mesa import Mesa
from cliente import Cliente
from pedido import Pedido

class Garcom:
    def __init__(self, salao: Salao, cozinha: Cozinha, cardapio: Cardapio) -> None: 
        self.salao = salao
        self.cozinha = cozinha
        self.cardapio = cardapio
        self.clientes: list[Cliente] = []
        self.pedidos: list[Pedido] = []


    def atualizar(self) -> None:
        self._coletar_pedidos()
        self._entregar_pedidos()


    def acomodar_cliente(self, cliente: Cliente) -> None:
        self.clientes.append(cliente)
        mesa = self._localizar_mesa()

        if mesa is None:
            print("Nenhuma mesa disponível no momento. Cliente inserido na fila...")
            self.restaurante.fila.append(cliente)
            return

        mesa.receber(cliente, self.cardapio)
        print(f"{cliente.nome} acomodado à mesa n° {mesa.numero}")


    def _localizar_mesa(self) -> Mesa | None:
        for mesa in self.salao.mesas:
            if mesa.esta_livre():
                return mesa

        return None


    def _coletar_pedidos(self) -> None:
        for cliente in self.clientes:
            if cliente.quer_pedir():
                cliente.receber_cardapio(self.cardapio)
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