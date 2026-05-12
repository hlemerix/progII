def main():
    print("--- CALCULADORA FACTORIAL ---")
    
    try:
        n = int(input("Introduce N: "))
        
        if n < 0:
            print("Error: El número debe ser positivo.")
            return

        fact = 1
        for i in range(1, n + 1):
            fact *= i
            
        print(f">> Resultado: {n}! = {fact}")
        
    except ValueError:
        print("Error: Entrada no válida.")

if __name__ == "__main__":
    main()