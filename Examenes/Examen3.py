# --- CLASES BASE DEL PROFESOR ---

class Stack: # Pila
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        return None
    def isEmpty(self):
        return len(self.items) == 0
    def peek(self): # Ver el de arriba sin sacar
        if not self.isEmpty():
            return self.items[-1]

class Queue: # Cola
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop(0) # Saca el primero (índice 0)
        return None
    def isEmpty(self):
        return len(self.items) == 0