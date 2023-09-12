import csv
import networkx as nx
import numpy
import psutil
import timeit
from memory_profiler import profile


class Laberinto:
    def __init__(self, nombre_archivo):
        self.matriz = self.leer_archivo(nombre_archivo)
        self.filas, self.columnas = self.matriz.shape

    def leer_archivo(self, archivo):
        with open(archivo, 'r') as archivocsv:
            leer_archivo = csv.reader(archivocsv)
            return numpy.array([[int(cell) for cell in row] for row in leer_archivo])

    def imprimir_laberinto(self):
        for fila in self.matriz:
            print(' '.join(map(str, fila)))

    def es_valida(self, fila, columna):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas and self.matriz[fila][columna] != 1


class Dijkstra:
    def __init__(self, laberinto):
        self.laberinto = laberinto

    # @profile
    def resolver(self, inicio, fin):
        G = nx.Graph()
        for fila in range(self.laberinto.filas):
            for columna in range(self.laberinto.columnas):
                if self.laberinto.matriz[fila][columna] != 1:
                    G.add_node((fila, columna))

        for fila in range(self.laberinto.filas):
            for columna in range(self.laberinto.columnas):
                if self.laberinto.es_valida(fila, columna):
                    vecinos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1)]
                    vecinos_validos = [(f, c) for f, c in vecinos if self.laberinto.es_valida(f, c)]
                    for vecino in vecinos_validos:
                        G.add_edge((fila, columna), vecino)

        if not nx.has_path(G, source=inicio, target=fin):
            return None

        return nx.shortest_path(G, source=inicio, target=fin)


def ejecutar():
    laberinto = Laberinto('laberinto.csv')
    inicio = None
    fin = None

    for fila in range(laberinto.filas):
        for columna in range(laberinto.columnas):
            if laberinto.matriz[fila][columna] == 2:
                inicio = (fila, columna)
            elif laberinto.matriz[fila][columna] == 3:
                fin = (fila, columna)

    if inicio is None or fin is None:
        print("No se encontraron puntos de inicio o final en el laberinto.")
        return

    dijkstra = Dijkstra(laberinto)

    camino = dijkstra.resolver(inicio, fin)

    if camino is None:
        print("No hay ruta válida desde el punto de inicio al punto final.")
        return

    tiempo_ejecucion = timeit.timeit(lambda: dijkstra.resolver(inicio, fin), number=1)

    print(f"Camino desde {inicio} hasta {fin}:")
    print(camino)
    print("Laberinto con ruta mínima:")
    for fila, columna in camino:
        laberinto.matriz[fila][columna] = 5
    laberinto.imprimir_laberinto()

    uso_memoria = psutil.Process().memory_info().rss / 1024 / 1024

    print(f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
    print(f"Uso de memoria: {uso_memoria:.2f} MB")

    with open("dijkstra_output/output.csv", 'w', newline='') as csvfile:
        escritor = csv.writer(csvfile, delimiter=' ')
        for fila in laberinto.matriz:
            escritor.writerow(fila)
        escritor.writerow("")
        # Guardar estadísticas de tiempo y memoria
        escritor.writerow(["Tiempo de Ejecucion:", tiempo_ejecucion])
        escritor.writerow(["Uso de Memoria:", uso_memoria])


if __name__ == "__main__":
    ejecutar()
