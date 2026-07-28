from random import choice
from utils import validar_string, validar_inteiro

class Cardapio:
    def __init__(self) -> None:
        self.pratos = {
            1 : {
                'nome' : 'Strogonoff de carne',
                'preco' : 40,
                'tempo' : 20
            },
            2 : {
                'nome' : 'Bife à parmegiana',
                'preco': 60,
                'tempo': 30
            },
            3 : {
                'nome' : 'Risotto',
                'preco': 35,
                'tempo': 30
            },
            4 : {
                'nome' : 'Costela ao molho',
                'preco' : 80,
                'tempo' : 60
            }
        }


    def exibir_cardapio(self) -> None:
        print('\nCardápio de hoje:')
        for codigo, prato in self.pratos.items():
            nome = prato['nome']
            preco = prato['preco']
            tempo = prato['tempo']
            print(f"\nPrato n° {codigo}: \n{nome} | Preço: R${preco:.2f} | Tempo de preparo: {tempo}min")


    def obter_prato(self, codigo: int) -> dict:
        return self.pratos.get(codigo)


    def prato_aleatorio(self) -> dict:
        codigo = choice(list(self.pratos.keys()))
        return self.pratos[codigo]


    def adicionar_prato(self) -> None:
        nome = validar_string("Nome do prato: ")
        preco = validar_inteiro("Preço do prato: ")
        tempo = validar_inteiro("Tempo de preparo: ")

        self.pratos[max(self.pratos) + 1] = {
            'nome': nome, 
            'preco': preco, 
            'tempo': tempo
        }
        self.exibir_cardapio()