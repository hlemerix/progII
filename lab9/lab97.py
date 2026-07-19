from typing import final 
class Padre:
    @final
    def metodo_sagrado(self):
        print("no me cambies.")
class Hijo(Padre):
    #un linter (como MyPy) marcara esto como ERROR:
    def metodo_sagrado(self):
        print("Intentando cambiarlo.")
<<<<<<< HEAD
           
=======

        #modificación 
class Padre:
 
    @final
    def metodo_sagrado(self):
        print("No me cambies.")
 
    def metodo_normal(self):
        print("Este sí puedes sobreescribir.")
 
class Hijo(Padre):
 
    # Un linter (como MyPy) marcará esto como ERROR:
    # Cannot override final attribute "metodo_sagrado"
    def metodo_sagrado(self):         # <-- Pylance/MyPy advertirá aquí
        print("Intentando cambiarlo.")
 
    def metodo_normal(self):          # Esto está permitido
        print("Método normal sobreescrito en Hijo.")
 
# Demostración
padre = Padre()
padre.metodo_sagrado()        # No me cambies.
padre.metodo_normal()         # Este sí puedes sobreescribir.
 
hijo = Hijo()
hijo.metodo_sagrado()         # Python lo ejecuta (no hay error en runtime)
hijo.metodo_normal()          # Método normal sobreescrito en Hijo.
 
>>>>>>> 04e2dc1 (Reemplazo de la carpeta lab9 con las versiones modificadas)
