from abc import ABC, abstractmethod
class Encriptador(ABC): # Actua como intefaz pura 
    @abstractmethod 
    def encriptar(self, datos, str)->str: 
        pass
    @abstractmethod
    def desencriptar(self, datos, str)->str: 
        pass
class EncriptadorAES(Encriptador):
    def encriptar(self, datos,str)->str: 
        return f"AES({datos})"
    def desencriptar(self, datos,str)->str: 
<<<<<<< HEAD
        return datos.replace("AES(", "").replace(")", "")
=======
        return datos.replace("AES(", "").replace(")", "")
    
    # modificación 
class Encriptador(ABC):  # Actúa como interfaz pura
 
    @abstractmethod
    def encriptar(self, datos: str) -> str:
        pass
 
    @abstractmethod
    def desencriptar(self, datos: str) -> str:
        pass
 
# Clase concreta que implementa la interfaz
class EncriptadorAES(Encriptador):
 
    def encriptar(self, datos: str) -> str:
        return f"AES({datos})"
 
    def desencriptar(self, datos: str) -> str:
        return datos.replace("AES(", "").replace(")", "")
 
# Uso
enc = EncriptadorAES()
mensaje_cifrado = enc.encriptar("HolaMundo")
print("Encriptado:", mensaje_cifrado)         # Encriptado: AES(HolaMundo)
 
mensaje_original = enc.desencriptar(mensaje_cifrado)
print("Desencriptado:", mensaje_original)     # Desencriptado: HolaMundo
 
# Si olvidas implementar un método, Python lanzará un TypeError al instanciar.
>>>>>>> 04e2dc1 (Reemplazo de la carpeta lab9 con las versiones modificadas)
