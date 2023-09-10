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

    def leer_archivo(self, archivo):
        with open(archivo, 'r') as archivocsv:
            leer_archivo = csv.reader(archivocsv)
            return numpy.array([[int(cell) for cell in row] for row in leer_archivo])

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

    def bellman_ford(self):
        if self.nodo_inicio is None or self.nodo_final is None:
            self.inicializar_nodos()

        def get_distancia():
            distancia_total = [[float('inf') for _ in range(self.columnas)] for _ in range(self.filas)]
            return distancia_total

        distancia = get_distancia()
        parent = [[None for _ in range(self.columnas)] for _ in range(self.filas)]

        inicio_fila, inicio_col = self.nodo_inicio
        objetivo_fila, objetivo_col = self.nodo_final

        distancia[inicio_fila][inicio_col] = 0

        for _ in range(self.filas * self.columnas - 1):
            for r in range(self.filas):
                for c in range(self.columnas):
                    if self.matriz[r][c] == 1:
                        continue
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.filas and 0 <= nc < self.columnas and distancia[r][c] + 1 < distancia[nr][nc]:
                            distancia[nr][nc] = distancia[r][c] + 1
                            parent[nr][nc] = (r, c)

        if distancia[objetivo_fila][objetivo_col] == float('inf'):
            return None

        camino = []
        r, c = objetivo_fila, objetivo_col
        while (r, c) != (inicio_fila, inicio_col):
            camino.append((r, c))
            r, c = parent[r][c]
        camino.append((inicio_fila, inicio_col))
        camino.reverse()

        self.imprimir_consola(camino)
        self.guardar_ruta_en_csv(camino)

    def inicio_fin(self):
        inicio = None
        objetivo = None
        for fila_num, fila in enumerate(self.matriz):
            for col_num, valor in enumerate(fila):
                if valor == 2:
                    inicio = (fila_num, col_num)
                elif valor == 3:
                    objetivo = (fila_num, col_num)

        if inicio is None or objetivo is None:
            raise ValueError("No se pudo encontrar el punto de inicio o el objetivo en la Matriz XP.")

        return inicio, objetivo

    def guardar_ruta_en_csv(self, ruta):
        with open("bellman_ford_output/output.csv", 'w', newline='') as csvfile:
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
        with open("bellman_ford_output/output.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow("")
            writer.writerow([f"Tiempo de ejecucion: {duracion:.6f} segundos"])
            writer.writerow([f"Uso de memoria: {memoria:.2f} MB"])


def ejecutar():
    algoritmo = Grafo("laberinto.csv")
    tiempo_inicio: float = time.time()
    algoritmo.bellman_ford()
    tiempo_final: float = time.time()
    duracion = tiempo_final - tiempo_inicio
    memoria = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"Tiempo de ejecución: {duracion:.6f} segundos")
    print(f"Uso de memoria: {memoria:.2f} MB")
    algoritmo.guardar_tiempo_memoria(duracion, memoria)


if __name__ == "__main__":
    ejecutar()
