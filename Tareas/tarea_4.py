# Tarea 4 - Estructuras de Datos
# Fecha: Febrero 2026

from collections import deque

# =============================================
# GRAFO CON LISTA DE ADYACENCIA
# =============================================

class Grafo:
    def __init__(self):
        self.lista = {}

    def agregar_vertice(self, v):
        if v not in self.lista:
            self.lista[v] = []

    def agregar_arista(self, v1, v2):
        self.agregar_vertice(v1)
        self.agregar_vertice(v2)
        self.lista[v1].append(v2)
        self.lista[v2].append(v1)

    def mostrar(self):
        for v in self.lista:
            print(v, "->", self.lista[v])

    def dfs(self, inicio):
        visitados = []
        pila = [inicio]
        while pila:
            nodo = pila.pop()
            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.lista[nodo]:
                    if vecino not in visitados:
                        pila.append(vecino)
        return visitados

    def bfs(self, inicio):
        visitados = []
        cola = deque([inicio])
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.lista[nodo]:
                    if vecino not in visitados:
                        cola.append(vecino)
        return visitados


# =============================================
# ARBOL BINARIO DE BUSQUEDA (BST)
# =============================================

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

class BST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar(nodo.izq, valor)
        else:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar(nodo.der, valor)

    def buscar(self, valor):
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        if valor < nodo.valor:
            return self._buscar(nodo.izq, valor)
        return self._buscar(nodo.der, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            # nodo con un solo hijo o sin hijos
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq
            # nodo con dos hijos: buscar el minimo del subarbol derecho
            minimo = nodo.der
            while minimo.izq is not None:
                minimo = minimo.izq
            nodo.valor = minimo.valor
            nodo.der = self._eliminar(nodo.der, minimo.valor)
        return nodo

    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        izq = self._altura(nodo.izq)
        der = self._altura(nodo.der)
        return 1 + max(izq, der)

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo is not None:
            self._inorden(nodo.izq, resultado)
            resultado.append(nodo.valor)
            self._inorden(nodo.der, resultado)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)
            self._preorden(nodo.izq, resultado)
            self._preorden(nodo.der, resultado)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, resultado):
        if nodo is not None:
            self._postorden(nodo.izq, resultado)
            self._postorden(nodo.der, resultado)
            resultado.append(nodo.valor)


# =============================================
# ARBOL GENERAL
# =============================================

class NodoGeneral:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

class ArbolGeneral:
    def __init__(self, valor_raiz):
        self.raiz = NodoGeneral(valor_raiz)

    def recorrido(self):
        cola = deque([self.raiz])
        resultado = []
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            for hijo in nodo.hijos:
                cola.append(hijo)
        return resultado


# =============================================
# CONVERSION A ARBOL BINARIO
# (tecnica hijo-izquierdo / hermano-derecho)
# =============================================

class NodoBin:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None  # primer hijo
        self.der = None  # siguiente hermano

def convertir(nodo_gen):
    if nodo_gen is None:
        return None
    nodo_bin = NodoBin(nodo_gen.valor)
    if len(nodo_gen.hijos) > 0:
        nodo_bin.izq = convertir(nodo_gen.hijos[0])
        actual = nodo_bin.izq
        for i in range(1, len(nodo_gen.hijos)):
            actual.der = convertir(nodo_gen.hijos[i])
            actual = actual.der
    return nodo_bin

def preorden_bin(nodo):
    if nodo is None:
        return []
    return [nodo.valor] + preorden_bin(nodo.izq) + preorden_bin(nodo.der)



print("--- GRAFO ---")
g = Grafo()
g.agregar_arista("A", "B")
g.agregar_arista("A", "C")
g.agregar_arista("B", "D")
g.agregar_arista("C", "D")
g.agregar_arista("D", "E")
g.mostrar()
print("DFS:", g.dfs("A"))
print("BFS:", g.bfs("A"))

print("\n--- BST ---")
arbol = BST()
for n in [50, 30, 70, 20, 40, 60, 80]:
    arbol.insertar(n)
print("Inorden:", arbol.inorden())
print("Preorden:", arbol.preorden())
print("Postorden:", arbol.postorden())
print("Altura:", arbol.altura())
print("Buscar 40:", arbol.buscar(40))
print("Buscar 99:", arbol.buscar(99))
arbol.eliminar(30)
print("Inorden sin 30:", arbol.inorden())

print("\n--- ARBOL GENERAL ---")
ag = ArbolGeneral("A")
b = NodoGeneral("B")
c = NodoGeneral("C")
d = NodoGeneral("D")
e = NodoGeneral("E")
f = NodoGeneral("F")
gn = NodoGeneral("G")
b.hijos.append(e)
b.hijos.append(f)
d.hijos.append(gn)
ag.raiz.hijos.append(b)
ag.raiz.hijos.append(c)
ag.raiz.hijos.append(d)
print("Recorrido BFS:", ag.recorrido())

print("\n--- CONVERSION A BINARIO ---")
raiz_bin = convertir(ag.raiz)
print("Preorden binario:", preorden_bin(raiz_bin))