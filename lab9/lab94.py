class Calculadora:
    @staticmethod
    def sumar(a, b):
        return a + b # no usa 'self' ni 'cls'
    #se llama directamente sin instanciar 
<<<<<<< HEAD
resultado = Calculadora.sumar(5, 3)
=======
resultado = Calculadora.sumar(5, 3)

class Calculadora:
 
    @staticmethod
    def sumar(a, b):
        return a + b    # No usa 'self' ni 'cls'
 
    @staticmethod
    def restar(a, b):
        return a - b
 
    @staticmethod
    def multiplicar(a, b):
        return a * b
 
    @staticmethod
    def dividir(a, b):
        if b == 0:
            print("Error: no se puede dividir entre cero.")
            return None
        return a / b
 
# Se llama directamente sin instanciar la clase
resultado = Calculadora.sumar(5, 3)
print(f"5 + 3 = {resultado}")           # 8
 
print(f"10 - 4 = {Calculadora.restar(10, 3)}")          
print(f"6 x 7 = {Calculadora.multiplicar(6, 7)}")       
print(f"15 / 6 = {Calculadora.dividir(15, 6)}")         
print(f"19 / 0 = {Calculadora.dividir(19, 0)}")         
>>>>>>> 04e2dc1 (Reemplazo de la carpeta lab9 con las versiones modificadas)
