# una pila es una estructura de datos que permite almacenar y recuperar datos en orden LIFO (Last In, First Out)
# El primero que entra es el ultimo en salir
# Base -> [1][2][3] -> Top / Clima(top)
# Peek -> consulta elemento superior 
# Is_empty -> consulta si la pila esta vacia
# Size -> consulta el tamaño de la pila



#=====================
#Forma 1 
#=====================
""" stack = []

#Push -> es meter 
stack.append(10)
stack.append(20)

#Pop -> es sacar el ultimo elemento que esta
stacck.pop() """



class Pila:
    def __init__(self):
        self.items = []

    def push(self , value):
        if self.is_empy():
            return None
        self.items.append(value)
        return self.items
    
    def pop(self):
        if self.is_empy():
            return None
        return self.items.pop()
    
    def peek(self):
        if self.is_empy():
            return None
        return self.items[-1]
    
    def is_empy(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)


#=====================
# Aplicaciones de las pilas 
#=====================
pila = Pila()
pila.push(10)
pila.push(20)
pila.push(30)
print(pila.peek())
print(pila.pop())
print(pila.size())
print(pila.is_empy())