# TF-10 - MiniGit

## Medições

| commits | passos do commitar | passos do log |
|--------------------|----------|
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

## 1

O método commitar sempre realiza as mesmas operações: criar o commit e mover o ponteiro da branch. Por isso ele gasta sempre 2 passos.

Já o log precisa visitar todos os commits alcançáveis. Quanto maior o histórico, mais commits precisam ser percorridos e mais passos são gastos.

## 2

mensagem(commit) usa a chave do dicionário diretamente, então encontra o resultado em um único acesso.

buscar(texto) procura dentro das mensagens. Como o dicionário organiza os dados pelas chaves e não pelos valores, pode ser necessário verificar vários commits até encontrar o texto.

## 3

Um merge une dois históricos diferentes. Por isso o commit de merge possui dois pais.

Quando existem commits com mais de um pai, a estrutura deixa de ser uma lista linear e passa a ser um grafo.

## 4

O método pais devolve uma tupla para proteger o histórico.

Se a lista interna fosse devolvida diretamente, qualquer código externo poderia alterar os pais dos commits e corromper a estrutura do MiniGit
