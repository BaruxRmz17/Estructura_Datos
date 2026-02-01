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
    fila, col = map(int, input(f"Ingresa las coordenadas del paso {len(ruta) + 1} (fila col): ").split())
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
    comando = input("\nIngresa un comando (C=agregar paso, I=imprimir, F=finalizar): ").strip()

    if comando == "F":
        print("¡Programa finalizado!")
        return                          # caso base → termina

    if comando == "C":
        fila, col = map(int, input("Ingresa las coordenadas del nuevo paso (fila col): ").split())
        ruta.append((fila, col))        # agregar paso extra
        print(f"Paso agregado en ({fila}, {col})")

    elif comando == "I":
        print("\n--- Estado actual de Gabita ---")
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
    print("\nConfiguración inicial:")
    m, n = map(int, input("Ingresa las dimensiones de la matriz (filas columnas): ").split())
    print(f"Matriz de {m}x{n} creada exitosamente.")

    # 2) Crear matriz vacía
    matriz = crear_matriz(m, n)

    # 3) Leer cantidad de pasos iniciales
    N = int(input(f"\nIngresa la cantidad de pasos iniciales de Gabita: "))
    print(f"Se leerán {N} coordenadas iniciales.")

    # 4) Leer los N pasos iniciales (recursivo)
    ruta = []
    print("\n--- Ingreso de pasos iniciales ---")
    leer_pasos(N, ruta)
    print(f"Pasos iniciales registrados: {ruta}")

    # 5) Entrar al bucle de comandos (recursivo)
    print("\n--- Modo interactivo iniciado ---")
    print("Comandos disponibles:")
    print("  C - Agregar un paso extra")
    print("  I - Mostrar posición actual de Gabita")
    print("  F - Finalizar programa")
    procesar_comandos(matriz, ruta)


if __name__ == "__main__":
    main()