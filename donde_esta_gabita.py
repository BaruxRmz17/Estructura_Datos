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
def leer_pasos(n, ruta):
    """Lee n pares de coordenadas de forma recursiva y los agrega a la ruta."""
    if n == 0:
        return
    fila, col = map(int, input().split())
    ruta.append((fila, col))
    leer_pasos(n - 1, ruta)


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

    # Imprimir cada fila
    for fila in copia:
        print(" ".join(str(x) for x in fila))


def marcar_ruta(copia, ruta, i):
    """Marca recursivamente cada punto de la ruta en la matriz.
    - Si es el último punto → 'G'
    - Si no → '*'
    """
    if i >= len(ruta):
        return
    fila, col = ruta[i]
    if i == len(ruta) - 1:
        copia[fila][col] = "G"   # posición actual
    else:
        copia[fila][col] = "*"   # ruta previa
    marcar_ruta(copia, ruta, i + 1)


# ---------- Bucle principal de comandos (recursivo) ----------
def procesar_comandos(matriz, ruta):
    """Lee comandos C / I / F de forma recursiva."""
    comando = input().strip()

    if comando == "F":
        return                          # caso base → termina

    if comando == "C":
        fila, col = map(int, input().split())
        ruta.append((fila, col))        # agregar paso extra

    elif comando == "I":
        imprimir_matriz(matriz, ruta)   # imprimir estado actual

    # Caso recursivo → seguir leyendo el siguiente comando
    procesar_comandos(matriz, ruta)


# ============================================================
# MAIN
# ============================================================
def main():
    # 1) Leer dimensiones de la matriz
    m, n = map(int, input().split())

    # 2) Crear matriz vacía
    matriz = crear_matriz(m, n)

    # 3) Leer cantidad de pasos iniciales
    N = int(input())

    # 4) Leer los N pasos iniciales (recursivo)
    ruta = []
    leer_pasos(N, ruta)

    # 5) Entrar al bucle de comandos (recursivo)
    procesar_comandos(matriz, ruta)


if __name__ == "__main__":
    main()