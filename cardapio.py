from random import choice
from prato import Prato
from bebida import Bebida
from utils import validar_string, validar_inteiro

class Cardapio:
    def __init__(self) -> None:
        self.pratos = {
            1 : Prato('Strogonoff de carne', preco=40, tempo=20),
            2 : Prato('Bife à parmegiana', preco=60, tempo=30),
            3 : Prato('Risotto', preco=35, tempo=30),
            4 : Prato('Costela ao molho', preco=80, tempo=60),
        }
        self.bebidas = {
            1: Bebida('Água mineral', preco=3),
            2: Bebida('Suco natural', preco=5),
            3: Bebida('Refrigerante', preco=7),
            4: Bebida('Taça de vinho', preco=15)
        }


    def exibir_cardapio(self) -> None:
        print('\nCardápio de hoje:')
        for codigo, prato in self.pratos.items():
            print(f"\nPrato n° {codigo}: {prato.descricao()}")
            
        print('\nBebidas:')
        for codigo, bebida in self.bebidas.items():
            print(f"{codigo}. {bebida.descricao()}")


    def obter_prato(self, codigo: int) -> Prato:
        return self.pratos.get(codigo)


    def prato_aleatorio(self) -> Prato:
        codigo = choice(list(self.pratos.keys()))
        return self.pratos[codigo]


    def bebida_aleatoria(self):
        codigo = choice(list(self.bebidas.keys()))
        return self.bebidas[codigo]


    def adicionar_prato(self) -> None:
        nome = validar_string("Nome do prato: ")
        preco = validar_inteiro("Preço do prato: ")
        tempo = validar_inteiro("Tempo de preparo: ")

        self.pratos[max(self.pratos) + 1] = Prato(nome=nome, preco=preco, tempo=tempo)

        self.exibir_cardapio()