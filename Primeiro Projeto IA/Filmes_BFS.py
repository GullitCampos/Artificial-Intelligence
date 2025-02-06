import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Função BFS com backtracking para encontrar o menor caminho entre filmes
def bfs_backtracking(filme_inicial, filme_destino, lista_de_filmes):
    # Fila para o BFS
    fila = deque([filme_inicial])
    
    # Dicionário para armazenar o predecessor de cada filme
    predecessores = {filme_inicial: None}
    
    # Conjunto para armazenar os filmes visitados
    visitados = set([filme_inicial])
    
    # Realizando a busca em largura (BFS)
    while fila:
        # Retirar o primeiro elemento da fila
        filme_atual = fila.popleft()
        
        # Se chegarmos ao destino, realizamos o backtracking para reconstruir o caminho
        if filme_atual == filme_destino:
            return reconstruir_caminho(predecessores, filme_destino)
        
        # Para cada filme relacionado ao filme atual
        for filme_vizinho, _ in lista_de_filmes[filme_atual]:
            if filme_vizinho not in visitados:
                visitados.add(filme_vizinho)  # Marca o filme como visitado
                predecessores[filme_vizinho] = filme_atual  # Marca o predecessor
                fila.append(filme_vizinho)  # Adiciona o filme na fila para exploração
    
    # Se o destino não for alcançado, retornamos uma lista vazia
    return []

# Função para reconstruir o caminho usando o dicionário de predecessores
def reconstruir_caminho(predecessores, filme_destino):
    caminho = []
    filme_atual = filme_destino
    while filme_atual is not None:
        caminho.append(filme_atual)
        filme_atual = predecessores[filme_atual]
    
    # Como reconstruímos o caminho de trás para frente, invertemos o resultado
    return caminho[::-1]

# Criando a lista de filmes e suas conexões no MCU (filmes relacionados)
lista_de_filmes = {
    'Homem de Ferro': [('Homem de Ferro 2', 1), ('Os Vingadores', 2)],
    'Homem de Ferro 2': [('Homem de Ferro', 1), ('Os Vingadores', 2), ('Capitão América: O Primeiro Vingador', 3)],
    'Os Vingadores': [('Homem de Ferro', 2), ('Thor', 1), ('Capitão América: O Primeiro Vingador', 1), ('Vingadores: Era de Ultron', 2)],
    'Thor': [('Thor: O Mundo Sombrio', 1), ('Os Vingadores', 1), ('Thor: Ragnarok', 2)],
    'Capitão América: O Primeiro Vingador': [('Os Vingadores', 1), ('Capitão América: O Soldado Invernal', 2)],
    'Vingadores: Era de Ultron': [('Os Vingadores', 2), ('Vingadores: Guerra Infinita', 3), ('Homem de Ferro 3', 2)],
    'Capitão América: O Soldado Invernal': [('Capitão América: Guerra Civil', 1), ('Vingadores: Guerra Infinita', 3)],
    'Thor: O Mundo Sombrio': [('Thor', 1), ('Thor: Ragnarok', 3), ('Os Vingadores', 2)],
    'Thor: Ragnarok': [('Thor', 2), ('Thor: O Mundo Sombrio', 3), ('Vingadores: Guerra Infinita', 1)],
    'Vingadores: Guerra Infinita': [('Vingadores: Ultimato', 1), ('Vingadores: Era de Ultron', 3), ('Capitão América: O Soldado Invernal', 3)],
    'Vingadores: Ultimato': [('Vingadores: Guerra Infinita', 1), ('Homem de Ferro 3', 4), ('Thor: Ragnarok', 2)],
    'Homem de Ferro 3': [('Vingadores: Era de Ultron', 2), ('Vingadores: Ultimato', 4)],
    'Capitão América: Guerra Civil': [('Capitão América: O Soldado Invernal', 1), ('Vingadores: Guerra Infinita', 2)],
}

# Função para plotar o grafo dos filmes e suas conexões
def plotar_grafo(lista_de_filmes):
    # Criando um grafo utilizando a biblioteca 'networkx'
    G = nx.Graph()

    # Adicionando os filmes e suas conexões ao grafo
    for filme in lista_de_filmes.keys():
        G.add_node(filme)

    for filme, conexoes in lista_de_filmes.items():
        for conexao, custo in conexoes:
            G.add_edge(filme, conexao, weight=custo)

    # Plotar o grafo com pesos nas arestas
    pos = nx.spring_layout(G)  # Layout para o grafo
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, font_color='red')
    plt.show()

# Chamando a função de plotar o grafo
plotar_grafo(lista_de_filmes)

# Recebendo os parâmetros do usuário com validação de entrada
filme_inicial = input("Digite o nome do filme de partida: ").strip()
while filme_inicial not in lista_de_filmes:
    filme_inicial = input("Filme de partida inválido. Digite novamente: ").strip()

filme_destino = input("Digite o nome do filme de destino: ").strip()
while filme_destino not in lista_de_filmes:
    filme_destino = input("Filme de destino inválido. Digite novamente: ").strip()

# Chamando a função de busca BFS com backtracking
filmes_visitados = bfs_backtracking(filme_inicial, filme_destino, lista_de_filmes)

# Exibindo o resultado
if filmes_visitados:
    print(f"O caminho de {filme_inicial} até {filme_destino} é: {' -> '.join(filmes_visitados)}")
else:
    print(f"Não foi possível encontrar um caminho de {filme_inicial} até {filme_destino}.")
