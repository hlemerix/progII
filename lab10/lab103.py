print("Modo 'a': Agregar contenido al archivo ")
with open("archivo_demo.txt", "a", encoding="utf-8") as f:
    f.write("¡Ahora el archivo tiene más contenido!")
 
           # Leer el archivo después de agregar contenido
with open("archivo_demo.txt", encoding="utf-8") as f:
    print(f.read())
 
print("\n Modo 'w': Sobrescribir el contenido existente ")
with open("archivo_demo.txt", "w", encoding="utf-8") as f:
    f.write("¡Ups! ¡He borrado el contenido!")
 
   # Leer el archivo después de sobrescribirlo
with open("archivo_demo.txt", encoding="utf-8") as f:
    print(f.read())