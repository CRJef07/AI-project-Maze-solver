import heapq
import csv
import timeit
import numpy
import psutil
import random
from memory_profiler import profile


class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.costo_desde_inicio = 0
        self.heuristica = 0

    def __lt__(self, otro):
        return self.costo_total < otro.costo_total


def leer_laberinto(archivo):
    laberinto = []
    with open(archivo, 'r') as csvfile:
        lector = csv.reader(csvfile, delimiter=' ')
        for fila in lector:
            laberinto.append([int(celda) for celda in fila])
    return laberinto


def leer_archivo(archivo):
    with open(archivo, 'r') as archivocsv:
        leer_archivo = csv.reader(archivocsv)
        return numpy.array([[int(cell) for cell in row] for row in leer_archivo])


def imprimir_laberinto(laberinto):
    for fila in laberinto:
        print(' '.join(map(str, fila)))


def es_valido(laberinto, fila, col):
    return 0 <= fila < len(laberinto) and 0 <= col < len(laberinto[0]) and laberinto[fila][col] != 1

# @profile
def astar(laberinto, inicio, fin):
    lista_abierta = []
    conjunto_cerrado = set()
    nodo_inicio = Nodo(inicio)
    nodo_fin = Nodo(fin)
    heapq.heappush(lista_abierta, nodo_inicio)

    while lista_abierta:
        nodo_actual = heapq.heappop(lista_abierta)
        conjunto_cerrado.add(nodo_actual.posicion)

        if nodo_actual.posicion == nodo_fin.posicion:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1]

        vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for vecino in vecinos:
            nueva_posicion = (nodo_actual.posicion[0] + vecino[0], nodo_actual.posicion[1] + vecino[1])

            if (
                    not es_valido(laberinto, nueva_posicion[0], nueva_posicion[1])
                    or nueva_posicion in conjunto_cerrado
            ):
                continue

            nodo_vecino = Nodo(nueva_posicion, nodo_actual)
            nodo_vecino.costo_desde_inicio = nodo_actual.costo_desde_inicio + 1
            nodo_vecino.heuristica = abs(nueva_posicion[0] - nodo_fin.posicion[0]) + abs(
                nueva_posicion[1] - nodo_fin.posicion[1])
            nodo_vecino.costo_total = nodo_vecino.costo_desde_inicio + nodo_vecino.heuristica

            if any(nodo_vecino.posicion == nodo.posicion and nodo_vecino.costo_total >= nodo.costo_total for nodo in
                   lista_abierta):
                continue

            heapq.heappush(lista_abierta, nodo_vecino)

    return None


def ejecutar():
    laberinto = leer_archivo('laberinto.csv')
    inicio = None
    fin = None

    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            for col in range(len(laberinto[0])):
                if laberinto[fila][col] == 2:
                    inicio = (fila, col)
                elif laberinto[fila][col] == 3:
                    fin = (fila, col)

    if inicio is None or fin is None:
        print("No se encontraron puntos de inicio o fin en el laberinto.")
        return

    tiempo_ejecucion_optimo = timeit.timeit(lambda: astar(laberinto, inicio, fin), number=1)

    uso_memoria_optimo = psutil.Process().memory_info().rss / 1024 / 1024

    camino_optimo = astar(laberinto, inicio, fin)

    if camino_optimo is None:
        print("No hay un camino válido desde el punto de inicio hasta el punto de fin.")
        return

    laberinto_con_camino_optimo = [fila[:] for fila in laberinto]

    for fila, col in camino_optimo:
        laberinto_con_camino_optimo[fila][col] = 5

    random.seed(42)

    print("El mejor camino es:")
    imprimir_laberinto(laberinto_con_camino_optimo)

    print(f"\nTiempo de Ejecución: {tiempo_ejecucion_optimo:.6f} segundos")
    print(f"Uso de Memoria: {uso_memoria_optimo:.2f} MB")

    with open("a_star_output/output.csv", 'w', newline='') as csvfile:
        escritor = csv.writer(csvfile, delimiter=' ')

        for fila in laberinto_con_camino_optimo:
            escritor.writerow(fila)
        escritor.writerow("")
        escritor.writerow(["Tiempo de Ejecucion:", tiempo_ejecucion_optimo])
        escritor.writerow(["Uso de Memoria:", uso_memoria_optimo])


if __name__ == "__main__":
    ejecutar()
