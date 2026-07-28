from restaurante import Restaurante
from cardapio import Cardapio
from utils import validar_inteiro

def menu_principal(restaurante: Restaurante, cardapio: Cardapio) -> None:
    def _encerrar():
        print("Até a próxima!")
        return False


    opcoes = {
        1: ("Abrir restaurante", restaurante.abrir_restaurante),
        2: ("Conferir cardápio", cardapio.exibir_cardapio),
        3: ("Adicionar um novo prato", cardapio.adicionar_prato),
        4: ("Verificar status", restaurante.verificar_status),
        5: ("Sair", _encerrar),
    }


    def _exibir_opcoes():
        for chave, (descricao, _) in opcoes.items():
            print(f"[{chave}] - {descricao}")


    def _validar_escolha():
        opcao_escolhida = validar_inteiro("Selecione uma das opções: ")

        if opcao_escolhida == 5:
            return _encerrar()

        if opcao_escolhida in opcoes:
            _, funcao = opcoes[opcao_escolhida]
            funcao()
            return True
        
        print("Opção inválida!")
        return True


    _exibir_opcoes()
    return _validar_escolha()