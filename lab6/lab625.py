y = True
while y == True:
    x = input("Ingrese un numero: ")
    try:
        x = float(x)
        y = False
    except:
        print("Entrada incorrecta, intente de nuevo ")
        print("Gracias!")
        