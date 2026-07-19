import os
if os.path.exists("archivo_demo.txt"):
    os.remove("archivo_demo.txt")
    print("Archivo 'archivo_demo.txt' eliminado exitosamente.")
else:
    print("The file does not exist")