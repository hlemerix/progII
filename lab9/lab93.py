class persona:
    # Atributo estatico (compartidos por todas las instancias 
    contador = 0   
    def __init__(self):
        persona.contador += 1 # se accede con el nombre de la clase
        
