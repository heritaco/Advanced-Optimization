import numpy as np
from numba import njit
import random
import time

@njit
def calcular_fitness_numba(indices_instalaciones_abiertas, costos_fijos, costos_transporte):
    if indices_instalaciones_abiertas.size == 0:
        return np.int64(1e9)

    costo_fijo = 0
    for indice in indices_instalaciones_abiertas:
        costo_fijo += int(costos_fijos[indice])

    costo_transporte = 0
    for cliente in range(costos_transporte.shape[0]):
        costo_minimo = np.int64(1e9)
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
        self.costos_fijos = np.array(costos_fijos[1:]).astype(np.int64)
        self.costos_transporte = np.array(costos_transporte[1:])[:, 1:].astype(np.int64)
        self.tamaño_poblacion = tamaño_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.tasa_crossover = tasa_crossover
        self.tamaño_torneo = tamaño_torneo
        self.max_generaciones = max_generaciones
        self.tipo_crossover = tipo_crossover
        self.tipo_mutacion = tipo_mutacion
        self.poblacion = []
        self.generacion = 0
        self.mejor_solucion = None
        self.mejor_fitness = np.int64(1e9)
        self.historial_fitness = []
        self.random_seed = random_seed
        self.fitness_objetivo = fitness_objetivo

        if self.random_seed is not None:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)

    def _generar_individuo(self):
        num_abiertas = np.random.randint(1, self.n_instalaciones)
        indices_abiertos = np.sort(np.random.choice(self.n_instalaciones, size=num_abiertas, replace=False))
        return {'solucion': set(indices_abiertos), 'fitness': None}  # Usar un conjunto

    def _inicializar_poblacion(self):
        self.poblacion = [self._generar_individuo() for _ in range(self.tamaño_poblacion)]
        self._evaluar_poblacion()
        self.poblacion.sort(key=lambda ind: ind['fitness'])
        self.mejor_solucion = list(self.poblacion[0]['solucion'].copy())  # Convertir a lista para almacenamiento
        self.mejor_fitness = self.poblacion[0]['fitness']
        self.historial_fitness.append(self.mejor_fitness)

    def _calcular_fitness(self, individuo):
        # Convertir el conjunto a un array ordenado para numba
        indices_array = np.sort(np.array(list(individuo['solucion'])))
        return calcular_fitness_numba(
            indices_array,
            self.costos_fijos,
            self.costos_transporte
        )

    def _evaluar_poblacion(self):
        for individuo in self.poblacion:
            if individuo['fitness'] is None:  # Solo calcular si el fitness no está almacenado
                individuo['fitness'] = self._calcular_fitness(individuo)
        mejor_individuo = min(self.poblacion, key=lambda ind: ind['fitness']) #Calcula el mejor individuo de la población
        if mejor_individuo['fitness'] < self.mejor_fitness:
            self.mejor_fitness = mejor_individuo['fitness']
            self.mejor_solucion = list(mejor_individuo['solucion'].copy())

    def _seleccion_torneo(self):
        torneo = random.sample(self.poblacion, self.tamaño_torneo)
        ganador = min(torneo, key=lambda ind: ind['fitness'])
        return ganador

    def _crossover_uniforme(self, padre1, padre2):
        conjunto1 = set(padre1['solucion'])
        conjunto2 = set(padre2['solucion'])
        union_conjunto = conjunto1.union(conjunto2)

        descendiente1_indices = set()
        descendiente2_indices = set()

        for indice_instalacion in union_conjunto:
            if np.random.random() < 0.5:
                descendiente1_indices.add(indice_instalacion)
            else:
                descendiente2_indices.add(indice_instalacion)

        # Asegurar que al menos una instalacion esté abierta
        if not descendiente1_indices:
            descendiente1_indices.add(random.choice(list(union_conjunto)))
        if not descendiente2_indices:
            descendiente2_indices.add(random.choice(list(union_conjunto)))
        return {'solucion': descendiente1_indices, 'fitness': None}, \
               {'solucion': descendiente2_indices, 'fitness': None}

    def _crossover_un_punto(self, padre1, padre2):
        solucion1 = sorted(list(padre1['solucion']))  # Convertir a lista ordenada para el corte
        solucion2 = sorted(list(padre2['solucion']))
        longitud1 = len(solucion1)
        longitud2 = len(solucion2)

        if longitud1 < 2 or longitud2 < 2:
            return self._crossover_uniforme(padre1, padre2)

        punto_crossover1 = np.random.randint(1, longitud1 - 1)
        punto_crossover2 = np.random.randint(1, longitud2 - 1)

        descendiente1_indices = set(solucion1[:punto_crossover1] + solucion2[punto_crossover2:])
        descendiente2_indices = set(solucion2[:punto_crossover2] + solucion1[punto_crossover1:])

        # Asegurar que al menos una instalacion esté abierta
        if not descendiente1_indices:
            descendiente1_indices = {random.choice(list(padre1['solucion'].union(padre2['solucion'])))}
        if not descendiente2_indices:
             descendiente2_indices = {random.choice(list(padre1['solucion'].union(padre2['solucion'])))}
        return {'solucion': descendiente1_indices, 'fitness': None}, {'solucion': descendiente2_indices, 'fitness': None}

    def _operador_crossover(self, padre1, padre2):
        if self.tipo_crossover == 'uniforme':
            return self._crossover_uniforme(padre1, padre2)
        elif self.tipo_crossover == 'un punto':
            return self._crossover_un_punto(padre1, padre2)
        else:
            print(f"Tipo de crossover '{self.tipo_crossover}' no lo conozco, usando uniforme.")
            return self._crossover_uniforme(padre1, padre2)
        
    def _mutar_random(self, individuo):
        indices_mutados = set(individuo['solucion'])
        num_abiertas = len(indices_mutados)
        todas_instalaciones = set(range(self.n_instalaciones))

        if random.random() < self.tasa_mutacion:
            if num_abiertas > 1 and random.random() < 0.33:
                indice_eliminar = random.choice(list(indices_mutados))
                indices_mutados.remove(indice_eliminar)
            elif num_abiertas < self.n_instalaciones and random.random() < 0.66:
                indices_cerradas = todas_instalaciones - indices_mutados
                if indices_cerradas:
                    indice_agregar = random.choice(list(indices_cerradas))
                    indices_mutados.add(indice_agregar)
            elif num_abiertas > 0 and self.n_instalaciones > num_abiertas:
                indice_eliminar = random.choice(list(indices_mutados))
                indices_cerradas = todas_instalaciones - indices_mutados
                if indices_cerradas:
                    indice_agregar = random.choice(list(indices_cerradas))
                    indices_mutados.remove(indice_eliminar)
                    indices_mutados.add(indice_agregar)
        return {'solucion': indices_mutados, 'fitness': None}

    def _mutar_mejor(self, individuo):
        original_solucion = individuo['solucion']
        original_fitness = individuo['fitness'] # Usar el fitness almacenado
        if original_fitness is None:
            original_fitness = self._calcular_fitness(individuo)
        max_intentos = 5
        todas_instalaciones = set(range(self.n_instalaciones))

        for _ in range(max_intentos):
            indices_mutados = set(original_solucion.copy())
            num_abiertas = len(indices_mutados)

            if num_abiertas > 1 and random.random() < 0.33:
                indice_eliminar = random.choice(list(indices_mutados))
                indices_mutados.remove(indice_eliminar)
            elif num_abiertas < self.n_instalaciones and random.random() < 0.66:
                indices_cerradas = todas_instalaciones - indices_mutados
                if indices_cerradas:
                    indice_agregar = random.choice(list(indices_cerradas))
                    indices_mutados.add(indice_agregar)
            elif num_abiertas > 0 and self.n_instalaciones > num_abiertas:
                indice_eliminar = random.choice(list(indices_mutados))
                indices_cerradas = todas_instalaciones - indices_mutados
                if indices_cerradas:
                    indice_agregar = random.choice(list(indices_cerradas))
                    indices_mutados.remove(indice_eliminar)
                    indices_mutados.add(indice_agregar)

            nuevo_individuo = {'solucion': indices_mutados, 'fitness': None}
            nuevo_fitness = self._calcular_fitness(nuevo_individuo)
            nuevo_individuo['fitness'] = nuevo_fitness # Almacenar el fitness

            if nuevo_fitness <= original_fitness:
                return nuevo_individuo

        return {'solucion': original_solucion, 'fitness': original_fitness}

    def _mutar(self, individuo):
        if self.tipo_mutacion == 'random':
            return self._mutar_random(individuo)
        elif self.tipo_mutacion == 'mejor':
            return self._mutar_mejor(individuo)

    def _reemplazo(self, nueva_poblacion):
        for individuo in nueva_poblacion:
            if individuo['fitness'] is None:
                individuo['fitness'] = self._calcular_fitness(individuo)
        nueva_poblacion.append({'solucion': self.mejor_solucion, 'fitness': self.mejor_fitness})
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
                    nueva_poblacion.append(self._mutar({'solucion': padre1['solucion'].copy(), 'fitness': padre1['fitness']})) # Pasar el fitness
                    nueva_poblacion.append(self._mutar({'solucion': padre2['solucion'].copy(), 'fitness': padre2['fitness']})) # Pasar el fitness

            self._reemplazo(nueva_poblacion)
            self._evaluar_poblacion()
            self.historial_fitness.append(self.mejor_fitness)

            generacion_opti = None
            if self.fitness_objetivo is not None and self.mejor_fitness <= self.fitness_objetivo:
                generacion_opti = generacion + 1
                break

        tiempo_fin = time.time()
        return self.mejor_solucion, self.mejor_fitness, self.historial_fitness, tiempo_fin - tiempo_inicio, self.generacion + 1, generacion_opti
