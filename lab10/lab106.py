from abc import ABC, abstractmethod
import math
class Figura(ABC):
    @abstractmethod
    def calcularArea(self):
        pass
 
    def __str__(self):
        return f"{self.__class__.__name__}: área = {self.calcularArea():.2f}"
class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio
 
    def calcularArea(self):
        return math.pi * self.radio ** 2
class Rectangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
 
    def calcularArea(self):
        return self.base * self.altura
class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
 
    def calcularArea(self):
        return (self.base * self.altura) / 2
figuras = [
    Circulo(56),
    Rectangulo(4, 6),
    Triangulo(3, 8),
    Circulo(2.5),
    Rectangulo(14, 3),
]
 
print(" Áreas de las figuras ")
for figura in figuras:
    print(figura)