# ==================
# Ejercicio 1
# ==================
print("=================")
print("Ejercicio 1")
print("=================")

def lista_dupli(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return print("Numero dupli")
            
    
    return print("Lista correcta")
    
print(lista_dupli([1,2,3]))
            
# ==================
# Ejercicio 2
# ==================

print("=================")
print("Ejercicio 2")
print("=================")
# crear funcion dado lista tuplas "t=[(3,"Ana") , (1,"Luis"), (2,"pedro")]


def bubbleS(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-1-i):
            if arr[j][0] > arr[j+1][0]:
                arr[j], arr[j+1] = arr[j+1] , arr[j]

    return arr
    
t=[(3,"Ana") , (1,"Luis"), (2,"pedro")]
print(bubbleS(t))

print("=================")
print("Ejercicio 3")
print("=================")
class Nodo:
    def __init__(self,data):
        self.data = data
        self.next = None

    def elementoC(self, head):
        cont = 0
        actualNodo = head 
        while actualNodo:
            cont += 1
            actualNodo = actualNodo.next
        centro = cont // 2 
        actual = head 
        indice = 0
        while indice < centro:
            actual = actual.next
            indice += 1
            
        return actual.data
            
h = Nodo(1)
h.next = Nodo(2)
h.next.next = Nodo(3)
h.next.next.next = Nodo(4)

print(h.elementoC(h))


print("=================")
print("Ejercicio 4")
print("=================")

def son_circulares_iguales(lista1, lista2):
    # 1. Si no tienen el mismo tamaño, no pueden ser iguales
    if len(lista1) != len(lista2):
        return False
    
    # Caso especial: listas vacías son iguales
    if not lista1 and not lista2:
        return True

    # 2. Probamos todas las rotaciones de lista1
    n = len(lista1)
    for i in range(n):
        # Creamos la rotación: tomamos desde i hasta el final, 
        # y le sumamos desde el principio hasta i
        rotacion = lista1[i:] + lista1[:i]
        
        # Comparamos la rotación con la lista2
        if rotacion == lista2:
            return True
            
    return False

# --- Ejemplos de uso ---
lista_a = [1, 2, 3, 4]
lista_b = [3, 4, 1, 2] # Es la misma rotada
lista_c = [1, 2, 4, 3] # Mismos elementos, distinto orden circular

print(f"¿A y B son iguales? {son_circulares_iguales(lista_a, lista_b)}")
print(f"¿A y C son iguales? {son_circulares_iguales(lista_a, lista_c)}")