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
        return datos.replace("AES(", "").replace(")", "")