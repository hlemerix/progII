import string

def contar_palabras_unicas(t):
    t = t.translate(str.maketrans('', '', string.punctuation)).lower()
    return len(set(t.split()))

def palabra_mas_larga(t):
    p = t.translate(str.maketrans('', '', string.punctuation)).split()
    return max(p, key=len) if p else ""

def frecuencia_caracteres(t):
    l = [c.lower() for c in t if c != " "]
    for c in sorted(set(l)):
        p = (l.count(c)/len(l))*100
        print(f"{c}: {l.count(c)} ({p:.1f}%)")

if __name__ == "__main__":
    s = input("Texto: ")
    if s.strip():
        print(f"Únicas: {contar_palabras_unicas(s)}\nLarga: {palabra_mas_larga(s)}")
        frecuencia_caracteres(s)