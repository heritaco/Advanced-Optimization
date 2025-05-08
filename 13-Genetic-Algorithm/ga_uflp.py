import numpy as np
from numba import njit
import random
import time

@njit
def calcular_fitness_numba(indices_instalaciones_abiertas, costos_fijos, costos_transporte):
    if indices_instalaciones_abiertas.size == 0:
        return np.int64(1e9)  # Penalización alta pero como entero

    costo_fijo = 0
    for indice in indices_instalaciones_abiertas:
        costo_fijo += int(costos_fijos[indice])  # Asegurar entero

    costo_transporte = 0
    for cliente in range(costos_transporte.shape[0]):
        costo_minimo = 1e9  # Entero
        for indice_instalacion in indices_instalaciones_abiertas:
            costo = int(costos_transporte[cliente, indice_instalacion])
            if costo < costo_minimo:
                costo_minimo = costo
        costo_transporte += costo_minimo

    return costo_fijo + costo_transporte

class UFLP_GA:
    def __init__(self, n_instalaciones, n_clientes, costos_fijos, costos_transporte,
                 tamaño_poblacion=50, tasa_mutacion=0.1, tasa_crossover=0.8,
                 tamaño_torneo=3, max_generaciones=100, tipo_crossover='uniforme', tipo_mutacion='random',
                 random_seed=None, fitness_objetivo=None):
        self.n_instalaciones = n_instalaciones
        self.n_clientes = n_clientes
        self.costos_fijos = np.array(costos_fijos[1:])  # Ignorar el indice 0 porque los indices en Python empiezan desde 0.
        self.costos_transporte = np.array(costos_transporte[1:])[:, 1:]  # Ignorar el indice 0 para clientes e instalaciones.
        self.tamaño_poblacion = tamaño_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.tasa_crossover = tasa_crossover
        self.tamaño_torneo = tamaño_torneo
        self.max_generaciones = max_generaciones
        self.tipo_crossover = tipo_crossover
        self.tipo_mutacion = tipo_mutacion
        self.poblacion = []
        self.generacion = 0
        self.mejor_solucion = None  # Almacenara los indices de las instalaciones abiertas
        self.mejor_fitness = np.int64(1e9)  # Inicializar con un valor muy grande para asegurar que se encuentre un mejor valor.
        self.historial_fitness = []
        self.random_seed = random_seed
        self.fitness_objetivo = fitness_objetivo  # Almacena el objetivo de fitness si se proporciona.

        if self.random_seed is not None:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)  

    def _generar_individuo(self):
        num_abiertas = np.random.randint(1, self.n_instalaciones)  # Elige un número aleatorio de instalaciones para abrir.
        indices_abiertos = np.sort(np.random.choice(self.n_instalaciones, size=num_abiertas, replace=False))  # Selecciona aleatoriamente instalaciones únicas.
        return {'solucion': indices_abiertos, 'fitness': None}  # Devuelve el individuo con la solucion y fitness sin calcular.

    def _inicializar_poblacion(self):
        self.poblacion = [self._generar_individuo() for _ in range(self.tamaño_poblacion)]  # Crea una lista de individuos aleatorios.
        self._evaluar_poblacion()  # Calcula la fitness de cada individuo en la poblacion.
        self.poblacion.sort(key=lambda ind: ind['fitness'])  # Ordena la poblacion según la fitness (de menor a mayor).
        self.mejor_solucion = self.poblacion[0]['solucion'].copy()  # Almacena la mejor solucion encontrada hasta ahora.
        self.mejor_fitness = self.poblacion[0]['fitness']  # Almacena la mejor fitness encontrada hasta ahora.
        self.historial_fitness.append(self.mejor_fitness)  # Guarda la mejor fitness en el historial.

    def _calcular_fitness(self, individuo):
        return calcular_fitness_numba(
            individuo['solucion'],
            self.costos_fijos,
            self.costos_transporte
        )

    def _evaluar_poblacion(self):
        for individuo in self.poblacion:
            individuo['fitness'] = self._calcular_fitness(individuo)  # Calcula la fitness del individuo.
            if individuo['fitness'] < self.mejor_fitness:  # Si la fitness es mejor que la mejor encontrada hasta ahora:
                self.mejor_fitness = individuo['fitness']  # Actualiza la mejor fitness.
                self.mejor_solucion = individuo['solucion'].copy()  # Actualiza la mejor solucion.

    def _seleccion_torneo(self):
        torneo = random.sample(self.poblacion, self.tamaño_torneo)  # Selecciona un subconjunto aleatorio de la poblacion.
        ganador = min(torneo, key=lambda ind: ind['fitness'])  # Encuentra al individuo con la mejor fitness en el torneo.
        return ganador  # Devuelve al ganador del torneo.

    def _crossover_uniforme(self, padre1, padre2):
        conjunto1 = set(padre1['solucion'])
        conjunto2 = set(padre2['solucion'])
        union_conjunto = conjunto1.union(conjunto2)  # Obtiene el conjunto de todas las instalaciones abiertas por ambos padres.
        # interseccion_conjunto = conjunto1.intersection(conjunto2) # Obtiene el conjunto de instalaciones abiertas por ambos padres

        descendiente1_indices = []
        descendiente2_indices = []

        # Itera sobre todas las instalaciones únicas abiertas por los padres.
        for indice_instalacion in union_conjunto:
            if np.random.random() < 0.5:  # Decide aleatoriamente de qué padre hereda la instalacion.
                descendiente1_indices.append(indice_instalacion)  # Agrega la instalacion al primer descendiente.
            else:
                descendiente2_indices.append(indice_instalacion)  # Agrega la instalacion al segundo descendiente.

        # Asegurar que al menos una instalacion esté abierta
        if not descendiente1_indices:
            descendiente1_indices.append(np.random.choice(list(union_conjunto)))
        if not descendiente2_indices:
            descendiente2_indices.append(np.random.choice(list(union_conjunto)))

        # Devuelve los descendientes con las instalaciones abiertas y fitness sin calcular.
        return {'solucion': np.sort(np.array(list(descendiente1_indices))), 'fitness': None}, \
               {'solucion': np.sort(np.array(list(descendiente2_indices))), 'fitness': None}

    def _crossover_un_punto(self, padre1, padre2):
        solucion1 = padre1['solucion']
        solucion2 = padre2['solucion']
        longitud1 = len(solucion1)
        longitud2 = len(solucion2)

        if longitud1 < 2 or longitud2 < 2:
            return self._crossover_uniforme(padre1, padre2)  # Volver a uniforme si es demasiado corto

        punto_crossover1 = np.random.randint(1, longitud1 - 1)
        punto_crossover2 = np.random.randint(1, longitud2 - 1)

        descendiente1_indices = np.sort(np.concatenate((solucion1[:punto_crossover1], solucion2[punto_crossover2:])))
        descendiente2_indices = np.sort(np.concatenate((solucion2[:punto_crossover2], solucion1[punto_crossover1:])))

        # Asegurar que al menos una instalacion esté abierta
        if not descendiente1_indices.size:
            descendiente1_indices = np.array([np.random.choice(np.concatenate((solucion1, solucion2)))])
        if not descendiente2_indices.size:
            descendiente2_indices = np.array([np.random.choice(np.concatenate((solucion1, solucion2)))])

        return {'solucion': descendiente1_indices, 'fitness': None}, {'solucion': descendiente2_indices, 'fitness': None}

    def _operador_crossover(self, padre1, padre2):
        if self.tipo_crossover == 'uniforme':
            return self._crossover_uniforme(padre1, padre2)
        elif self.tipo_crossover == 'un_punto':
            return self._crossover_un_punto(padre1, padre2)

    def _mutar_random(self, individuo):
        indices_mutados = list(individuo['solucion'])
        num_abiertas = len(indices_mutados)

        if random.random() < self.tasa_mutacion:
            if num_abiertas > 1 and random.random() < 0.33:  # Eliminar una instalacion
                indice_eliminar = random.randint(0, num_abiertas - 1)
                indices_mutados.pop(indice_eliminar)
            elif num_abiertas < self.n_instalaciones and random.random() < 0.66:  # Agregar una instalacion
                indices_cerradas = np.array([i for i in range(self.n_instalaciones) if i not in indices_mutados])
                if indices_cerradas.size > 0:
                    indice_agregar = random.choice(indices_cerradas)
                    indices_mutados.append(indice_agregar)
            elif num_abiertas > 0 and self.n_instalaciones > num_abiertas: # Intercambiar una instalacion
                indice_eliminar = random.randint(0, num_abiertas - 1)
                indices_cerradas = np.array([i for i in range(self.n_instalaciones) if i not in indices_mutados])
                if indices_cerradas.size > 0:
                    indice_agregar = random.choice(indices_cerradas)
                    indices_mutados[indice_eliminar] = indice_agregar

        return {'solucion': np.sort(np.array(indices_mutados)), 'fitness': None}
    
    def _mutar_mejor(self, individuo):
        original_solucion = individuo['solucion']
        original_fitness = self._calcular_fitness(individuo)
        max_intentos = 10  # Número máximo de intentos de mutación

        for _ in range(max_intentos):
            indices_mutados = list(original_solucion.copy())
            num_abiertas = len(indices_mutados)

            if num_abiertas > 1 and random.random() < 0.33:  # Eliminar una instalación
                indice_eliminar = random.randint(0, num_abiertas - 1)
                indices_mutados.pop(indice_eliminar)
            elif num_abiertas < self.n_instalaciones and random.random() < 0.66:  # Agregar una instalación
                indices_cerradas = np.array([i for i in range(self.n_instalaciones) if i not in indices_mutados])
                if indices_cerradas.size > 0:
                    indice_agregar = random.choice(indices_cerradas)
                    indices_mutados.append(indice_agregar)
            elif num_abiertas > 0 and self.n_instalaciones > num_abiertas:  # Intercambiar una instalación
                indice_eliminar = random.randint(0, num_abiertas - 1)
                indices_cerradas = np.array([i for i in range(self.n_instalaciones) if i not in indices_mutados])
                if indices_cerradas.size > 0:
                    indice_agregar = random.choice(indices_cerradas)
                    indices_mutados[indice_eliminar] = indice_agregar

            indices_mutados = np.sort(np.array(indices_mutados))
            fitness_mutado = self._calcular_fitness({'solucion': indices_mutados, 'fitness': None})

            if fitness_mutado < original_fitness:
                return {'solucion': indices_mutados, 'fitness': fitness_mutado}

        # Si ningún intento mejora, devuelve el original con fitness actualizado
        return {'solucion': original_solucion.copy(), 'fitness': original_fitness}
    
    def _mutar(self, individuo):
        if self.tipo_mutacion == 'random':
            return self._mutar_random(individuo)
        elif self.tipo_mutacion == 'mejor':
            return self._mutar_mejor(individuo)


    def _reemplazo(self, nueva_poblacion):
        for individuo in nueva_poblacion:
            if individuo['fitness'] is None:
                individuo['fitness'] = self._calcular_fitness(individuo)
        nueva_poblacion.append({'solucion': self.mejor_solucion.copy(), 'fitness': self.mejor_fitness})
        nueva_poblacion.sort(key=lambda ind: ind['fitness'])
        self.poblacion = nueva_poblacion[:self.tamaño_poblacion]

    def run(self):
        tiempo_inicio = time.time()
        self._inicializar_poblacion()

        for generacion in range(self.max_generaciones):
            self.generacion = generacion
            nueva_poblacion = []
            while len(nueva_poblacion) < self.tamaño_poblacion - 1:
                padre1 = self._seleccion_torneo()
                padre2 = self._seleccion_torneo()
                if random.random() < self.tasa_crossover:
                    descendiente1, descendiente2 = self._operador_crossover(padre1, padre2)
                    nueva_poblacion.append(self._mutar(descendiente1))
                    nueva_poblacion.append(self._mutar(descendiente2))
                else:
                    nueva_poblacion.append(self._mutar({'solucion': padre1['solucion'].copy(), 'fitness': None}))
                    nueva_poblacion.append(self._mutar({'solucion': padre2['solucion'].copy(), 'fitness': None}))

            self._reemplazo(nueva_poblacion)
            self._evaluar_poblacion()
            self.historial_fitness.append(self.mejor_fitness)

            generacion_opti = None
            if self.fitness_objetivo is not None and self.mejor_fitness <= self.fitness_objetivo:
                generacion_opti = generacion + 1
                break
            
        tiempo_fin = time.time()
        return self.mejor_solucion, self.mejor_fitness, self.historial_fitness, tiempo_fin - tiempo_inicio, self.generacion + 1, generacion_opti
