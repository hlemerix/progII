class persona:
    # Atributo estatico (compartidos por todas las instancias 
    contador = 0   
    def __init__(self):
        persona.contador += 1 # se accede con el nombre de la clase
        
<<<<<<< HEAD
=======
 
class Persona:
    # Atributo estático (compartido por todas las instancias)
    contador = 0
 
    def __init__(self, nombre: str):
        self.nombre = nombre                  # Atributo de instancia
        Persona.contador += 1                 # Se accede con el nombre de la clase
 
    def mostrar(self):
        print(f"Nombre: {self.nombre}")
 
# Uso
p1 = Persona("Ana")
p2 = Persona("Johany")
p3 = Persona("Jose")
 
p1.mostrar()
p2.mostrar()
p3.mostrar()
 
# El contador es compartido: refleja el total de instancias creadas
print(f"Total de personas creadas: {Persona.contador}")   # 3
 

>>>>>>> 04e2dc1 (Reemplazo de la carpeta lab9 con las versiones modificadas)
