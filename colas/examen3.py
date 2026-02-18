# Examen demo 
# Ejercicio 1 

class Pila:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def esta_vacia(self):
        return len(self.items) == 0


def invertir_cadena(cadena):
    pila = Pila()

    for letra in cadena:
        pila.push(letra)

    inv = ""
    while not pila.esta_vacia():
        inv += pila.pop()

    return inv


print(invertir_cadena("estructura"))
print("--------")

class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0


def evaluar_postfija(expresion):
    pila = Stack()
    tokens = expresion.split()

    for token in tokens:
        if token.isdigit():
            pila.push(int(token))
        else:
            b = pila.pop()
            a = pila.pop()

            if token == '+':
                pila.push(a + b)
            elif token == '-':
                pila.push(a - b)
            elif token == '*':
                pila.push(a * b)
            elif token == '/':
                pila.push(a / b)

    return pila.pop()


print(evaluar_postfija("3 4 + 2 *"))
print("-----")
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, x):
        self.items.append(x)

    def dequeue(self):
        return self.items.pop(0)

    def isEmpty(self):
        return len(self.items) == 0


def rotacion(queue, k):
    cola = Queue()

    # Copiar elementos de la cola original
    for elemento in queue.items:
        cola.enqueue(elemento)

    # Rotar k veces
    for _ in range(k):
        cola.enqueue(cola.dequeue())

    return cola.items


mi_cola = Queue()
mi_cola.enqueue(10)
mi_cola.enqueue(20)
mi_cola.enqueue(30)
mi_cola.enqueue(40)
mi_cola.enqueue(50)

print("Rotada:", rotacion(mi_cola, 2))
print("---")
import heapq

def numeros_grandes(lista, k):
    if k <= 0:
        return []

    heap = []

    for num in lista:
        if len(heap) < k:
            heapq.heappush(heap, num)
        else:
            if num > heap[0]:  # heap[0] es el menor del heap
                heapq.heapreplace(heap, num)

    # devolver de mayor a menor (solo ordenamos k elementos, no toda la lista)
    return sorted(heap, reverse=True)


# Prueba
print(numeros_grandes([3, 10, 5, 20, 7], 2))

