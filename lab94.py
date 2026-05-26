class Calculadora:
    @staticmethod
    def sumar(a, b):
        return a + b # no usa 'self' ni 'cls'
    #se llama directamente sin instanciar 
resultado = Calculadora.sumar(5, 3)