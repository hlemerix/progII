class Usuario:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    @classmethod
    def crear_anonimo(cls):
        #'cls' es equivalente a usar 'Usuario'
        return cls("Anonimo", 0) 
# Uso del constructor alternativo
invitado = Usuario.crear_anonimo()
<<<<<<< HEAD
=======

class Usuario:
 
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad
 
    @classmethod
    def crear_anonimo(cls):
        # 'cls' es equivalente a usar 'Usuario' directamente
        return cls("Anónimo", 0)
 
    @classmethod
    def crear_desde_cadena(cls, cadena: str):
        """Constructor alternativo: recibe 'Nombre,Edad' como string."""
        partes = cadena.split(",")
        nombre = partes[0].strip()
        edad = int(partes[1].strip())
        return cls(nombre, edad)
 
    def mostrar(self):
        print(f"Usuario: {self.nombre}, Edad: {self.edad}")
 
# Uso del constructor estándar
u1 = Usuario("Hanna", 20)
u1.mostrar()                          # Usuario: Hanna, Edad: 20
 
# Uso del constructor alternativo (anónimo)
invitado = Usuario.crear_anonimo()
invitado.mostrar()                    # Usuario: Anónimo, Edad: 0
 
# Uso del constructor alternativo (desde cadena)
u2 = Usuario.crear_desde_cadena("Jose, 31")
u2.mostrar()                          # Usuario: Jose, Edad: 31
 
>>>>>>> 04e2dc1 (Reemplazo de la carpeta lab9 con las versiones modificadas)
