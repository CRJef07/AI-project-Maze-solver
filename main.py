import os

import bfs
import dijkstra
import a_star
import dfs
import bellman_ford


def limpiar_consola():
    if os.name == 'posix':  # For Unix and Linux
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')


def menu():
    print("Bienvenido!")
    print("1. Algoritmo BFS - Breadth First Search")
    print("2. Algoritmo Dijkstra")
    print("3. Algoritmo A*")
    print("4. Algoritmo DFS - Depth First Search")
    print("5. Algoritmo Bellman Ford")
    print("77. Salir")


def opcion_seleccionada():
    opc = input("Ingrese la opcion que desea: ")
    return opc


def main():
    while True:
        limpiar_consola()
        menu()
        opc = opcion_seleccionada()

        if opc == "1":  # Breadth First Search or BFS
            bfs.ejecutar()
            os.system("pause")

        elif opc == "2":  # Dijkstra
            dijkstra.ejecutar()
            os.system("pause")

        elif opc == "3":  # A*
            a_star.ejecutar()
            os.system("pause")

        elif opc == "4":  # Depth First Search
            dfs.ejecutar()
            os.system("pause")

        elif opc == "5":  # Bellman – Ford
            bellman_ford.ejecutar()
            os.system("pause")

        elif opc == "77":
            print("¡¡Hasta luego!!")
            os.system("pause")
            break

        else:
            print("Debe ingresar una opción válida!")
            os.system("pause")


if __name__ == '__main__':
    main()
