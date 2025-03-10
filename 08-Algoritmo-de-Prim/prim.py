import random

grafo = {}

with open(r'C:\Heri\GitHub\.Semester\Advanced-Optimization\08-Algoritmo-de-Prim\MST01.txt', 'r') as file:
    for line in file:
        u, v, w = map(int, line.split())
        if u not in grafo:
            grafo[u] = []
        if v not in grafo:
            grafo[v] = []
        grafo[u].append((v, w))
        grafo[v].append((u, w))

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
        if peso_minimo <= 1:
            break

    aristas.remove((peso_minimo, u, v)) 

    if v not in visitados:
        visitados.append(v) 
        mst.append((u, v, peso_minimo)) 

        for vecino, p in grafo[v]:
            aristas.append((p, v, vecino))  

peso_total = 0

print("Árbol de Expansión Mínimo:\n")
for nodo_u, nodo_v, peso in mst:
    print(f"{nodo_u} - {nodo_v}")
    peso_total += sum({peso})

print(f"\nPeso Total: {peso_total}")