from google.colab import files

uploaded = files.upload()

def ReadDataFile(FileName):
    V = set()
    Edges = list()
    edge= dict()
    try:
        with open(FileName, 'r') as file:
            for line in file:
                i, j, c = map(float, line.strip().split())
                edge = {'i': int(i-1), 'j': int(j-1), 'c': c}
                Edges.append(edge)
                V.add(int(i-1))
                V.add(int(j-1))
        return V, Edges
    except FileNotFoundError:
        print(f'El archivo {File} no existe')
        quit()

def argmin(Edges, FeasibleSet):
    kstar = -1
    mincost = float('inf')
    for k in FeasibleSet:
        if Edges[k]['c'] < mincost:
            mincost = Edges[k]['c']
            kstar = k
    return kstar

def UpdateFeasibleSet(V, Edges, FeasibleSet, label):
    edgestar = argmin(Edges, FeasibleSet)
    l = label[Edges[edgestar]['j']]

    for j in V:
        if label[j] == l:
            label[j] = label[Edges[edgestar]['i']]

    S = set(FeasibleSet)
    for k in S:
        if label[Edges[k]['i']] == label[Edges[k]['j']]:
            FeasibleSet.remove(k)
    print(FeasibleSet)
    print(S)

def Run():
    FileName = input("Archivo de datos: ")
    V, Edges = ReadDataFile(FileName)
    S = list()
    label=[j for j in V]
    f = 0.
    TreeEdges = 0
    iter = 0
    FeasibleSet = set(range(len(Edges)))

    while FeasibleSet:
        iter += 1
        edgestar = argmin(Edges, FeasibleSet)
        print(f"En la iteración {iter}, se selecciona la arista {{ {Edges[edgestar]['i']+1}, {Edges[edgestar]['j']+1} }} con costo {Edges[edgestar]['c']}")
        TreeEdges += 1
        S.append(Edges[edgestar])
        f += Edges[edgestar]['c']
        UpdateFeasibleSet(V, Edges, FeasibleSet, label)
    print("El costo total es:", f)

Run()