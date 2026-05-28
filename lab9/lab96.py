from typing import final
@final
class Base:
    pass
# un linter (como MyPy) marcara esto como ERROR:
class Derivada(Base):
<<<<<<< HEAD
    pass    
=======
    pass    

#modificación 
from typing import final
 
# Clases Finales: el decorador @final le indica al linter que esta clase
# NO debe ser heredada. Equivalente a 'final class' en Java.
# NOTA: Python NO lanza error en ejecución; el error lo detecta MyPy o VS Code.
 
@final
class Base:
    def saludar(self):
        print("Hola desde Base (clase final).")
 
# Un linter (como MyPy) marcará esto como ERROR:
# Cannot inherit from final class "Base"
class Derivada(Base):   # <-- MyPy/Pylance advertirá aquí
    pass
 
# Demostración
b = Base()
b.saludar()                   # Funciona normalmente
 
d = Derivada()
d.saludar()                   # Python lo ejecuta igualmente (no hay error en runtime)
                              # pero el linter lo marca como violación de diseño
 
>>>>>>> 04e2dc1 (Reemplazo de la carpeta lab9 con las versiones modificadas)
