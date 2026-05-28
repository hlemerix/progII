with open("archivo_demo.txt", "w", encoding="utf-8") as f:
    f.write("¡Hola! Bienvenido a archivo_demo.txt\n")
    f.write("Este archivo es para fines de prueba.\n")
    f.write("¡Buena suerte!\n")
 
print("Forma 1: usando 'with' (cierre automático)")
with open("archivo_demo.txt", "r", encoding="utf-8") as f:
    print(f.read())
 
print("Forma 2: apertura y cierre manual ")
f = open("archivo_demo.txt", encoding="utf-8")
print(f.readline())
f.close()