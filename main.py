from roundRobin import definir

def main():
    cantidad_de_procesos = int(input("Introduzca la cantidad de trabajos a procesar: "))
    quantum = int(input("Introduzca el quantum: "))
    definir(cantidad_de_procesos, quantum)

main()