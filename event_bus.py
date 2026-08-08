class EventBus:
    def __init__(self):
        self._eventos = []


    def registrar(self, categoria, mensagem):
        """Armazena a categoria e a mensagem de um evento na lista geral de eventos."""
        self._eventos.append((categoria, mensagem))


    def coletar(self):
        """Retorna a lista geral de eventos que foram registrados."""
        eventos = self._eventos
        self._eventos = []
        return eventos