#====================
# Grafos 
# -> un grafo es una estructura formada por: 
# -> un conjunto de vertices (V)
# -> un conjunto de aristas (E) que unen a los vertices
# se define formalmente como G = (V, E)
#====================

def dfs(grafo,nodo, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(nodo)
    print(nodo)
    for vecino in grafo[nodo]:
        if vecino not in visitados:
            dfs(grafo , vecino, visitados)



from collections import deque

def bfs(grafo,inicio):
    visitados = set()
    cola = deque([inicio])

    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            print(nodo)
            visitados.add(nodo)
            cola.extend(grafo[nodo])

grafo = {
    1: [2, 3],
    2: [4, 5],
    3: [6],
    4: [],
    5: [],
    6: []
}

dfs(grafo, 1)
print("----")
bfs(grafo, 1)