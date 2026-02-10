"""
Tarea 3 - Estructuras de Datos
Procesamiento de Imágenes PGM con Algoritmos de Ordenamiento y Búsqueda
Autor: [Tu nombre]
Fecha: 09 de febrero de 2026
"""

from PIL import Image
import numpy as np
import time

# ================== FUNCIONES DE LECTURA Y ESCRITURA ==================

def readImgPGM(path):
    """Lee una imagen PGM y retorna el arreglo de intensidades"""
    img = Image.open(path)
    img_array = np.array(img)
    
    print(f"Image format: {img.format}")
    print(f"Image mode: {img.mode}")
    print(f"Image size (width, height): {img.size}")
    
    return img_array

def printImg(img_array, filename="modified_output.pgm"):
    """Guarda una imagen a partir de un arreglo numpy"""
    modified_img = Image.fromarray(img_array.astype('uint8'), 'L')
    modified_img.save(filename)
    print(f"\nImagen guardada como {filename}")

# ================== PARTE 1: LECTURA Y ESTRUCTURA DE DATOS ==================

def matriz_a_arreglo(matriz):
    """Convierte una matriz bidimensional en un arreglo unidimensional"""
    filas, columnas = matriz.shape
    arreglo = np.zeros(filas * columnas, dtype=int)
    
    idx = 0
    for i in range(filas):
        for j in range(columnas):
            arreglo[idx] = matriz[i][j]
            idx += 1
    
    return arreglo

# ================== PARTE 2: ALGORITMOS DE ORDENAMIENTO ==================

def bubble_sort(arr):
    """
    Implementación de Bubble Sort OPTIMIZADO
    Retorna: arreglo ordenado, número de comparaciones, tiempo de ejecución
    """
    n = len(arr)
    arr_copy = arr.copy()
    comparaciones = 0
    
    inicio = time.time()
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparaciones += 1
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        if not swapped:
            break
    
    tiempo = time.time() - inicio
    
    return arr_copy, comparaciones, tiempo

def insertion_sort(arr):
    """
    Implementación de Insertion Sort
    Retorna: arreglo ordenado, número de comparaciones, tiempo de ejecución
    """
    n = len(arr)
    arr_copy = arr.copy()
    comparaciones = 0
    
    inicio = time.time()
    
    for i in range(1, n):
        key = arr_copy[i]
        j = i - 1
        
        while j >= 0:
            comparaciones += 1
            if arr_copy[j] > key:
                arr_copy[j + 1] = arr_copy[j]
                j -= 1
            else:
                break
        
        arr_copy[j + 1] = key
    
    tiempo = time.time() - inicio
    
    return arr_copy, comparaciones, tiempo

def selection_sort(arr):
    """
    Implementación de Selection Sort
    Retorna: arreglo ordenado, número de comparaciones, tiempo de ejecución
    """
    n = len(arr)
    arr_copy = arr.copy()
    comparaciones = 0
    
    inicio = time.time()
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparaciones += 1
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
    
    tiempo = time.time() - inicio
    
    return arr_copy, comparaciones, tiempo

# ================== ALGORITMO EFICIENTE: MERGE SORT ==================

def merge_sort(arr):
    """
    Implementación de Merge Sort (algoritmo eficiente)
    Retorna: arreglo ordenado, número de comparaciones, tiempo de ejecución
    """
    comparaciones = [0]  # Usamos lista para pasar por referencia
    
    inicio = time.time()
    arr_copy = arr.copy()
    resultado = merge_sort_recursive(arr_copy, comparaciones)
    tiempo = time.time() - inicio
    
    return resultado, comparaciones[0], tiempo

def merge_sort_recursive(arr, comparaciones):
    """Función recursiva de Merge Sort"""
    if len(arr) <= 1:
        return arr
    
    # Dividir el arreglo en dos mitades
    medio = len(arr) // 2
    izquierda = merge_sort_recursive(arr[:medio], comparaciones)
    derecha = merge_sort_recursive(arr[medio:], comparaciones)
    
    # Combinar las mitades ordenadas
    return merge(izquierda, derecha, comparaciones)

def merge(izquierda, derecha, comparaciones):
    """Combina dos arreglos ordenados"""
    resultado = []
    i = j = 0
    
    while i < len(izquierda) and j < len(derecha):
        comparaciones[0] += 1
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    
    # Agregar elementos restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    
    return resultado

# ================== ALGORITMO EFICIENTE: QUICK SORT ==================

def quick_sort(arr):
    """
    Implementación de Quick Sort (algoritmo eficiente)
    Retorna: arreglo ordenado, número de comparaciones, tiempo de ejecución
    """
    comparaciones = [0]
    
    inicio = time.time()
    arr_copy = arr.copy()
    quick_sort_recursive(arr_copy, 0, len(arr_copy) - 1, comparaciones)
    tiempo = time.time() - inicio
    
    return arr_copy, comparaciones[0], tiempo

def quick_sort_recursive(arr, bajo, alto, comparaciones):
    """Función recursiva de Quick Sort"""
    if bajo < alto:
        pi = partition(arr, bajo, alto, comparaciones)
        quick_sort_recursive(arr, bajo, pi - 1, comparaciones)
        quick_sort_recursive(arr, pi + 1, alto, comparaciones)

def partition(arr, bajo, alto, comparaciones):
    """Particiona el arreglo para Quick Sort"""
    pivot = arr[alto]
    i = bajo - 1
    
    for j in range(bajo, alto):
        comparaciones[0] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1

# ================== CÁLCULOS ESTADÍSTICOS ==================

def calcular_moda(arr):
    """Calcula la moda (valor más frecuente) del arreglo"""
    # Contar frecuencias
    frecuencias = {}
    for valor in arr:
        if valor in frecuencias:
            frecuencias[valor] += 1
        else:
            frecuencias[valor] = 1
    
    # Encontrar el valor con mayor frecuencia
    moda = max(frecuencias, key=frecuencias.get)
    return moda

def crear_imagen_moda(matriz_original, moda):
    """
    Crea una imagen binaria basada en la moda:
    - Si el valor > moda: asigna 255 (blanco)
    - Si el valor <= moda: asigna 0 (negro)
    """
    filas, columnas = matriz_original.shape
    nueva_imagen = np.zeros((filas, columnas), dtype=int)
    
    for i in range(filas):
        for j in range(columnas):
            if matriz_original[i][j] > moda:
                nueva_imagen[i][j] = 255
            else:
                nueva_imagen[i][j] = 0
    
    return nueva_imagen

# ================== PARTE 3: BÚSQUEDA ==================

def busqueda_lineal(matriz, valor_buscado):
    """
    Búsqueda lineal en la matriz original
    Retorna: coordenadas (fila, columna) de la primera ocurrencia, o None
    """
    filas, columnas = matriz.shape
    
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == valor_buscado:
                return (i, j)
    
    return None

def busqueda_binaria(arr_ordenado, valor_buscado):
    """
    Búsqueda binaria en arreglo ordenado
    Retorna: True si existe, False si no existe
    """
    izquierda = 0
    derecha = len(arr_ordenado) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        
        if arr_ordenado[medio] == valor_buscado:
            return True
        elif arr_ordenado[medio] < valor_buscado:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return False

def contar_ocurrencias(arr, valor):
    """Cuenta cuántas veces aparece un valor en el arreglo"""
    contador = 0
    for elemento in arr:
        if elemento == valor:
            contador += 1
    return contador

def encontrar_todas_coordenadas(matriz, valor):
    """Encuentra todas las coordenadas donde aparece un valor"""
    coordenadas = []
    filas, columnas = matriz.shape
    
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == valor:
                coordenadas.append((i, j))
    
    return coordenadas

# ================== PROGRAMA PRINCIPAL ==================

def main():
    print("="*70)
    print("TAREA 3 - ESTRUCTURAS DE DATOS")
    print("Procesamiento de Imágenes PGM")
    print("="*70)
    
    # ===== PARTE 1: Lectura y Estructura de Datos =====
    print("\n" + "="*70)
    print("PARTE 1: LECTURA Y ESTRUCTURA DE DATOS")
    print("="*70)
    
    path = "eo.pgm"
    print(f"\nLeyendo imagen: {path}")
    matriz_original = readImgPGM(path)
    
    print(f"\nDimensiones de la matriz: {matriz_original.shape}")
    
    # Convertir matriz a arreglo unidimensional
    print("\nConvirtiendo matriz bidimensional a arreglo unidimensional...")
    arreglo_1d = matriz_a_arreglo(matriz_original)
    print(f"Tamaño del arreglo unidimensional: {len(arreglo_1d)} elementos")
    
    # ===== PARTE 2: Ordenamiento de Intensidades =====
    print("\n" + "="*70)
    print("PARTE 2: ORDENAMIENTO DE INTENSIDADES")
    print("="*70)
    
    print("\nEjecutando algoritmos de ordenamiento...")
    print("NOTA: Los algoritmos O(n²) se ejecutarán con muestra de 100,000 elementos.")
    print("Esto tomará aproximadamente 10-15 minutos en total.\n")
    
    # Muestra para algoritmos lentos (100,000 elementos = ~15 min total)
    muestra_size = 100000
    muestra = arreglo_1d[:muestra_size].copy()
    
    print(f"Probando algoritmos con muestra de {muestra_size:,} elementos:")
    print("-" * 70)
    
    # Bubble Sort (muestra de 100k)
    print("\n1. BUBBLE SORT (muestra optimizado)")
    print("   Ejecutando... (esto puede tomar 5-7 minutos)")
    arr_bubble, comp_bubble, tiempo_bubble = bubble_sort(muestra)
    print(f"   Comparaciones: {comp_bubble:,}")
    print(f"   Tiempo de ejecución: {tiempo_bubble:.4f} segundos ({tiempo_bubble/60:.2f} minutos)")
    print(f"   ¿Terminó? SÍ")
    
    # Insertion Sort (muestra de 100k)
    print("\n2. INSERTION SORT (muestra)")
    print("   Ejecutando... (esto puede tomar 3-5 minutos)")
    arr_insertion, comp_insertion, tiempo_insertion = insertion_sort(muestra)
    print(f"   Comparaciones: {comp_insertion:,}")
    print(f"   Tiempo de ejecución: {tiempo_insertion:.4f} segundos ({tiempo_insertion/60:.2f} minutos)")
    print(f"   ¿Terminó? SÍ")
    
    # Selection Sort (muestra de 100k)
    print("\n3. SELECTION SORT (muestra)")
    print("   Ejecutando... (esto puede tomar 4-6 minutos)")
    arr_selection, comp_selection, tiempo_selection = selection_sort(muestra)
    print(f"   Comparaciones: {comp_selection:,}")
    print(f"   Tiempo de ejecución: {tiempo_selection:.4f} segundos ({tiempo_selection/60:.2f} minutos)")
    print(f"   ¿Terminó? SÍ")
    
    # Merge Sort (imagen completa)
    print("\n4. MERGE SORT (imagen completa - algoritmo eficiente)")
    print("   Ordenando 1,440,000 elementos...")
    arr_merge, comp_merge, tiempo_merge = merge_sort(arreglo_1d)
    print(f"   Comparaciones aproximadas: {comp_merge:,}")
    print(f"   Tiempo de ejecución: {tiempo_merge:.4f} segundos")
    print(f"   ¿Terminó? SÍ")
    
    # Quick Sort (imagen completa)
    print("\n5. QUICK SORT (imagen completa - algoritmo eficiente)")
    print("   Ordenando 1,440,000 elementos...")
    arr_quick, comp_quick, tiempo_quick = quick_sort(arreglo_1d)
    print(f"   Comparaciones aproximadas: {comp_quick:,}")
    print(f"   Tiempo de ejecución: {tiempo_quick:.4f} segundos")
    print(f"   ¿Terminó? SÍ")
    
    # Usar el resultado de merge sort para estadísticas
    arr_ordenado = arr_merge
    
    # Estadísticas del arreglo ordenado
    print("\n" + "-" * 70)
    print("ESTADÍSTICAS DE LA IMAGEN:")
    print("-" * 70)
    intensidad_min = arr_ordenado[0]
    intensidad_max = arr_ordenado[-1]
    intensidad_mediana = arr_ordenado[len(arr_ordenado) // 2]
    
    print(f"Intensidad mínima: {intensidad_min}")
    print(f"Intensidad máxima: {intensidad_max}")
    print(f"Intensidad mediana: {intensidad_mediana}")
    
    # Calcular moda
    print("\nCalculando moda...")
    moda = calcular_moda(arreglo_1d)
    print(f"Moda (valor más frecuente): {moda}")
    
    # Crear imagen basada en moda
    print("\nCreando imagen binaria basada en la moda...")
    imagen_moda = crear_imagen_moda(matriz_original, moda)
    printImg(imagen_moda, "imagen_moda.pgm")
    print("Imagen de moda guardada exitosamente.")
    
    # ===== PARTE 3: Búsqueda en la Imagen =====
    print("\n" + "="*70)
    print("PARTE 3: BÚSQUEDA EN LA IMAGEN")
    print("="*70)
    
    # Solicitar intensidad al usuario
    print("\nIngrese una intensidad de gris a buscar (0-255):")
    try:
        intensidad_buscar = int(input("Intensidad: "))
        
        if intensidad_buscar < 0 or intensidad_buscar > 255:
            print("Error: La intensidad debe estar entre 0 y 255")
            return
        
        print(f"\nBuscando intensidad: {intensidad_buscar}")
        print("-" * 70)
        
        # Búsqueda lineal en matriz original
        print("\n1. BÚSQUEDA LINEAL (en matriz original)")
        coordenada = busqueda_lineal(matriz_original, intensidad_buscar)
        
        if coordenada:
            print(f"   Primera ocurrencia encontrada en: fila {coordenada[0]}, columna {coordenada[1]}")
        else:
            print("   No se encontró la intensidad en la imagen")
        
        # Búsqueda binaria en arreglo ordenado
        print("\n2. BÚSQUEDA BINARIA (en arreglo ordenado)")
        existe = busqueda_binaria(arr_ordenado, intensidad_buscar)
        print(f"   ¿Existe la intensidad? {'SÍ' if existe else 'NO'}")
        
        # Si existe, contar ocurrencias y mostrar coordenadas
        if existe:
            print("\n3. INFORMACIÓN ADICIONAL:")
            
            num_ocurrencias = contar_ocurrencias(arreglo_1d, intensidad_buscar)
            print(f"   Número de ocurrencias: {num_ocurrencias:,}")
            
            # Mostrar algunas coordenadas (máximo 5 para no saturar)
            coordenadas = encontrar_todas_coordenadas(matriz_original, intensidad_buscar)
            print(f"\n   Coordenadas donde aparece (primeras 5):")
            for i, coord in enumerate(coordenadas[:5]):
                print(f"   - Posición {i+1}: fila {coord[0]}, columna {coord[1]}")
            
            if len(coordenadas) > 5:
                print(f"   ... y {len(coordenadas) - 5} ocurrencias más")
        
    except ValueError:
        print("Error: Debe ingresar un número entero")
    except EOFError:
        # Modo automático para testing
        print("\nModo automático activado (testing)")
        intensidad_buscar = int(moda)
        print(f"Buscando la moda: {intensidad_buscar}")
        
        coordenada = busqueda_lineal(matriz_original, intensidad_buscar)
        if coordenada:
            print(f"Primera ocurrencia: fila {coordenada[0]}, columna {coordenada[1]}")
        
        existe = busqueda_binaria(arr_ordenado, intensidad_buscar)
        print(f"Existe: {'SÍ' if existe else 'NO'}")
        
        if existe:
            num_ocurrencias = contar_ocurrencias(arreglo_1d, intensidad_buscar)
            print(f"Ocurrencias: {num_ocurrencias:,}")
    
    print("\n" + "="*70)
    print("PROGRAMA FINALIZADO")
    print("="*70)

# ================== ANÁLISIS CONCEPTUAL (PARTE 4) ==================
"""
PARTE 4: ANÁLISIS CONCEPTUAL

1. ¿Por qué la búsqueda binaria no puede aplicarse directamente a la matriz
original de la imagen?

La búsqueda binaria requiere que los datos estén ORDENADOS. En la matriz
original de la imagen, los valores representan intensidades de píxeles en
su posición espacial (fila, columna), y estos valores NO están ordenados.
Los píxeles vecinos pueden tener valores muy diferentes. Por ejemplo:
- Píxel (0,0) podría tener intensidad 44
- Píxel (0,1) podría tener intensidad 44
- Píxel (0,2) podría tener intensidad 43

La búsqueda binaria divide el espacio de búsqueda a la mitad en cada paso,
comparando con el elemento del medio. Esto solo funciona si sabemos que
los valores menores están a la izquierda y los mayores a la derecha, lo
cual NO es cierto en una matriz de imagen donde el orden es espacial,
no numérico.

2. ¿Qué ventajas ofrece ordenar las intensidades antes de realizar búsquedas?

Ventajas principales:

a) EFICIENCIA: La búsqueda binaria tiene complejidad O(log n), mucho más
    rápida que la búsqueda lineal O(n). Para una imagen de 1,440,000 píxeles:
    - Búsqueda lineal: hasta 1,440,000 comparaciones
    - Búsqueda binaria: aproximadamente 21 comparaciones

b) ESTADÍSTICAS INMEDIATAS: Con datos ordenados podemos obtener:
    - Mínimo: primer elemento
    - Máximo: último elemento
    - Mediana: elemento del medio
    Todas estas operaciones son O(1) en vez de O(n)

c) ANÁLISIS DE DISTRIBUCIÓN: Un arreglo ordenado facilita encontrar rangos,
    percentiles, y analizar la distribución de intensidades.

d) OPTIMIZACIÓN DE BÚSQUEDAS REPETIDAS: Si necesitamos buscar múltiples
    valores, el costo de ordenar una vez (O(n log n)) se amortiza sobre
    múltiples búsquedas binarias rápidas.

3. ¿En qué situaciones la búsqueda lineal sigue siendo una opción adecuada?

La búsqueda lineal es adecuada cuando:

a) BÚSQUEDA POR POSICIÓN: Cuando necesitamos las coordenadas (fila, columna)
    exactas donde aparece un valor, como en esta tarea. La búsqueda binaria
    solo nos dice SI existe, pero no DÓNDE está en la imagen original.

b) DATOS PEQUEÑOS: Para conjuntos muy pequeños (< 100 elementos), la
    diferencia de rendimiento es insignificante y la búsqueda lineal es
    más simple de implementar.

c) DATOS NO ORDENADOS: Cuando ordenar los datos es costoso o imposible,
    y solo necesitamos hacer una búsqueda ocasional.

d) BÚSQUEDA DEL PRIMER ELEMENTO: Si sabemos que el elemento buscado está
    probablemente al inicio de los datos, la búsqueda lineal puede ser más
    rápida que ordenar primero.

e) CRITERIOS COMPLEJOS: Cuando buscamos con criterios que no son simples
    comparaciones de igualdad (ej: "pixeles con intensidad entre 40 y 50
    Y en la región superior izquierda").

f) DATOS DINÁMICOS: Si los datos cambian frecuentemente, mantener el orden
    puede ser más costoso que hacer búsquedas lineales.
"""

if __name__ == "__main__":
    main()
