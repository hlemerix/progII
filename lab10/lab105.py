class Factorial:
    def __init__(self, num):
        self.num = num
 
    def calcular(self):
        if self.num < 0:
            raise ValueError("No existe factorial de números negativos.")
        resultado = 1
        for i in range(2, self.num + 1):
            resultado *= i
        return resultado
 
    def __str__(self):
        return f"{self.num}! = {self.calcular()}"
try:
    n = int(input("Ingrese un número entero para calcular su factorial: "))
    factorial = Factorial(n)
    print(factorial)
except ValueError as e:
    print(f"Error: {e}")