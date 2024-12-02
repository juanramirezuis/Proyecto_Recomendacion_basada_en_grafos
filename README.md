# Proyecto Final de Matemáticas Discretas: Sistema de Recomendación de Videojuegos para PC

## Grupo F3
### Integrantes
- **Juan Manuel Ramírez Salamanca**  
  - Matrícula: 2192279  
  - Email: juanramirezuis@gmail.com  
  - Rol: Líder, escritor del código y del notebook.

- **Diego Andrés Duque Meza**  
  - Matrícula: 2221102  
  - Email: sofysanchez03@gmail.com  
  - Rol: Diseño del póster y análisis del problema.

- **Karen Sofía Sánchez Castañeda**  
  - Matrícula: 2211855  
  - Email: londonofabian95@gmail.com  
  - Rol: Material de apoyo y documentación del código.

---

## Introducción

En este proyecto se propone un **Sistema de Recomendación de Videojuegos para PC**, utilizando herramientas de la **teoría de grafos** para generar recomendaciones basadas en las preferencias de los usuarios. El sistema analiza videojuegos basándose en características clave como género, desarrolladora, año de publicación y otros aspectos relevantes.

### Contexto del Problema
Los videojuegos han pasado de ser simples pasatiempos a una industria cultural de gran relevancia. Con una oferta tan variada, las plataformas enfrentan el desafío de ofrecer recomendaciones personalizadas que cumplan con las expectativas de los usuarios. Este proyecto busca abordar este reto mediante un modelo matemático práctico y escalable.

### Objetivos
#### General
Desarrollar un sistema que recomiende videojuegos similares a uno seleccionado previamente, basándose en características clave.

#### Específicos
1. Aplicar la teoría de grafos para modelar la relación entre videojuegos.
2. Analizar similitudes basadas en atributos como género, empresa desarrolladora y otros.
3. Generar un sistema de recomendaciones eficiente y fácil de implementar.

---

## Planteamiento del Problema Matemático

El problema se modela como un **grafo no dirigido** \( G=(V, E) \), donde:
- \( V \): Nodos representando videojuegos.
- \( E \): Aristas que conectan videojuegos similares.
- Peso de las aristas (\( w \)): Grado de similitud entre dos videojuegos, basado en atributos compartidos.

El objetivo es encontrar los \( k \)-nodos más similares a un nodo dado \( v \), ordenados por el peso de sus aristas.

### Representación del Grafo
- Nodos (\( V \)): Videojuegos.
- Aristas (\( E \)): Relación de similitud.
- Peso (\( w \)): Calculado como:  
  \[
  w(u,v) = \sum_{i=1}^n \delta(a_i(u), a_i(v))
  \]  
  Donde \( \delta(x, y) \) retorna 1 si \( x=y \) y 0 en caso contrario.

### Construcción del Grafo
1. Iterar sobre todos los pares de videojuegos.
2. Calcular el peso \( w(u,v) \) entre nodos \( u \) y \( v \).
3. Si \( w(u,v) > 0 \), añadir una arista con peso \( w \).

---

## Implementación

### Herramientas Utilizadas
- **Python**: Lenguaje de programación.
- **Librerías**:
  - `pandas`: Para el manejo de datos.
  - `networkx`: Para crear y analizar grafos.
  - `matplotlib`: Para visualizar grafos.

### Flujo de Trabajo
1. **Base de Datos**:  
   Una lista de 100 videojuegos mejor calificados, extraídos de la plataforma *3D Juegos*. Los datos se almacenan en un archivo Excel que se procesa para crear los nodos del grafo.
   
2. **Clase Juego**:  
   Modela cada videojuego como un nodo con atributos como género, empresa desarrolladora, año de publicación, etc.

3. **Construcción del Grafo**:  
   Se comparan las características de cada par de videojuegos para calcular el peso de las aristas.

4. **Recomendaciones**:  
   Basadas en los vecinos más cercanos del nodo correspondiente al videojuego seleccionado.

---

## Código
El repositorio contiene los scripts necesarios para:
- Crear el grafo.
- Generar visualizaciones del grafo.
- Implementar el sistema de recomendación.

### Ejemplo de Uso
1. Ejecuta el script en un entorno como Google Colab.
2. Carga el archivo Excel con los datos de videojuegos.
3. Selecciona un videojuego del menú interactivo.
4. Recibe una lista de recomendaciones basadas en similitudes.

---

## Alternativas de Solución
1. **Optimización del Algoritmo**: Uso de aprendizaje automático para mejorar las recomendaciones.
2. **Ampliación de la Base de Datos**: Incorporar más videojuegos y plataformas.
3. **Pesos Dinámicos**: Adaptar los pesos en tiempo real según las preferencias del usuario.
4. **Análisis Temporal**: Incorporar tendencias de popularidad.
5. **Integración con APIs**: Conectar con plataformas como Steam para recomendaciones en tiempo real.

---

## Visualización del Grafo
El grafo muestra los videojuegos como nodos y sus similitudes como aristas ponderadas. Se pueden identificar clusters que representan grupos de videojuegos con características similares.

```python
pos = nx.spring_layout(g_Juegos)
labels = {juego: juego.Nombre for juego in l_Juegos}
nx.draw(g_Juegos, pos, with_labels=False, node_size=50)
nx.draw_networkx_labels(g_Juegos, pos, labels, font_size=8)
plt.title('Grafo de Juegos')
plt.show()
