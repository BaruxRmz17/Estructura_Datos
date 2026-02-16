print("===================")
print("Ejercicio 1")
def arrPares(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-1-i):
            if arr[j][1] > arr[j+1][1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
arre = [[1,4], [2,1], [6,0]]

resultado = arrPares(arre)
print(resultado)

print("===================")
print("Ejercicio 2")
def numero_de_veces(num , n):
    cont = 0
    for i in n:
        if i == num:
            cont += 1
    return cont 
arre = [1,2,2,3,3,4,5,6,6,6]
print(arre)
print(numero_de_veces(6,arre))


print("===================")
print("Ejercicio 3")
def contar_ocurrencias(arr, x):
    n = len(arr)
    
    low = 0
    high = n - 1
    primera = -1
    
    while low <= high:
        mid = low + high
        mid = mid // 2
        
        if arr[mid] == x:
            primera = mid
            high = mid - 1  
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    
    if primera == -1:
        return 0 
    
    low = 0
    high = n - 1
    ultima = -1
    
    while low <= high:
        mid = low + high
        mid = mid // 2
        
        if arr[mid] == x:
            ultima = mid
            low = mid + 1  
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    
    return ultima - primera + 1


arr = [1,2,2,3,3,4,5,6,6,6]
print(contar_ocurrencias(arr, 6))  



print("===================")
print("Ejercicio 5")
print("===================")
class Ligada:
    def __init__(self, data):
        self.data = data
        self.next = None

class ListaLigada:
    def __init__(self):
        self.head = None

    def esCircular(self):
        actualNodo = self.head
        nodoRapido = self.head
        
        while nodoRapido and nodoRapido.next:
            actualNodo = actualNodo.next
            nodoRapido = nodoRapido.next.next
            
            if actualNodo == nodoRapido:
                return True  
        
        return False  


print("No es circular:")
lista = ListaLigada()
lista.head = Ligada(1)
lista.head.next = Ligada(2)
lista.head.next.next = Ligada(3)
lista.head.next.next.next = Ligada(4)
lista.head.next.next.next.next = Ligada(5)
print(lista.esCircular())
print("Si es circular:")
lista.head.next.next.next.next = lista.head  
print(lista.esCircular())  

