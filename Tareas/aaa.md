# Explicación Detallada del Código Tarea_3.py

## Librerías Utilizadas

```python
from PIL import Image
import numpy as np
import time
```

| Librería | Por qué | Qué hace |
|----------|---------|----------|
| **PIL (Image)** | Necesaria para leer archivos PGM | Abre y convierte imágenes a matrices numéricas |
| **NumPy** | Manejo eficiente de matrices grandes | Operaciones rápidas con arreglos 2D y 1D |
| **time** | Medir rendimiento de algoritmos | Calcula tiempo de ejecución de cada ordenamiento |

---

## PARTE 1: Lectura y Estructura de Datos

### `readImgPGM(path)`

**Por qué existe:**
- El archivo PGM es un formato especial que necesita ser interpretado correctamente
- Necesitamos extraer la información de la imagen y convertirla a datos numéricos

**Qué hace:**
```python
img = Image.open(path)           # Abre el archivo PGM
img_array = np.array(img)        # Convierte a matriz NumPy
```
- Transforma el archivo PGM en una matriz 2D donde cada número es la intensidad de un píxel
- Imprime información: formato, modo (L = escala de grises), tamaño

**Retorna:** Matriz 2D con valores 0-255

---

### `matriz_a_arreglo(matriz)`

**Por qué existe:**
- Los algoritmos de ordenamiento trabajan mejor con arreglos 1D
- Necesitamos todos los píxeles en una sola dimensión para ordenarlos

**Qué hace:**
```python
return matriz.flatten()  # Convierte 2D → 1D
```
- Transforma matriz 1200×1200 en arreglo de 1,440,000 elementos
- Mantiene todos los valores, solo cambia la estructura

**Ejemplo:**
```
Matriz 2D:        Arreglo 1D:
[44, 44, 44]  →   [44, 44, 44, 42, 41, 41, ...]
[42, 41, 41]
```

---

## PARTE 2: Ordenamiento

### `bubble_sort(arr)`

**Por qué existe:**
- Es un algoritmo simple para entender cómo funciona el ordenamiento
- Sirve como referencia para comparar con algoritmos más eficientes

**Qué hace:**
```python
for i in range(n):
    for j in range(0, n - i - 1):
        comparaciones += 1
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambia
```
- Compara elementos adyacentes
- Si el izquierdo es mayor, los intercambia
- Repite hasta que todo esté ordenado

**Complejidad:** O(n²) - Muy lento para 1.44M elementos

---

### `merge_sort(arr)`

**Por qué existe:**
- Es mucho más rápido que Bubble Sort
- Garantiza O(n log n) incluso en el peor caso
- Necesario para procesar imágenes grandes eficientemente

**Qué hace:**
```python
def merge_sort_rec(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_rec(arr[:mid])      # Divide izquierda
    right = merge_sort_rec(arr[mid:])     # Divide derecha
    return merge(left, right)              # Combina ordenado
```

**Estrategia "Divide y Conquista":**
1. Divide el arreglo en mitades recursivamente
2. Ordena cada mitad
3. Combina las mitades manteniendo orden

**Complejidad:** O(n log n) - ~20 veces más rápido que Bubble Sort

---

### `calcular_estadisticas(arr_ordenado)`

**Por qué existe:**
- Una vez ordenado, obtener min/max/mediana es trivial
- Sin ordenamiento, calcular mediana requeriría O(n) extra

**Qué hace:**
```python
minimo = arr_ordenado[0]           # Primer elemento = mínimo
maximo = arr_ordenado[-1]          # Último elemento = máximo
mediana = arr_ordenado[n // 2]     # Elemento central = mediana
```

**Por qué funciona:**
- En arreglo ordenado, el menor está al inicio
- El mayor está al final
- El del medio es la mediana

---

### `calcular_moda(arr)`

**Por qué existe:**
- Necesitamos encontrar el valor más frecuente para crear la imagen binaria
- NumPy tiene función optimizada para esto

**Qué hace:**
```python
unique, counts = np.unique(arr, return_counts=True)
moda = unique[np.argmax(counts)]
```
- `np.unique()` encuentra valores únicos y sus frecuencias
- `np.argmax()` encuentra el índice del valor más frecuente
- Retorna ese valor

**Ejemplo:**
```
Arreglo: [50, 50, 50, 100, 100, 200]
Únicos:  [50, 100, 200]
Conteos: [3, 2, 1]
Moda:    50 (aparece 3 veces)
```

---

### `aplicar_moda_a_imagen(matriz, moda)`

**Por qué existe:**
- Necesitamos crear una imagen binaria basada en la moda
- Separa píxeles claros (≥ moda) de oscuros (< moda)

**Qué hace:**
```python
resultado = np.where(matriz > moda, 255, 0)
```
- Si píxel > moda → asigna 255 (blanco)
- Si píxel ≤ moda → asigna 0 (negro)

**Resultado:** Imagen de solo 2 colores (blanco y negro)

---

### `guardar_imagen(img_array, nombre_archivo)`

**Por qué existe:**
- Necesitamos guardar la imagen procesada en formato PGM
- Permite visualizar el resultado

**Qué hace:**
```python
img = Image.fromarray(img_array.astype('uint8'), 'L')
img.save(nombre_archivo)
```
- Convierte arreglo NumPy a imagen PIL
- `uint8` = valores 0-255
- `'L'` = escala de grises
- Guarda como archivo PGM

---

## PARTE 3: Búsqueda

### `busqueda_lineal(matriz, valor)`

**Por qué existe:**
- Necesitamos encontrar TODAS las ocurrencias de un valor
- Necesitamos la coordenada (fila, columna) de la primera ocurrencia
- Búsqueda binaria no puede hacer esto

**Qué hace:**
```python
for i in range(filas):
    for j in range(columnas):
        if matriz[i, j] == valor:
            contador += 1
            if primera_posicion is None:
                primera_posicion = (i, j)
```
- Recorre TODA la matriz
- Cuenta cuántas veces aparece el valor
- Guarda la primera posición encontrada

**Retorna:** `(fila, columna), contador`

**Complejidad:** O(n) - Recorre todos los elementos

---

### `busqueda_binaria(arr_ordenado, valor)`

**Por qué existe:**
- Verifica rápidamente si un valor existe en el arreglo ordenado
- Mucho más rápido que búsqueda lineal para verificación

**Qué hace:**
```python
while izq <= der:
    mid = (izq + der) // 2
    if arr_ordenado[mid] == valor:
        return True
    elif arr_ordenado[mid] < valor:
        izq = mid + 1  # Busca en la derecha
    else:
        der = mid - 1  # Busca en la izquierda
```

**Estrategia:**
1. Compara con el elemento del medio
2. Si es igual → encontrado
3. Si es menor → busca en la mitad derecha
4. Si es mayor → busca en la mitad izquierda
5. Repite hasta encontrar o agotar opciones

**Complejidad:** O(log n) - Solo ~20 comparaciones para 1.44M elementos

---

## PARTE 4: Main - Flujo del Programa

### Estructura General

```python
def main():
    # 1. Lee imagen
    matriz = readImgPGM(path)
    arreglo = matriz_a_arreglo(matriz)
    
    # 2. Ordena con dos algoritmos
    arr_bubble, comp_bubble = bubble_sort(arreglo)
    arr_merge, comp_merge = merge_sort(arreglo)
    
    # 3. Calcula estadísticas
    minimo, maximo, mediana = calcular_estadisticas(arr_merge)
    moda = calcular_moda(arreglo)
    
    # 4. Crea imagen binaria
    imagen_modificada = aplicar_moda_a_imagen(matriz, moda)
    guardar_imagen(imagen_modificada, "imagen_moda.pgm")
    
    # 5. Busca valor
    posicion, contador = busqueda_lineal(matriz, valor_buscar)
    existe = busqueda_binaria(arr_merge, valor_buscar)
```

---

## Optimización: Reutilizar Datos de Búsqueda Lineal

### El Problema Original
```python
# Búsqueda binaria solo retorna True/False
existe = busqueda_binaria(arr_merge, valor_buscar)
print(f"Valor existe: {'Sí' if existe else 'No'}")
```
- No muestra coordenada ni conteo
- Requeriría recorrer la matriz nuevamente

### La Solución
```python
# Búsqueda lineal ya tiene toda la información
posicion, contador = busqueda_lineal(matriz, valor_buscar)

# Búsqueda binaria solo verifica
existe = busqueda_binaria(arr_merge, valor_buscar)

# Si existe, reutiliza datos de búsqueda lineal
if existe:
    print(f"Primera ocurrencia: Fila {posicion[0]}, Columna {posicion[1]}")
    print(f"Total de ocurrencias: {contador}")
```

**Ventaja:** Sin recorrer la matriz nuevamente, mostramos toda la información

---

## Resumen de Decisiones de Diseño

| Decisión | Razón |
|----------|-------|
| Usar NumPy | Operaciones rápidas con matrices grandes |
| Bubble Sort + Merge Sort | Comparar eficiencia: O(n²) vs O(n log n) |
| Arreglo 1D para ordenamiento | Los algoritmos de ordenamiento trabajan mejor en 1D |
| Mantener matriz 2D original | Necesaria para búsqueda lineal con coordenadas |
| Búsqueda lineal + binaria | Lineal para contar/coordenadas, binaria para verificación |
| Reutilizar datos | Evitar recorrer la matriz múltiples veces |
| Imagen binaria con moda | Umbralización automática basada en distribución |

