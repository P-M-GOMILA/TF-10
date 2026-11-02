from collections import deque


class MiniGit:
    """
    Simula um repositório Git simplificado.
    Guarda commits, branches e histórico.
    """

    __slots__ = (
        "__pais",
        "__mensagens",
        "__branches",
        "__branch_atual",
        "__contador",
        "__passos",
    )

    def __init__(self):
        """
        Cria um repositório vazio.
        """
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__contador = 0
        self.__passos = 0

    @property
    def passos(self):
        return self.__passos

    def commitar(self, mensagem):
        """
        Cria um commit novo.
        Gasta 2 passos.
        """
        if not mensagem:
            raise ValueError("mensagem vazia")

        self.__contador += 1
        identificador = f"c{self.__contador}"

        pai = self.__branches[self.__branch_atual]

        if pai is None:
            self.__pais[identificador] = []
        else:
            self.__pais[identificador] = [pai]

        self.__mensagens[identificador] = mensagem

        self.__branches[self.__branch_atual] = identificador

        self.__passos = 2

        return identificador

    def mensagem(self, commit):
        """
        Busca uma mensagem por chave.
        Gasta 1 passo.
        """
        if commit not in self.__mensagens:
            raise ValueError("commit inexistente")

        self.__passos = 1
        return self.__mensagens[commit]

    def pais(self, commit):
        """
        Devolve os pais como tupla.
        Gasta 1 passo.
        """
        if commit not in self.__pais:
            raise ValueError("commit inexistente")

        self.__passos = 1
        return tuple(self.__pais[commit])