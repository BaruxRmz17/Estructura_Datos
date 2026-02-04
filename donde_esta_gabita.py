# ============================================================
# Tarea 2 - Estructura de Datos
# ¿Dónde está Gabita?
# ============================================================

# ---------- Crear la matriz de ceros ----------
def crear_matriz(m, n):
    """Crea una matriz m x n llena de ceros (recursiva por filas)."""
    if m == 0:
        return []
    return [[0] * n] + crear_matriz(m - 1, n)


# ---------- Leer los N pasos iniciales (recursiva) ----------
def leer_pasos(n, ruta, contador):
    """Lee n pares de coordenadas de forma recursiva y los agrega a la ruta."""
    if n == 0:
        return
    
    # Leer coordenadas de forma simple
    print("Ingresa las coordenadas del paso", contador, "(fila col): ")
    entrada = input()
    
    # Separar la entrada manualmente
    partes = entrada.split()
    fila = int(partes[0])
    col = int(partes[1])
    
    ruta.append((fila, col))
    leer_pasos(n - 1, ruta, contador + 1)


# ---------- Imprimir una fila (recursivo) ----------
def imprimir_fila(fila, indice):
    """Imprime los elementos de una fila recursivamente."""
    if indice >= len(fila):
        print()  # salto de línea al terminar la fila
        return
    
    # Imprimir el elemento actual
    print(fila[indice], end=" ")
    
    # Imprimir el siguiente elemento
    imprimir_fila(fila, indice + 1)


# ---------- Imprimir todas las filas (recursivo) ----------
def imprimir_todas_filas(matriz, indice_fila):
    """Imprime todas las filas de la matriz recursivamente."""
    if indice_fila >= len(matriz):
        return
    
    # Imprimir la fila actual
    imprimir_fila(matriz[indice_fila], 0)
    
    # Imprimir la siguiente fila
    imprimir_todas_filas(matriz, indice_fila + 1)


# ---------- Imprimir la matriz con la ruta ----------
def imprimir_matriz(matriz, ruta):
    """Marca la ruta en una copia de la matriz y la imprime.
    - Todos los puntos de la ruta menos el último → *
    - El último punto (posición actual de Gabita)  → G
    """
    m = len(matriz)
    n = len(matriz[0])

    # Crear copia limpia
    copia = crear_matriz(m, n)

    # Marcar la ruta (recursiva)
    marcar_ruta(copia, ruta, 0)

    # Imprimir todas las filas recursivamente
    imprimir_todas_filas(copia, 0)


def marcar_ruta(copia, ruta, i):
    """Marca recursivamente cada punto de la ruta en la matriz.
    - Si es el último punto → 'G'
    - Si no → '*'
    """
    if i >= len(ruta):
        return
    
    fila = ruta[i][0]
    col = ruta[i][1]
    
    if i == len(ruta) - 1:
        copia[fila][col] = "G"   # posición actual
    else:
        copia[fila][col] = "*"   # ruta previa
    
    marcar_ruta(copia, ruta, i + 1)


# ---------- Bucle principal de comandos (recursivo) ----------
def procesar_comandos(matriz, ruta):
    """Lee comandos C / I / F de forma recursiva."""
    print()
    print("Ingresa un comando (C=agregar paso, I=imprimir, F=finalizar): ")
    comando = input()

    if comando == "F":
        print("¡Programa finalizado!")
        return                          # caso base → termina

    if comando == "C":
        print("Ingresa las coordenadas del nuevo paso (fila col): ")
        entrada = input()
        
        # Separar la entrada manualmente
        partes = entrada.split()
        fila = int(partes[0])
        col = int(partes[1])
        
        ruta.append((fila, col))        # agregar paso extra
        print("Paso agregado en (", fila, ",", col, ")")

    elif comando == "I":
        print()
        print("--- Estado actual de Gabita ---")
        imprimir_matriz(matriz, ruta)   # imprimir estado actual
        print("--- Fin del estado ---")

    # Caso recursivo → seguir leyendo el siguiente comando
    procesar_comandos(matriz, ruta)


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 50)
    print("    ¿DÓNDE ESTÁ GABITA? - Rastreador de Coneja")
    print("=" * 50)
    
    # 1) Leer dimensiones de la matriz
    print()
    print("Configuración inicial:")
    print("Ingresa las dimensiones de la matriz (filas columnas): ")
    entrada = input()
    
    # Separar la entrada manualmente
    partes = entrada.split()
    m = int(partes[0])
    n = int(partes[1])
    
    print("Matriz de", m, "x", n, "creada exitosamente.")

    # 2) Crear matriz vacía
    matriz = crear_matriz(m, n)

    # 3) Leer cantidad de pasos iniciales
    print()
    print("Ingresa la cantidad de pasos iniciales de Gabita: ")
    N = int(input())
    print("Se leerán", N, "coordenadas iniciales.")

    # 4) Leer los N pasos iniciales (recursivo)
    ruta = []
    print()
    print("--- Ingreso de pasos iniciales ---")
    leer_pasos(N, ruta, 1)
    print("Pasos iniciales registrados:", ruta)

    # 5) Entrar al bucle de comandos (recursivo)
    print()
    print("--- Modo interactivo iniciado ---")
    print("Comandos disponibles:")
    print("  C - Agregar un paso extra")
    print("  I - Mostrar posición actual de Gabita")
    print("  F - Finalizar programa")
    procesar_comandos(matriz, ruta)


if __name__ == "__main__":
    main()