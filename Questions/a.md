


  </div class="bubble left">
  <div class="bubble right">
en las restricciones de programacion lineal 

cual es la diferencia entre poner 
suma _i^n suma_j^m x_ij

y

suma_j^m x_ij i e N


  </div class="bubble right">
  <div class="bubble left">


La diferencia principal entre las dos expresiones radica en la forma en que se suman las variables de decisión y en la notación de los índices:

1. **$\sum_{i=1}^{n} \sum_{j=1}^{m} x_{ij}$**  
   - Aquí se está sumando sobre todos los valores de $i$ y $j$, lo que significa que se está considerando **todas las combinaciones posibles** de los índices $i$ y $j$.
   - Esto da como resultado una **suma doble**, que generalmente representa el total de todas las variables $x_{ij}$.
   - Se usa cuando se necesita una restricción global que involucra todas las variables de la matriz $x_{ij}$.

2. **$\sum_{j=1}^{m} x_{ij}, \quad i \in N$**  
   - Aquí la sumatoria solo se realiza sobre el índice $j$, mientras que $i$ es **un valor fijo** que pertenece al conjunto $N$.
   - En otras palabras, para cada $i$, se suman todas las $x_{ij}$ sobre $j$, lo que genera una ecuación o restricción **para cada valor de $i$**.
   - Se usa cuando se necesita una restricción que se cumpla para cada $i$ por separado.



  </div class="bubble left">
  <div class="bubble left">

 **Ejemplo en un problema de asignación**
Supongamos que tenemos un problema donde $x_{ij}$ indica si la persona $i$ es asignada a la tarea $j$ (1 si se asigna, 0 si no).

- **$\sum_{i=1}^{n} \sum_{j=1}^{m} x_{ij} \leq k$**  
  - Esta restricción indica que el número total de asignaciones (sumando todas las personas y tareas) no puede superar $k$.

- **$\sum_{j=1}^{m} x_{ij} = 1, \quad \forall i \in N$**  
  - Esta restricción indica que cada persona $i$ solo puede ser asignada a una única tarea, asegurando que la suma sobre $j$ para cada $i$ sea exactamente 1.

Ambas expresiones tienen usos distintos en la modelación de restricciones dentro de la programación lineal.


  </div class="bubble left">
  <div class="bubble right">
me puedes dar un ejemplo de como se ve desarrollado? 


  </div class="bubble right">
  <div class="bubble left">

Claro, aquí tienes un ejemplo más completo usando la notación que mencionas en el contexto de un problema de asignación. Supongamos que estamos resolviendo un problema de asignación de trabajadores a tareas, con $n$ trabajadores y $m$ tareas. La variable de decisión $x_{ij}$ es igual a 1 si el trabajador $i$ es asignado a la tarea $j$, y 0 en caso contrario.



  </div class="bubble left">
  <div class="bubble left">

 Definición del problema
Queremos asignar a cada trabajador exactamente una tarea, y cada tarea puede ser asignada a un solo trabajador. Además, tenemos que asegurar que la cantidad total de asignaciones no exceda de un cierto límite $k$.



  </div class="bubble left">
  <div class="bubble left">

 Restricciones y su desarrollo

1. **Restricción 1: Cada trabajador debe ser asignado exactamente a una tarea**

Para esta restricción, usamos la notación:

$$
\sum_{j=1}^{m} x_{ij} = 1, \quad \forall i \in N
$$

Esto significa que para cada trabajador $i$ (es decir, para cada valor de $i \in N$, donde $N$ es el conjunto de trabajadores), la suma de las asignaciones $x_{ij}$ sobre todas las tareas $j$ debe ser igual a 1. Es decir, cada trabajador debe ser asignado a una única tarea.



  </div class="bubble left">
  <div class="bubble left">

 Desarrollo:
Para $i = 1, 2, \dots, n$:

- Para el trabajador 1:

$$
x_{11} + x_{12} + \dots + x_{1m} = 1
$$

- Para el trabajador 2:

$$
x_{21} + x_{22} + \dots + x_{2m} = 1
$$

- Y así sucesivamente para todos los trabajadores hasta $i = n$.

Esta restricción asegura que cada trabajador está asignado a una tarea.

2. **Restricción 2: El número total de asignaciones no puede exceder de $k$**

Para esta restricción, usamos la notación:

$$
\sum_{i=1}^{n} \sum_{j=1}^{m} x_{ij} \leq k
$$

Esta restricción asegura que el número total de asignaciones de trabajadores a tareas no puede exceder el valor $k$. Es decir, no podemos asignar más de $k$ tareas en total, sin importar cómo se distribuyan entre los trabajadores.



  </div class="bubble left">
  <div class="bubble left">

 Desarrollo:
La sumatoria doble recorre todas las combinaciones de trabajadores $i$ y tareas $j$:

$$
x_{11} + x_{12} + \dots + x_{1m} + x_{21} + x_{22} + \dots + x_{2m} + \dots + x_{n1} + x_{n2} + \dots + x_{nm} \leq k
$$

Esto representa la cantidad total de asignaciones de tareas a trabajadores. Debe ser menor o igual a $k$.



  </div class="bubble left">
  <div class="bubble left">

 Visualización de un ejemplo con $n = 3$ trabajadores y $m = 3$ tareas

Supongamos que tenemos 3 trabajadores y 3 tareas, y queremos asegurarnos de que:

- Cada trabajador esté asignado exactamente a una tarea.
- El número total de asignaciones no exceda de 5.



  </div class="bubble left">
  <div class="bubble left">

 Restricción 1: Asignar exactamente una tarea por trabajador

$$
x_{11} + x_{12} + x_{13} = 1 \quad (\text{trabajador 1})
$$
$$
x_{21} + x_{22} + x_{23} = 1 \quad (\text{trabajador 2})
$$
$$
x_{31} + x_{32} + x_{33} = 1 \quad (\text{trabajador 3})
$$



  </div class="bubble left">
  <div class="bubble left">

 Restricción 2: El número total de asignaciones no puede exceder 5

$$
x_{11} + x_{12} + x_{13} + x_{21} + x_{22} + x_{23} + x_{31} + x_{32} + x_{33} \leq 5
$$

Este conjunto de restricciones asegura que:

- Cada trabajador se asigna exactamente a una tarea.
- El total de asignaciones no excede el número máximo de asignaciones posibles.

Este es un ejemplo simple, pero ilustra cómo las sumas de índices y las restricciones sobre variables de decisión se desarrollan en un problema de programación lineal.