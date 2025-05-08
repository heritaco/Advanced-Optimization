def cargar_datos(file_name):
    with open(file_name, 'r') as f:
        lineas = f.readlines()

    n, m = map(int, lineas[0].split())

    f_j = [0] * (n + 1)
    c_ij = [[0] * (n + 1) for _ in range(m + 1)]

    for j in range(1, n + 1):
        datos = list(map(int, lineas[j].split()))
        idx = datos[0]
        f_j[idx] = datos[1]
        for i in range(1, m + 1):
            c_ij[i][idx] = datos[i + 1]
    return n, m, f_j, c_ij