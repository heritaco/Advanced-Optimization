import random

def ReadDataFile():

    V = set()
    visitados = set()
    grafo = dict()
    mst = list()

    FileName = r'C:\Heri\GitHub\.Semester\Advanced-Optimization\08-Algoritmo-de-Prim\MST01.txt'

    try:
        with open(FileName, 'r') as file:
            for line in file:

                i, j, c = map(float, line.strip().split())
                
                i = int(i-1)
                j = int(j-1)
                
                V.add(int(i))
                V.add(int(j))
                
                if i not in grafo:
                    grafo[i] = []
                grafo[i].append((j, c))
                
                if j not in grafo:
                    grafo[j] = []
                grafo[j].append((i, c))

    except FileNotFoundError:
        print(f'El archivo {FileName} no existe')
        quit()

    return V, visitados, grafo, mst



def EscogerNodoInicial(V): 

    valor_random = random.randint(0, len(V)-1)   
    nodo_inicial = list(V)[valor_random]

    return nodo_inicial


    
def Prim(V, visitados, grafo, mst, nodo_inicial):

    visitados.add(nodo_inicial)

    while len(visitados) < len(V):

        peso_minimo = float('inf')
        u = None
        v = None

        for nodo in visitados:
            for vecino, peso in grafo[nodo]:
                if vecino not in visitados:
                    if peso < peso_minimo:
                        u, v, peso_minimo = nodo, vecino, peso  
                if peso_minimo <= 1:
                    break

        visitados.add(v)
        mst.append((u, v, peso_minimo))

    return mst



def calcularPesoTotal(mst):

    peso_total = 0
    # es un _ porque no lo vamos a usar
    for _, _, peso in mst:
        peso_total += peso

    return peso_total



def imprimirMST(mst):

    print("Árbol de Expansión Mínimo:\n")
    for u, v, _ in mst:
        print(f"{int(u+1)} - {int(v+1)}")

    peso_total = calcularPesoTotal(mst)

    print(f"\nPeso Total: {peso_total}")


def Run():

    V, visitados, grafo, mst = ReadDataFile()
    nodo_inicial = EscogerNodoInicial(V)
    mst = Prim(V, visitados, grafo, mst, nodo_inicial)
    imprimirMST(mst)

Run()