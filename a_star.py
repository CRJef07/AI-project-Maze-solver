import heapq
import csv
import timeit
import numpy
import psutil
import random


class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.costo_desde_inicio = 0  # Costo desde el nodo de inicio hasta este nodo
        self.heuristica = 0  # Costo estimado desde este nodo hasta el nodo objetivo
        self.costo_total = 0  # Costo total (f = g + h)

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

        vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos arriba, abajo, izquierda, derecha
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
    laberinto = leer_archivo('laberinto.csv')  # Reemplaza con el nombre de tu archivo CSV
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

    # Medir el tiempo de ejecución usando timeit
    tiempo_ejecucion_optimo = timeit.timeit(lambda: astar(laberinto, inicio, fin), number=1)

    uso_memoria_optimo = psutil.Process().memory_info().rss / 1024 / 1024  # Obtener el uso de memoria en megabytes

    camino_optimo = astar(laberinto, inicio, fin)

    if camino_optimo is None:
        print("No hay un camino válido desde el punto de inicio hasta el punto de fin.")
        return

    # Crear una copia del laberinto para mostrar el camino óptimo
    laberinto_con_camino_optimo = [fila[:] for fila in laberinto]

    for fila, col in camino_optimo:
        laberinto_con_camino_optimo[fila][col] = 4

    # Generar dos caminos aleatorios
    random.seed(42)  # Semilla para reproducibilidad
    inicio_aleatorio = (random.randint(0, len(laberinto) - 1), random.randint(0, len(laberinto[0]) - 1))
    fin_aleatorio = (random.randint(0, len(laberinto) - 1), random.randint(0, len(laberinto[0]) - 1))

    camino_aleatorio1 = astar(laberinto, inicio_aleatorio, fin_aleatorio)

    # Asegurarse de que los caminos aleatorios sean válidos

    # Mostrar los caminos
    print("El mejor camino es:")
    imprimir_laberinto(laberinto_con_camino_optimo)

    print(f"\nTiempo de Ejecución: {tiempo_ejecucion_optimo:.6f} segundos")
    print(f"Uso de Memoria: {uso_memoria_optimo:.2f} MB")

    # Guardar las tres matrices y sus estadísticas en un solo archivo CSV

    with open("a_star_output/output.csv", 'w', newline='') as csvfile:
        escritor = csv.writer(csvfile, delimiter=' ')

        # Guardar el camino óptimo
        # escritor.writerow(["Camino Óptimo"])
        for fila in laberinto_con_camino_optimo:
            escritor.writerow(fila)
        escritor.writerow("")
        # Guardar estadísticas de tiempo y memoria
        escritor.writerow(["Tiempo de Ejecucion:", tiempo_ejecucion_optimo])
        escritor.writerow(["Uso de Memoria:", uso_memoria_optimo])
#
#
# if __name__ == "__main__":
#     main()
