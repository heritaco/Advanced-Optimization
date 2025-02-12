# Machines production 

A factory produces two products: **A** and **B**. Each product requires resources from **two machines**, and the time requirements per unit are as follows:

| Machine | Time per unit of A (hours) | Time per unit of B (hours) | Total available hours |
|---------|-----------------------------|-----------------------------|-----------------------|
| Machine 1 | 3 | 2 | 18 |
| Machine 2 | 2 | 1 | 12 |

The profit for each unit of **A** is $5, and for **B** it is $3. The goal is to maximize the profit.

#### Variables:
- $x_1$: number of units of product **A** to produce.
- $x_2$: number of units of product **B** to produce.

#### Objective Function:
Maximize $Z = 5x_1 + 3x_2$

#### Constraints:
1. $3x_1 + 2x_2 \leq 18$ (Machine 1 constraint)
2. $2x_1 + x_2 \leq 12$ (Machine 2 constraint)
3. $x_1, x_2 \geq 0$ (Non-negativity constraints)

#### Solution

If you want to solve it in VS, you have to go to the location (in the terminal) and then call mosel from the PATH with  ```mosel .\name-of-the-file```

Go to the location:
   ```bash
   (base) PS C:\Heri\GitHub\.Semester\Advanced-Optimization> cd .\00-Repaso-Programacion-Lineal\

   (base) PS C:\Heri\GitHub\.Semester\Advanced-Optimization\00-Repaso-Programacion-Lineal> cd .\04-Machines\
   ```

Run the file:
   ```bash
   mosel .\problem.mos
   ```

Solution:
```bash
Solving the problem...
Optimal solution:
x1 (units of A): 6
x2 (units of B): 0
Maximum Profit: 30
```

- **$x_1 = 6$** (6 units of product A)
- **$x_2 = 0$** (0 units of product B)
- **Maximum Profit = 30**

### Explanation
Let’s reanalyze the problem step by step:

#### Objective Function:
Maximize $Z = 5x_1 + 3x_2$

#### Constraints:
1. $3x_1 + 2x_2 \leq 18$
2. $2x_1 + x_2 \leq 12$
3. $x_1, x_2 \geq 0$

#### Solving:
1. If we focus entirely on producing **A** ($x_2 = 0$):
   - $3x_1 \leq 18 \implies x_1 \leq 6$
   - $2x_1 \leq 12 \implies x_1 \leq 6$
   - So, $x_1 = 6$, $Z = 5(6) + 3(0) = 30$.

2. If we focus entirely on producing **B** ($x_1 = 0$):
   - $2x_2 \leq 18 \implies x_2 \leq 9$
   - $x_2 \leq 12$ (no further restriction)
   - So, $x_2 = 9$, $Z = 5(0) + 3(9) = 27$.

3. If we mix production ($x_1 > 0, x_2 > 0$):
   - Solving for the intersection of $3x_1 + 2x_2 = 18$ and $2x_1 + x_2 = 12$:
     - Multiply the second equation by 2: $4x_1 + 2x_2 = 24$.
     - Subtract the first equation: $4x_1 + 2x_2 - (3x_1 + 2x_2) = 24 - 18$.
     - $x_1 = 6$, $x_2 = 0$, $Z = 30$.

The optimal solution is to produce **6 units of A** and **0 units of B** for a maximum profit of **30**.
