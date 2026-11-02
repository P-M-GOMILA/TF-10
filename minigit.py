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
    
    @property
    def branch_atual(self):
        return self.__branch_atual

    def criar_branch(self, nome):
        """
        Cria uma branch.
        Gasta 1 passo.
        """
        if nome in self.__branches:
            raise ValueError("branch existente")

        ponta = self.__branches[self.__branch_atual]

        if ponta is None:
            raise ValueError("nao ha commits")

        self.__branches[nome] = ponta
        self.__passos = 1

    def trocar_branch(self, nome):
        """
        Troca de branch.
        Gasta 1 passo.
        """
        if nome not in self.__branches:
            raise ValueError("branch inexistente")

        self.__branch_atual = nome
        self.__passos = 1

    def mesclar(self, nome):
        """
        Cria commit de merge.
        Gasta 2 passos.
        """
        if nome not in self.__branches:
            raise ValueError("branch inexistente")

        if nome == self.__branch_atual:
            raise ValueError("nao pode mesclar a propria branch")

        pai1 = self.__branches[self.__branch_atual]
        pai2 = self.__branches[nome]

        self.__contador += 1

        identificador = f"c{self.__contador}"

        self.__pais[identificador] = [pai1, pai2]
        self.__mensagens[identificador] = f"merge de {nome}"

        self.__branches[self.__branch_atual] = identificador

        self.__passos = 2

        return identificador
    
    def log(self):
        """
        Percorre o histórico usando fila..
        """
        ponta = self.__branches[self.__branch_atual]

        if ponta is None:
            self.__passos = 0
            return ()

        fila = deque([ponta])
        visitados = set()
        resultado = []

        while fila:
            atual = fila.popleft()

            if atual in visitados:
                continue

            visitados.add(atual)
            resultado.append(atual)

            for pai in self.__pais[atual]:
                fila.append(pai)

        self.__passos = len(resultado)

        return tuple(resultado)

    def buscar(self, texto):
        """
        Procura mensagem.
        """
        passos = 0

        for numero in range(1, self.__contador + 1):
            passos += 1

            commit = f"c{numero}"

            if texto in self.__mensagens[commit]:
                self.__passos = passos
                return commit

        self.__passos = passos
        return None

    def merges(self):
        """
        Retorna commits de merge.
        """
        resposta = []

        for numero in range(1, self.__contador + 1):
            commit = f"c{numero}"

            if len(self.__pais[commit]) > 1:
                resposta.append(commit)

        self.__passos = self.__contador

        return tuple(resposta)

def tentar(acao):
    try:
        acao()
    except ValueError as erro:
        print("erro:", erro)

git = MiniGit()

git.commitar("primeiro commit")
print(git.passos)

git.commitar("segundo commit")

git.criar_branch("feature")
print(git.passos)

git.commitar("terceiro commit")

git.trocar_branch("feature")

git.commitar("quarto commit")

git.trocar_branch("main")

git.mesclar("feature")

print(git.pais("c5"))

print(git.log(), git.passos)

print(git.mensagem("c3"), git.passos)

print(git.buscar("quarto"), git.passos)

print(git.merges())

git.trocar_branch("feature")

print(git.log(), git.passos)

git.trocar_branch("main")

tentar(lambda: git.trocar_branch("inexistente"))
tentar(lambda: git.criar_branch("main"))
tentar(lambda: git.mesclar("main"))
tentar(lambda: git.pais("c99"))

def medir(quantidade):
    git = MiniGit()

    for numero in range(quantidade):
        git.commitar(f"commit {numero}")

    passos_commitar = git.passos

    git.log()

    passos_log = git.passos

    return passos_commitar, passos_log

print()
print("commits   passos do commitar   passos do log")

for quantidade in (10, 100, 1000):
    commitar, log = medir(quantidade)
    print(f"{quantidade:<10}{commitar:<22}{log}")