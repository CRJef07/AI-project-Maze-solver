import csv
import time
import numpy
import psutil
from memory_profiler import profile


class Grafo:
    def __init__(self, archivo):
        self.grafo = self.leer_archivo(archivo)
        self.filas, self.columnas = self.grafo.shape
        self.nodo_inicio = None
        self.nodo_final = None

    def leer_archivo(self, archivo):
        with open(archivo, 'r') as archivocsv:
            leer_archivo = csv.reader(archivocsv)
            return numpy.array([[int(cell) for cell in row] for row in leer_archivo])

    def inicializar_nodos(self):
        nodo_inicio = None
        nodo_final = None
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.grafo[i, j] == 2:
                    nodo_inicio = (i, j)
                elif self.grafo[i, j] == 3:
                    nodo_final = (i, j)
        if nodo_inicio is None or nodo_final is None:
            raise ValueError("No se encontraron los nodos")
        self.nodo_inicio = nodo_inicio
        self.nodo_final = nodo_final

    # @profile
    def bfs(self):
        if self.nodo_inicio is None or self.nodo_final is None:
            self.inicializar_nodos()

        visitado = numpy.zeros_like(self.grafo, dtype=bool)
        queue = [(self.nodo_inicio, [])]
        camino_resultado = []

        while queue:
            (x, y), camino = queue.pop(0)

            if (x, y) == self.nodo_final:
                camino_resultado = camino
                # self.imprimir_consola(camino)
                break

            visitado[x, y] = True

            vecinos = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

            for vecino_x, vecino_y in vecinos:
                if (
                        0 <= vecino_x < self.filas
                        and 0 <= vecino_y < self.columnas
                        and not visitado[vecino_x, vecino_y]
                        and self.grafo[vecino_x, vecino_y] != 1
                ):
                    queue.append(((vecino_x, vecino_y), camino + [(x, y)]))

        if camino_resultado is not None:
            self.imprimir_consola(camino_resultado)
            self.guardar_camino_en_csv(camino_resultado)
        else:
            print("No se encontró un camino correcto")

    def imprimir_consola(self, ruta):
        print("Ruta mínima encontrada:")
        for i in range(self.filas):
            for j in range(self.columnas):
                if (i, j) == self.nodo_inicio:
                    print("2", end=" ")
                elif (i, j) == self.nodo_final:
                    print("3", end=" ")
                elif (i, j) in ruta:
                    print("5", end=" ")
                else:
                    print("0" if self.grafo[i, j] == 0 else "1", end=" ")
            print()

    def guardar_camino_en_csv(self, camino):
        with open("bfs_output/output.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(self.filas):
                row = []
                for j in range(self.columnas):
                    if (i, j) == self.nodo_inicio:
                        row.append("2")
                    elif (i, j) == self.nodo_final:
                        row.append("3")
                    elif (i, j) in camino:
                        row.append("5")
                    else:
                        row.append("0" if self.grafo[i, j] == 0 else "1")
                writer.writerow(row)

    def guardar_tiempo_memoria(self, duracion, memoria):
        with open("bfs_output/output.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow("")
            writer.writerow([f"Tiempo de ejecucion: {duracion:.6f} segundos"])
            writer.writerow([f"Uso de memoria: {memoria:.2f} MB"])


def ejecutar():
    algoritmo = Grafo("laberinto.csv")
    tiempo_inicio: float = time.time()
    algoritmo.bfs()
    tiempo_final: float = time.time()
    duracion = tiempo_final - tiempo_inicio
    memoria = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"Tiempo de ejecución: {duracion:.6f} segundos")
    print(f"Uso de memoria: {memoria:.2f} MB")
    algoritmo.guardar_tiempo_memoria(duracion, memoria)


if __name__ == '__main__':
    ejecutar()
