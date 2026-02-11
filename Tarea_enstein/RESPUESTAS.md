# Tarea 3: Procesamiento de Imagen PGM - Respuestas

## Parte 4: Análisis Conceptual

### 1. ¿Por qué la búsqueda binaria no puede aplicarse directamente a la matriz original de la imagen?

La búsqueda binaria requiere que los datos estén **ordenados** para funcionar correctamente. El algoritmo divide el espacio de búsqueda a la mitad en cada iteración, asumiendo que los elementos menores están a un lado y los mayores al otro.

En una matriz 2D de imagen:
- Los píxeles están distribuidos espacialmente según su posición en la imagen, no por valor de intensidad
- No existe garantía de que los valores estén ordenados en ninguna dirección (ni por filas, ni por columnas)
- Aplicar búsqueda binaria directamente daría resultados incorrectos

**Solución:** Convertir la matriz 2D a un arreglo 1D y ordenarlo primero.

---

### 2. ¿Qué ventajas ofrece ordenar las intensidades antes de realizar búsquedas?

| Ventaja | Descripción |
|---------|-------------|
| **Búsqueda más rápida** | Permite usar búsqueda binaria: O(log n) vs O(n) de búsqueda lineal |
| **Estadísticas directas** | Mínimo, máximo y mediana se obtienen trivialmente del arreglo ordenado |
| **Análisis de distribución** | Facilita identificar patrones, frecuencias y valores atípicos |
| **Eficiencia en grandes volúmenes** | Con millones de píxeles, la diferencia es significativa |
| **Procesamiento por rangos** | Permite buscar intervalos de intensidades rápidamente |

**Ejemplo:** En una imagen de 1200×1200 (1.44M píxeles):
- Búsqueda lineal: ~720,000 comparaciones en promedio
- Búsqueda binaria: ~20 comparaciones máximo

---

### 3. ¿En qué situaciones la búsqueda lineal sigue siendo una opción adecuada?

La búsqueda lineal es apropiada cuando:

1. **Datos no ordenados y no se puede ordenar**
   - Si necesitas buscar en la matriz original sin modificarla
   - Cuando el costo de ordenamiento es mayor que el beneficio

2. **Conjuntos pequeños**
   - Menos de 1000 elementos: la diferencia de velocidad es imperceptible
   - Overhead de búsqueda binaria no compensa

3. **Búsquedas únicas**
   - Si solo necesitas buscar una vez, ordenar primero es ineficiente
   - Mejor hacer una búsqueda lineal directa

4. **Necesitas todas las ocurrencias**
   - Para contar cuántas veces aparece un valor
   - Búsqueda lineal recorre todo; búsqueda binaria solo verifica existencia

5. **Datos con estructura especial**
   - Si los datos tienen propiedades que hacen la búsqueda lineal eficiente
   - Ej: valores agrupados al inicio del arreglo

**En esta tarea:** La búsqueda lineal es ideal para encontrar la **primera ocurrencia** y **contar todas las ocurrencias** en la matriz original.

---

## Resumen de Resultados

### Algoritmos Implementados

#### Bubble Sort
- **Complejidad:** O(n²)
- **Comparaciones:** n(n-1)/2 ≈ 1.44M × 1.44M / 2
- **Uso:** Educativo, no recomendado para datos grandes

#### Merge Sort
- **Complejidad:** O(n log n)
- **Comparaciones:** n log n ≈ 1.44M × 20 ≈ 28.8M
- **Ventaja:** Mucho más rápido que Bubble Sort, garantizado O(n log n)

### Estadísticas de la Imagen
- **Tamaño:** 1200 × 1200 píxeles
- **Total de píxeles:** 1,440,000
- **Rango de intensidades:** [0-255]
- **Moda:** Valor más frecuente en la imagen
- **Mediana:** Valor central cuando se ordenan todas las intensidades

### Imagen Procesada
Se genera `imagen_moda.pgm` donde:
- Píxeles con intensidad ≥ moda → 255 (blanco)
- Píxeles con intensidad < moda → 0 (negro)

Esto crea una imagen binaria que separa los píxeles más claros de los más oscuros.
