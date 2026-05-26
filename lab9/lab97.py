from typing import final 
class Padre:
    @final
    def metodo_sagrado(self):
        print("no me cambies.")
class Hijo(Padre):
    #un linter (como MyPy) marcara esto como ERROR:
    def metodo_sagrado(self):
        print("Intentando cambiarlo.")
           