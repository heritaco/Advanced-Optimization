# **Problem: Warehouse Distribution**.

A company operates **2 warehouses** (W1 and W2) and supplies **3 retail stores** (S1, S2, and S3). The supply capacity of each warehouse and the demand of each store are as follows:


| Warehouse | Supply Capacity |
|-----------|-----------------|
| W1        | 40             |
| W2        | 50             |

| Store | Demand |
|-------|--------|
| S1    | 30     |
| S2    | 20     |
| S3    | 40     |

The transportation costs (\$ per unit) between warehouses and stores are:

|           | S1 | S2 | S3 |
|-----------|----|----|----|
| **W1**    | 8  | 6  | 10 |
| **W2**    | 9  | 12 | 7  |

---

### Math
Mathematical solution

#### Objective:
Minimize the total transportation cost.

#### Decision Variables:
Let:
- $x_{ij}$ = number of units transported from warehouse $i$ to store $j$.

#### Constraints:

1. Supply constraints:
   - $x_{11} + x_{12} + x_{13} \leq 40$ (W1 supply capacity)
   - $x_{21} + x_{22} + x_{23} \leq 50$ (W2 supply capacity)

2. Demand constraints:
   - $x_{11} + x_{21} \geq 30$ (S1 demand)
   - $x_{12} + x_{22} \geq 20$ (S2 demand)
   - $x_{13} + x_{23} \geq 40$ (S3 demand)

3. Non-negativity:
   - $x_{ij} \geq 0$ for all $i, j$.

---

### Solution

```bash
Solving the problem...
Optimal solution:
x(1,1) = 20
x(1,2) = 20
x(1,3) = 0
x(2,1) = 10
x(2,2) = 0
x(2,3) = 40
Minimum Transportation Cost: 650
```

---

The solution provided by the Mosel model is:

| **Warehouse → Store** | **Units Shipped ($x_{ij}$)** |
|-----------------------|--------------------------------|
| W1 → S1 ($x_{11}$) | 20                            |
| W1 → S2 ($x_{12}$) | 20                            |
| W1 → S3 ($x_{13}$) | 0                             |
| W2 → S1 ($x_{21}$) | 10                            |
| W2 → S2 ($x_{22}$) | 0                             |
| W2 → S3 ($x_{23}$) | 40                            |

---

### Step-by-Step Explanation

#### 1. Transportation Decisions
The model determines the optimal number of units shipped ($x_{ij}$) from each warehouse $i$ to each store $j$. The assignments are:

- From W1:
  - 20 units to S1.
  - 20 units to S2.
  - 0 units to S3 (none shipped).
  
- From W2:
  - 10 units to S1.
  - 0 units to S2 (none shipped).
  - 40 units to S3.

#### 2. Checking Constraints

**Warehouse Supply Constraints**:
- W1 total supply: $x_{11} + x_{12} + x_{13} = 20 + 20 + 0 = 40$ (meets W1's supply limit).
- W2 total supply: $x_{21} + x_{22} + x_{23} = 10 + 0 + 40 = 50$ (meets W2's supply limit).

**Store Demand Constraints**:
- S1 demand: $x_{11} + x_{21} = 20 + 10 = 30$ (meets S1's demand).
- S2 demand: $x_{12} + x_{22} = 20 + 0 = 20$ (meets S2's demand).
- S3 demand: $x_{13} + x_{23} = 0 + 40 = 40$ (meets S3's demand).

All constraints are satisfied.

---

#### 3. Objective Function: Minimum Cost
The transportation cost is calculated as:
$$
\text{Cost} = 20x_{11} + 20x_{12} + 0x_{13} + 10x_{21} + 40x_{22} + 0_{23}
$$
Substituting the solution values:
$$
\text{Cost} = 8(20) + 6(20) + 10(0) + 9(10) + 12(0) + 7(40)
$$
$$
\text{Cost} = 160 + 120 + 0 + 90 + 0 + 280 = 650
$$

Thus, the **minimum transportation cost is \$650**.

---

### Interpretation of Results
1. The model minimizes the cost by prioritizing shipments from warehouses with lower transportation costs to stores.
   - For example, S3’s demand is entirely fulfilled by W2 ($x_{23} = 40$) because W2 → S3 costs only \$7/unit.
   - S1 and S2's demands are mostly met by W1, which has lower costs to those stores.

2. The supply capacities of both warehouses are fully utilized:
   - W1 sends 40 units (its maximum capacity).
   - W2 sends 50 units (its maximum capacity).
