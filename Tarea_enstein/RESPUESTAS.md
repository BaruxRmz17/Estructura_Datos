**1. ¿Por qué la búsqueda binaria no puede aplicarse directamente a la matriz original de la imagen?**

Porque la búsqueda binaria solo funciona cuando los datos están **ordenados**, y la matriz original de la imagen no lo está.
Los valores de intensidad están distribuidos según la imagen, no en orden ascendente o descendente, así que aplicar búsqueda binaria ahí no tendría sentido ni daría resultados correctos.

---

**2. ¿Qué ventajas ofrece ordenar las intensidades antes de realizar búsquedas?**

Ordenar las intensidades permite usar algoritmos mucho más rápidos como la búsqueda binaria.
En lugar de revisar todos los valores uno por uno, la búsqueda se hace dividiendo el arreglo en partes, lo que reduce muchísimo el tiempo.
Además, al tener el arreglo ordenado se pueden obtener fácilmente datos como el mínimo, el máximo y la mediana.

---

**3. ¿En qué situaciones la búsqueda lineal sigue siendo una opción adecuada?**

La búsqueda lineal sigue siendo buena opción cuando:

* Los datos no están ordenados
* El tamaño del conjunto de datos es pequeño
* Se necesita recorrer toda la matriz para contar ocurrencias o encontrar posiciones específicas

