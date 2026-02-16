class Queue:
    def __init__(self):
        self.cola = []

    def enqueue(self, element):
        self.cola.append(element)

    def dequeue(self):
        self.cola.pop(0)

    def peek(self):
        print(self.cola[0])

    def is_empty(self):
        return len(self.cola) == 0

    def size(self):
        return len(self.cola)

    def show(self):
        print(self.cola)


cola = Queue()
cola.enqueue(1)
cola.enqueue(2)
cola.enqueue(3)
cola.show()
cola.dequeue()

print("==================")
class ColasBanco:
    def __init__(self):
        self.cola = []
        personas = ["juan", "alfredo", "eduin", "AnaPau", "Virlan", "Julion"]
        for persona in personas:
            self.atender(persona)

    def atender(self, cliente):
        self.cola.append(cliente)
        print(cliente)


banco = ColasBanco()
print(banco.cola)

print("==================")
# Simula una sala de emergencias donde cada paciente tiene prioridad
# menor número = mayor urgencia

import heapq

priority_queue = []

heapq.heappush(priority_queue, (2, "Anapau"))
heapq.heappush(priority_queue, (1, "Barux"))
heapq.heappush(priority_queue, (3, "Virlan"))
heapq.heappush(priority_queue, (5, "Alfredo"))

# Atender pacientes en orden de prioridad
while priority_queue:
    priority, patient = heapq.heappop(priority_queue)
    print(f"Atendiendo a {patient} con prioridad {priority}")


