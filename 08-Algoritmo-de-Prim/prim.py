import random

grafo = {
    1: [(3, 5),  (4, 7),  (6, 5) ],
    2: [(5, 4),  (11, 4), (7, 2), (10, 6), (12, 10)],
    3: [(1, 5),  (11, 1), (5, 1)],
    4: [(1, 7),  (11, 1), (7, 3)],
    5: [(3, 1),  (11, 2), (2, 4), (12, 15)],
    6: [(1, 5),  (9, 10)],
    7: [(4, 3),  (2, 2),  (10, 8),(9, 4)],
    8: [(9, 7),  (10, 9)],
    9: [(6, 10), (7, 4),  (8, 7)],
    10:[(8, 9),  (7, 8),  (2, 6), (12,8)],
    11:[(5, 2),  (4, 1),  (2, 4)],
    12:[(5, 15), (10, 8)]
}

valor_random = random.randint(0, len(grafo) - 1)
nodo_inicial = list(grafo.keys())[valor_random]
print(f'El nodo inicial es {nodo_inicial}')
mst = []
visitados = []
aristas = []

visitados.append(nodo_inicial)

for vecino, peso in grafo[nodo_inicial]:    
    arista = (peso, nodo_inicial, vecino)   
    aristas.append(arista)

while len(visitados) < len(grafo):
    peso_minimo, u, v = aristas[0] 
    for arista in aristas:  
        if arista[0] < peso_minimo: 
            peso_minimo, u, v = arista  

    aristas.remove((peso_minimo, u, v)) 

    if v not in visitados:
        visitados.append(v) 
        mst.append((u, v, peso_minimo)) 

        for vecino, p in grafo[v]:
            if vecino not in visitados: 
                aristas.append((p, v, vecino))  

peso_total = 0

print("Árbol de Expansión Mínimo:\n")
for nodo_u, nodo_v, peso in mst:
    print(f"{nodo_u} - {nodo_v}")
    peso_total += sum({peso})

print(f"\nPeso Total: {peso_total}")