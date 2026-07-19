print("Leer dos líneas con readline()")
with open("archivo_demo.txt", encoding="utf-8") as f:
    print(f.readline())
    print(f.readline())
 
print(" Recorrer todo el archivo línea por línea ")
with open("archivo_demo.txt", encoding="utf-8") as f:
    for x in f:
        print(x, end="")