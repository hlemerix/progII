def main():
    try:
        n = int(input("Ingrese el orden de la matriz (par): "))
        
        if n % 2 != 0:
            print("Error: El número debe ser par.")
            return

        print(f"\nMatriz Identidad {n}x{n}:")
        for i in range(n):
            # Genera la fila con 1 en la diagonal y 0 en el resto
            fila = [1 if i == j else 0 for j in range(n)]
            print(f"| {' '.join(map(str, fila))} |")
            
    except ValueError:
        print("Error: Entrada no válida.")

if __name__ == "__main__":
    main()