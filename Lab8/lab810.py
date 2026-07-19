class Persona:
    def __init__(self,nom, ape):
        self.__nombre = nom
        self.__edad = ape
    def obtener_edad(self):
        return self.__edad
    def asignar_edad(self, ed):
        if ed > 0:
            self.__edad = ed
        else:
         print("la edad debe ser un valor positivo")
p1 = Persona("Fulano", 28)
print(p1.obtener_edad())
p1.asignar_edad(29)
print(p1.obtener_edad())
