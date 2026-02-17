#====================
# Grafos 
# -> un grafo es una estructura formada por: 
# -> un conjunto de vertices (V)
# -> un conjunto de aristas (E) que unen a los vertices
# se define formalmente como G = (V, E)
# si tiene n nodos , tiene n-1 aristas
# Pre orden / in orden / post orden
# 
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



print("----")
class Nodo:
    def __init__(self,valor):
        self.valor = valor
        self.izq = None
        self.der = None
    
    #Preorden: Raiz -> Izquierda -> Derecha
    def preorden(raiz):
        if raiz:
            print(raiz.valor)
            Nodo.preorden(raiz.izq)
            Nodo.preorden(raiz.der)

    def inorden(raiz):
        if raiz:
            Nodo.inorden(raiz.izq)
            print(raiz.valor)
            Nodo.inorden(raiz.der)
    
    def postorden(raiz):
        if raiz:
            Nodo.postorden(raiz.izq)
            Nodo.postorden(raiz.der)
            print(raiz.valor)

raiz = Nodo(1)
raiz.izq = Nodo(2)
raiz.der = Nodo(3)
raiz.izq.izq = Nodo(4)
raiz.izq.der = Nodo(5)
print("Preorden:")
Nodo.preorden(raiz)
print("Inorden:")
Nodo.inorden(raiz)
print("Postorden:")
Nodo.postorden(raiz)

print("----")
class Grafo:
    def __init__(self,valor):
        self.valor = valor
        self.izq = None
        self.der = None
    
    def insertar(raiz,valor):
        if raiz is None:
            return Nodo(valor)
        
        if valor < raiz.valor:
            raiz.izq = Grafo.insertar(raiz.izq, valor)
        
        else:
            raiz.der = Grafo.insertar(raiz.der, valor)
        
        return raiz
    
    def buscar(raiz,valor):
        if raiz is None or raiz.valor == valor:
            return raiz
        if valor < raiz.valor:
            return Grafo.buscar(raiz.izq, valor)
        else:
            return Grafo.buscar(raiz.der, valor)
    
    def altura(raiz):
        if raiz is None:
            return -1
        return 1 + max(Grafo.altura(raiz.izq), Grafo.altura(raiz.der))
 

