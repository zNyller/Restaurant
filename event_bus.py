class EventBus:
    def __init__(self):
        self._eventos = []


    def publicar(self, categoria, mensagem):
        """Armazena a categoria e a mensagem de um evento na lista geral de eventos."""
        self._eventos.append((categoria, mensagem))


    def coletar(self):
        eventos = self._eventos
        self._eventos = []
        return eventos