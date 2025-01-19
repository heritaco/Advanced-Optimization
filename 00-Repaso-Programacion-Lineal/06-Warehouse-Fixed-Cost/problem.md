Adding **fixed costs per warehouse** introduces a new dimension to the problem, making it a **mixed-integer programming** (MIP) problem. Fixed costs mean that if a warehouse is used (ships any units), there is an additional cost incurred regardless of the number of units shipped. This requires **binary variables** to decide whether each warehouse is active or not.

---

### Updated Problem: Fixed Costs for Warehouses


#### Fixed Costs:
- W1: \$100
- W2: \$120

#### Additional Decision Variables:
Introduce **binary variables** $y_i$ for each warehouse $i$:
- $y_1$: 1 if W1 is active, 0 otherwise.
- $y_2$: 1 if W2 is active, 0 otherwise.

#### Updated Objective Function:
Minimize total cost:
$$
\text{Total Cost} = \sum_{i=1}^{2}\sum_{j=1}^{3} c_{ij}x_{ij} + 100y_1 + 120y_2
$$
Where:
- $c_{ij}$: transportation cost per unit from warehouse $i$ to store $j$,
- $x_{ij}$: number of units shipped from $i$ to $j$,
- $y_i$: fixed cost decision for warehouse $i$.

#### Additional Constraints:
To ensure fixed costs are only incurred when a warehouse is used, add the following constraints:
$$
\sum_{j=1}^{3} x_{ij} \leq M y_i \quad \forall i
$$
Where:
- $M$: a large constant representing the maximum possible supply from a warehouse (e.g., the warehouse's supply capacity).

This ensures that if $y_i = 0$, no units can be shipped from warehouse $i$.


---

### Key Changes
1. **Binary Variables**:
   - $y(1)$ and $y(2)$ represent whether W1 and W2 are active, respectively.
2. **Fixed Costs in the Objective Function**:
   - Added $100y(1)$ and $120y(2)$ to account for the fixed costs of activating each warehouse.
3. **Capacity Constraints Linked to Activation**:
   - If $y(i) = 0$, then $x(i,j) = 0$ for all $j$.
4. **Large Constant $M$**:
   - Represents the maximum supply from each warehouse, ensuring $x(i,j) \leq M \cdot y(i)$.

---

### Example Output
When you run this model, the output might look like:

```
Solving the problem with fixed costs...
Optimal solution:
x(1,1) = 20
x(1,2) = 20
x(1,3) = 0
x(2,1) = 10
x(2,2) = 0
x(2,3) = 40
y(1) = 1
y(2) = 1
Minimum Total Cost: 870
```

---

### Interpretation of Results
1. Both warehouses are active ($y(1) = 1, y(2) = 1$), so fixed costs are incurred for both.
2. The optimal shipment plan minimizes the combined transportation and fixed costs.
3. The **minimum total cost** includes:
   - Transportation cost: \$650.
   - Fixed costs: \$100 (W1) + \$120 (W2) = \$220.
   - **Total cost** = \$870.

---

