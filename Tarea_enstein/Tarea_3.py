from PIL import Image
import numpy as np
import time

# ============= PARTE 1: LECTURA Y ESTRUCTURA DE DATOS =============

def readImgPGM(path):
    img = Image.open(path)
    img_array = np.array(img)
    
    print(f"Formato de imagen: {img.format}")
    print(f"Modo de imagen: {img.mode}")
    print(f"Tamaño (ancho, alto): {img.size}")
    print(f"Dimensiones matriz: {img_array.shape}\n")
    
    return img_array

def matriz_a_arreglo(matriz):
    return matriz.flatten()

# ============= PARTE 2: ORDENAMIENTO =============

def bubble_sort(arr, tiempo_limite=900):
    arr = arr.copy()
    n = len(arr)
    comparaciones = 0
    inicio = time.time()
    
    for i in range(n):
        for j in range(0, n - i - 1):
            comparaciones += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            
            if time.time() - inicio > tiempo_limite:
                return arr, comparaciones, False
    
    return arr, comparaciones, True

def merge_sort(arr):
    comparaciones = [0]
    
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparaciones[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_sort_rec(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort_rec(arr[:mid])
        right = merge_sort_rec(arr[mid:])
        return merge(left, right)
    
    arr_sorted = merge_sort_rec(arr.copy())
    return arr_sorted, comparaciones[0]

def calcular_estadisticas(arr_ordenado):
    minimo = arr_ordenado[0]
    maximo = arr_ordenado[-1]
    n = len(arr_ordenado)
    if n % 2 == 0:
        mediana = (arr_ordenado[n // 2 - 1] + arr_ordenado[n // 2]) / 2
    else:
        mediana = arr_ordenado[n // 2]
    
    return minimo, maximo, mediana

def calcular_moda(arr):
    unique, counts = np.unique(arr, return_counts=True)
    moda = unique[np.argmax(counts)]
    return moda

def aplicar_moda_a_imagen(matriz, moda):
    resultado = np.where(matriz > moda, 255, 0)
    return resultado

def guardar_imagen(img_array, nombre_archivo):
    img = Image.fromarray(img_array.astype('uint8'), 'L')
    img.save(nombre_archivo)
    print(f"Imagen guardada como: {nombre_archivo}\n")

# ============= PARTE 3: BÚSQUEDA =============

def busqueda_lineal(matriz, valor):
    filas, columnas = matriz.shape
    contador = 0
    primera_posicion = None
    
    for i in range(filas):
        for j in range(columnas):
            if matriz[i, j] == valor:
                contador += 1
                if primera_posicion is None:
                    primera_posicion = (i, j)
    
    return primera_posicion, contador

def busqueda_binaria(arr_ordenado, valor):
    izq, der = 0, len(arr_ordenado) - 1
    
    while izq <= der:
        mid = (izq + der) // 2
        if arr_ordenado[mid] == valor:
            return True
        elif arr_ordenado[mid] < valor:
            izq = mid + 1
        else:
            der = mid - 1
    
    return False

# ============= MAIN =============

def main():
    # Parte 1: Lectura
    print("=" * 60)
    print("PARTE 1: LECTURA Y ESTRUCTURA DE DATOS")
    print("=" * 60)
    
    path = "eo.pgm"
    matriz = readImgPGM(path)
    arreglo = matriz_a_arreglo(matriz)
    
    print(f"Total de píxeles: {len(arreglo)}")
    print(f"Rango de intensidades: [{arreglo.min()}, {arreglo.max()}]\n")
    
    # Parte 2: Ordenamiento
    print("=" * 60)
    print("PARTE 2: ORDENAMIENTO DE INTENSIDADES")
    print("=" * 60)
    
    # Bubble Sort
    print("\n--- BUBBLE SORT ---")
    inicio = time.time()
    arr_bubble, comp_bubble, termino_bubble = bubble_sort(arreglo)
    tiempo_bubble = time.time() - inicio
    print(f"Comparaciones aproximadas: {comp_bubble:,}")
    print(f"Tiempo de ejecución: {tiempo_bubble:.4f} segundos")
    print(f"¿Terminó?: {'Sí' if termino_bubble else 'No (límite de 15 min alcanzado)'}\n")
    
    # Merge Sort
    print("--- MERGE SORT ---")
    inicio = time.time()
    arr_merge, comp_merge = merge_sort(arreglo)
    tiempo_merge = time.time() - inicio
    print(f"Comparaciones aproximadas: {comp_merge:,}")
    print(f"Tiempo de ejecución: {tiempo_merge:.4f} segundos")
    print(f"¿Terminó?: Sí\n")
    
    # Estadísticas
    print("--- ESTADÍSTICAS DEL ARREGLO ORDENADO ---")
    minimo, maximo, mediana = calcular_estadisticas(arr_merge)
    print(f"Intensidad mínima: {minimo}")
    print(f"Intensidad máxima: {maximo}")
    print(f"Intensidad mediana: {mediana}\n")
    
    # Moda
    print("--- MODA ---")
    moda = calcular_moda(arreglo)
    print(f"Moda (valor más frecuente): {moda}\n")
    
    # Aplicar moda a imagen
    print("--- APLICANDO UMBRAL DE MODA ---")
    imagen_modificada = aplicar_moda_a_imagen(matriz, moda)
    guardar_imagen(imagen_modificada, "imagen_moda.pgm")
    
    # Parte 3: Búsqueda
    print("=" * 60)
    print("PARTE 3: BÚSQUEDA EN LA IMAGEN")
    print("=" * 60)
    
    valor_buscar = int(input("\nIngresa una intensidad de gris a buscar (0-255): "))
    
    if 0 <= valor_buscar <= 255:
        # Búsqueda lineal
        print("\n--- BÚSQUEDA LINEAL ---")
        posicion, contador = busqueda_lineal(matriz, valor_buscar)
        
        if posicion:
            print(f"Valor encontrado: Sí")
            print(f"Primera ocurrencia en: Fila {posicion[0]}, Columna {posicion[1]}")
            print(f"Total de ocurrencias: {contador}")
        else:
            print(f"Valor encontrado: No")
        
        # Búsqueda binaria
        print("\n--- BÚSQUEDA BINARIA ---")
        existe = busqueda_binaria(arr_merge, valor_buscar)
        if existe:
            print(f"Valor existe en imagen: Sí")
            print(f"Primera ocurrencia en: Fila {posicion[0]}, Columna {posicion[1]}")
            print(f"Total de ocurrencias: {contador}")
        else:
            print(f"Valor existe en imagen: No")
    else:
        print("Valor inválido. Debe estar entre 0 y 255.")
    
    # Parte 4: Análisis conceptual (en archivo MD)
    print("\n" + "=" * 60)
    print("ANÁLISIS CONCEPTUAL - Ver archivo RESPUESTAS.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
