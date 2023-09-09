import csv
import time

import numpy
import psutil


class Grafo:
    def __init__(self, archivo):
        self.matriz = self.leer_archivo(archivo)
        self.nodo_inicio = None
        self.nodo_final = None
        self.filas, self.columnas = self.matriz.shape

    def inicializar_nodos(self):
        nodo_inicio = None
        nodo_final = None
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i, j] == 2:
                    nodo_inicio = (i, j)
                elif self.matriz[i, j] == 3:
                    nodo_final = (i, j)
        if nodo_inicio is None or nodo_final is None:
            raise ValueError("No se encontraron los nodos")
        self.nodo_inicio = nodo_inicio
        self.nodo_final = nodo_final

    def leer_archivo(self, archivo):
        with open(archivo, 'r') as archivocsv:
            leer_archivo = csv.reader(archivocsv)
            return numpy.array([[int(cell) for cell in row] for row in leer_archivo])

    def dfs(self):
        if self.nodo_inicio is None or self.nodo_final is None:
            self.inicializar_nodos()

        def movimiento_valido(x, y):
            return 0 <= x < self.filas and 0 <= y < self.columnas and self.matriz[x][y] != 1

        def ruta(x, y, path):
            if (x, y) == self.nodo_final:
                return path + [(x, y)]

            if not movimiento_valido(x, y) or (x, y) in path:
                return None

            path.append((x, y))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                resultado = ruta(new_x, new_y, path)
                if resultado is not None:
                    return resultado

            path.pop()
            return None

        camino = ruta(self.nodo_inicio[0], self.nodo_inicio[1], [])

        if camino is not None:
            for x, y in camino:
                self.matriz[x][y] = 5
            self.imprimir_consola(camino)
            self.guardar_ruta_en_csv(camino)

    def guardar_ruta_en_csv(self, ruta):
        with open("dfs_output/output.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(self.filas):
                row = []
                for j in range(self.columnas):
                    if (i, j) == self.nodo_inicio:
                        row.append("2")
                    elif (i, j) == self.nodo_final:
                        row.append("3")
                    elif (i, j) in ruta:
                        row.append("5")
                    else:
                        row.append("0" if self.matriz[i, j] == 0 else "1")
                writer.writerow(row)

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
                    print("0" if self.matriz[i, j] == 0 else "1", end=" ")
            print()

    def guardar_tiempo_memoria(self, duracion, memoria):
        with open("dfs_output/output.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow("")
            writer.writerow([f"Tiempo de ejecucion: {duracion:.6f} segundos"])
            writer.writerow([f"Uso de memoria: {memoria:.2f} MB"])


def ejecutar():
    algoritmo = Grafo("laberinto.csv")
    tiempo_inicio: float = time.time()
    algoritmo.dfs()
    tiempo_final: float = time.time()
    duracion = tiempo_final - tiempo_inicio
    memoria = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"Tiempo de ejecución: {duracion:.6f} segundos")
    print(f"Uso de memoria: {memoria:.2f} MB")
    algoritmo.guardar_tiempo_memoria(duracion, memoria)


if __name__ == "__main__":
    ejecutar()
