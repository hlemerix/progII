#1. Literal de bytes(forma más común)
mi_bytes = b"\xFF"
#2. Constructor de bytes a partir de un entero
mi_byte_dos = bytes([255])
#verificación
print(type(mi_bytes)) #<class 'bytes'>
print(mi_bytes[0]) # 255
