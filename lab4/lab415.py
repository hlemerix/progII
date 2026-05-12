# la estructura definitiva: un diccionario de tuplas
panama = {
    "provincias": ("Bocas del Toro", "Coclé", "Colón", "Chiriquí", "Darién", "Herrera", "Los Santos", "Panamá", "Veraguas", "Panamá Oeste"),
    "comarcas": ("Guna Yala", "Ngäbe-Buglé", "Emberá-Wounaan", "Madugandí", "Wargandí")
}

def check_status():
    for categoria, lista in panama.items():
        print(f"nuestra seleccion de {categoria}:")
        print(lista)

if __name__ == "__main__":
    check_status()

    # el sistema protege el orden automáticamente
    try:
        panama["provincias"].reverse()
    except AttributeError:
        print("\nlo siento, el orden es inalterable para mantener la esencia")