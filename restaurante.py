import random
from cardapio import Cardapio
from cliente import Cliente
from mesa import Mesa
from pedido import Pedido
from cozinha import Cozinha
from utils import validar_string, validar_inteiro

class Restaurante:

    TEMPO_POR_TURNO = 10

    def __init__(self, cardapio: Cardapio) -> None:
        self.cardapio = cardapio
        self.cozinha = Cozinha()
        self.aberto = False
        self.turno = 1
        self.mesas = []
        self.fila = []
        self.clientes = []
        self.pedidos = []
        self.avaliacoes = 0

        self.criar_mesas()


    def proximo_turno(self) -> None:
        self.turno += 1

        print(f"\n===== TURNO {self.turno} =====")

        for cliente in self.clientes:
            cliente.atualizar(self.TEMPO_POR_TURNO)

        self.cozinha.atualizar(self.TEMPO_POR_TURNO)


    def criar_mesas(self) -> None:
        """Cria as mesas do restaurante e as adiciona à lista de mesas."""
        for num in range (1, 7):
            self.mesas.append(Mesa(num))


    def verificar_status(self) -> None:
        """Exibe o status atual do restaurante (avaliações, mesas, clientes, etc...)"""
        print(
            f"Status atual do restaurante:"
            f"\nAvaliações: {self.avaliacoes}"
            f"\nNúmero de mesas: {len(self.mesas)}"
            f"\nNúmero de clientes: {len(self.clientes)}"
            f"\nNúmero de pedidos feitos: {len(self.pedidos)}"
        )


    def abrir_restaurante(self) -> None:
        """Abre o restaurante e inicia o fluxo de atendimento."""
        print("Abrindo restaurante...")
        self.aberto = True

        print(f"\n===== TURNO {self.turno} =====")

        while self.aberto:
            self.talvez_chegue_cliente()
            self.acomodar_clientes()
            self.proximo_turno()
            self.coletar_pedidos()
            self.entregar_pedidos()
            if self.turno >= 10:
                self.encerrar()


    def acomodar_clientes(self) -> None:
        for cliente in self.clientes:
            if cliente.chegou():
                self.atender_cliente(cliente)
            if cliente.esta_sentado():
                cliente.fazer_pedido(self.cardapio)


    def coletar_pedidos(self) -> None:
        for cliente in self.clientes:
            if cliente.esta_sentado():
                self.anotar_pedido(cliente, cliente.mesa)


    def talvez_chegue_cliente(self) -> None:
        if random.random() < 0.5:
            print("Um cliente chegou!")
            self.recepcionar_cliente()
        else:
            print("Nenhum cliente chegou neste turno.")


    def recepcionar_cliente(self) -> None:
        """Recepciona o cliente [adicionar incrementação posteriormente]"""
        self.cadastrar_cliente()


    def cadastrar_cliente(self) -> Cliente:
        """Cadastra um cliente e o armazena na lista de clientes, o retornando ao final."""
        nome = validar_string("> Cadastrar cliente: ")
        cliente = Cliente(nome)
        self.clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
        return cliente


    def atender_cliente(self, cliente: Cliente) -> None:
        """Realiza o atendimento do cliente, da acomodação até a entrega do pedido."""
        mesa = self.acomodar_cliente(cliente)

        # Se não conseguiu acomodar (sem mesas disponíveis)
        if mesa is None:
            print("Nenhuma mesa disponível... cliente inserido na fila.")
            self.fila.append(cliente)
            return 

        if cliente.esta_sentado():
            pedido = self.anotar_pedido(cliente, mesa)
            self.enviar_para_cozinha(pedido)


    def acomodar_cliente(self, cliente: Cliente) -> Mesa | None:
        """
        Acomoda o cliente e retorna a mesa que foi ocupada, caso haja alguma disponível.
        Se não, retorna False.
        """
        for mesa in self.mesas:
            if mesa.esta_livre():
                mesa.ocupar(cliente)
                cliente.ocupar(mesa)
                print(f"Cliente acomodado à mesa n° {mesa.numero}.")
                return mesa

        return None


    def anotar_pedido(self, cliente: Cliente, mesa: Mesa) -> Pedido:
        """Anota o pedido feito pelo cliente, registra na lista de pedidos e o retorna."""
        pedido = cliente.fazer_pedido(self.cardapio)
        self.pedidos.append(pedido)
        mesa.registrar_pedido(pedido)
        pedido.vincular(mesa)
        cliente.aguardar_pedido()

        print(f"Anotando o pedido...")
        print(
            f"O cliente pediu {pedido.prato.nome} e {pedido.bebida.nome}, "
            f"no valor total de R${pedido.valor:.2f} "
            f"\nTempo estimado: {pedido.prato.tempo}min"
        )

        return pedido


    def enviar_para_cozinha(self, pedido: Pedido) -> None:
        """Envia o pedido à cozinha para ser preparado."""
        print("Enviando o pedido à cozinha...")
        self.cozinha.receber_pedido(pedido)


    def entregar_pedidos(self) -> None:
        """Verificar se há pedidos prontos e realiza a entrega."""
        for pedido in self.pedidos:
            if pedido.esta_pronto():
                pedido.entregar(pedido.mesa)


    def finalizar_atendimento(self, mesa: Mesa):
        mesa.liberar()


    def encerrar(self) -> None:
        print("1. Aguardar próximo cliente \n2. Encerrar atendimentos")
        decisao = validar_inteiro("Qual a decisão? ")

        if decisao == 2:
            self.aberto = False