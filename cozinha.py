from time import sleep
from prato import Prato

class Cozinha:
    def __init__(self):
        pass


    def preparar_prato(self, prato: Prato):
        print(f"Preparando {prato.nome}...")
        sleep(1)
        print("Misturando ingredientes...")
        tempo_preparo = prato.tempo / 10
        sleep(tempo_preparo)
        print("Prato finalizado!")