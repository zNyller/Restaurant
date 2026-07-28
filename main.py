from cardapio import Cardapio
from restaurante import Restaurante
from utils import validar_inteiro


def main() -> None:
    cardapio = Cardapio()
    restaurante = Restaurante(cardapio)

    opcoes = {
        1: ("Abrir restaurante", restaurante.abrir_restaurante),
        2: ("Conferir cardápio", cardapio.exibir_cardapio),
        3: ("Adicionar um novo prato", cardapio.adicionar_prato)
    }


    def menu_principal() -> None:
        print("=-" * 30)
        print("BOAS-VINDAS AO RESTAURANTE!".center(55))
        print("=-" *30)

        for chave, (descricao, _) in opcoes.items():
            print(f"[{chave}] - {descricao}")
        opcao_escolhida = validar_inteiro("Selecione uma das opções: ")
        if opcao_escolhida in opcoes:
            _, funcao = opcoes[opcao_escolhida]
            funcao()
        else:
            print("Opção inválida!")

    menu_principal()


if __name__ == "__main__":
    main()