#Crear una funcion recursiva que suma los elementos pares menos la suma de los elementos impares de un arreglo
def restar_pares(lista):
    if not lista:
        return 0
    else:
        if lista[0] % 2 == 0:  # número par
            return lista[0] + restar_pares(lista[1:])
        else:  # número impar
            return -lista[0] + restar_pares(lista[1:])

print(restar_pares([5,3,2,1]))  # -5 -3 +2 -1 = -7