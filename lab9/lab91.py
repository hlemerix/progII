from abc import ABC, abstractmethod 
class Vehiculo(ABC): #Heredar de ABC la hace abstracta 
    @abstractmethod 
    def arrancar(self): 
        """Metodo abstracto: obligatorio implementar en el hijo."""
        pass
    def pitar(self): 
        """Método normal: ya tiene logica heredable."""
        print("Beep beep!")
class Moto (Vehiculo):
    def arrancar(self):
        print("La moto ha arrancado.")  
# Uso
# # mi_vehiculo = Vehiculo() # Error: no se puede instanciar 
mi_moto = Moto()
mi_moto.arrancar() # Imprime: La moto ha arrancado.
mi_moto.pitar() # Imprime: Beep beep!