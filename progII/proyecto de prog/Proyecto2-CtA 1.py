# ====================================================================
#  Proyecto2-CtA.py
#  FORTIN DE DATOS - Conjunto A (Criptografia y Gestion)
#  Programacion II - Proyecto #2 - Prof. Regis Rivera
#  Objetivo: proteger informacion sensible EN REPOSO usando Python.
#  Version con INTERFAZ GRAFICA (Tkinter).
# ====================================================================

# --------------------------------------------------------------------
#  IMPORTACION DE MODULOS
# --------------------------------------------------------------------
import os          # Manejo de rutas y archivos del sistema operativo.
import json        # Leer y escribir datos en formato JSON.
import base64      # Codificar/decodificar en base64 (llaves Fernet).
import hashlib     # Hashing: PBKDF2 (contrasenas) y SHA-256 (integridad).
import hmac        # Firma HMAC-SHA256 para verificar integridad (como el Proyecto 1).
import secrets     # Generacion criptograficamente segura: salt y contrasenas.
import string      # Conjuntos de caracteres (letras, digitos).

from cryptography.fernet import Fernet, InvalidToken  # Cifrado autenticado (Fernet).
from dotenv import load_dotenv, set_key               # Manejo del archivo .env.

import tkinter as tk                                   # Libreria grafica (interfaz).
from tkinter import ttk, filedialog, messagebox, scrolledtext  # Componentes graficos.


# --------------------------------------------------------------------
#  CONSTANTES DE CONFIGURACION
# --------------------------------------------------------------------
CARPETA = os.path.dirname(os.path.abspath(__file__))     # Carpeta base del proyecto.
RUTA_ENV = os.path.join(CARPETA, ".env")                 # Archivo .env (llaves).
RUTA_USUARIOS = os.path.join(CARPETA, "usuarios.json")   # Archivo de usuarios.
RUTA_FIRMAS = os.path.join(CARPETA, "firmas.json")       # Archivo de firmas HMAC (integridad).

NOMBRE_LLAVE = "LLAVE_MAESTRA"   # Nombre de la variable de entorno de la llave.
SALT_FIRMA = b"SALT_INTEGRIDAD_HMAC"  # Salt fijo para derivar la llave de firma (como el Proyecto 1).
ITERACIONES = 200_000            # Iteraciones de PBKDF2 para contrasenas de login.
ITER_ARCHIVO = 100_000           # Iteraciones de PBKDF2 para cifrar archivos (como el Proyecto 1).
TAM_SALT = 16                    # Tamano del salt en bytes (128 bits).
TAM_BLOQUE = 8192                # Bloque de lectura para archivos grandes.
LONGITUD_MINIMA = 8              # Longitud minima de contrasena.

MINUSCULAS = string.ascii_lowercase   # "abc...xyz"
MAYUSCULAS = string.ascii_uppercase   # "ABC...XYZ"
DIGITOS = string.digits               # "0123456789"
SIMBOLOS = "!@#$%^&*()-_=+[]{}"       # Simbolos permitidos.

# Paleta de colores (esquema navy / teal) para la interfaz.
NAVY = "#1B2A4A"        # Azul marino para el encabezado.
TEAL = "#0E7C7B"        # Verde azulado para acentos y botones.
TEAL_OSCURO = "#0A5E5D"  # Teal mas oscuro (hover/realce).
FONDO = "#F4F6F8"       # Gris muy claro de fondo.
BLANCO = "#FFFFFF"      # Blanco.
VERDE_OK = "#1E7E34"    # Verde para mensajes de exito.
ROJO_ERR = "#C0392B"    # Rojo para mensajes de error/alerta.

# Estado de la sesion: guarda que usuario inicio sesion.
sesion = {"usuario": None}       # Al inicio nadie tiene la sesion iniciada.


# ====================================================================
#  SECCION 1 - GESTION DE LLAVES EN VARIABLES DE ENTORNO  (AMBOS GRUPOS)
# ====================================================================
def asegurar_env():
    """Crea el archivo .env vacio si todavia no existe."""
    if not os.path.exists(RUTA_ENV):     # Si el archivo .env NO existe...
        open(RUTA_ENV, "a").close()      # ...lo crea vacio y lo cierra.


def generar_y_guardar_llave():
    """Genera una nueva llave maestra Fernet y la guarda en .env."""
    asegurar_env()                                       # Garantiza que exista .env.
    nueva_llave = Fernet.generate_key().decode("utf-8")  # Genera la llave y la pasa a texto.
    set_key(RUTA_ENV, NOMBRE_LLAVE, nueva_llave)         # Escribe LLAVE_MAESTRA=... en .env.
    return nueva_llave.encode("utf-8")                   # Devuelve la llave en bytes.


def obtener_llave_maestra():
    """Carga la llave maestra desde .env; si no existe, la genera."""
    asegurar_env()                          # Asegura que .env exista.
    load_dotenv(RUTA_ENV, override=True)    # Carga las variables del .env.
    llave = os.getenv(NOMBRE_LLAVE)         # Lee LLAVE_MAESTRA.
    if not llave:                           # Si aun no hay llave...
        return generar_y_guardar_llave()    # ...la genera y la devuelve.
    return llave.encode("utf-8")            # Si existia, la devuelve en bytes.


def existe_llave():
    """Devuelve True si ya hay una llave maestra en .env."""
    asegurar_env()                          # Asegura que .env exista.
    load_dotenv(RUTA_ENV, override=True)    # Recarga las variables.
    return bool(os.getenv(NOMBRE_LLAVE))    # True si LLAVE_MAESTRA tiene valor.


# ====================================================================
#  SECCION 2 - LOGIN CON SALT Y LLAVES MAESTRAS  (PRIMER GRUPO)
# ====================================================================
def cargar_usuarios():
    """Lee usuarios.json y devuelve un diccionario."""
    if not os.path.exists(RUTA_USUARIOS):   # Si no existe el archivo...
        return {}                           # ...devuelve diccionario vacio.
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:  # Abre en lectura.
        try:                                # Intenta leer como JSON.
            return json.load(archivo)       # Devuelve el diccionario.
        except json.JSONDecodeError:        # Si esta vacio o danado...
            return {}                       # ...devuelve diccionario vacio.


def guardar_usuarios(usuarios):
    """Guarda el diccionario de usuarios en usuarios.json."""
    with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:  # Abre en escritura.
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)  # Escribe el JSON.


def derivar_hash(contrasena, salt):
    """Deriva el hash de la contrasena con PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(             # Funcion lenta a proposito (anti fuerza bruta).
        "sha256",                           # Algoritmo base SHA-256.
        contrasena.encode("utf-8"),         # Contrasena en bytes.
        salt,                               # Salt unico del usuario.
        ITERACIONES,                        # Iteraciones configuradas.
    )                                       # Devuelve el hash en bytes.


def registrar_usuario(usuario, contrasena):
    """Registra un usuario guardando salt + hash (nunca texto plano)."""
    usuario = usuario.strip().lower()       # Normaliza el nombre (sin espacios, minusculas).
    usuarios = cargar_usuarios()            # Carga los usuarios existentes.
    if usuario in usuarios:                 # Si ya existe...
        return False                        # ...no lo registra.

    salt = secrets.token_bytes(TAM_SALT)    # Salt aleatorio y unico (16 bytes).
    hash_derivado = derivar_hash(contrasena, salt)  # Hash de la contrasena con ese salt.

    usuarios[usuario] = {                   # Crea el registro del usuario:
        "salt": salt.hex(),                 #   salt en hexadecimal.
        "hash": hash_derivado.hex(),        #   hash en hexadecimal.
        "iteraciones": ITERACIONES,         #   iteraciones usadas.
    }
    guardar_usuarios(usuarios)              # Guarda en disco.
    return True                             # Registro exitoso.


def verificar_login(usuario, contrasena):
    """Verifica credenciales recalculando el hash con el salt guardado."""
    usuario = usuario.strip().lower()       # Normaliza el nombre.
    usuarios = cargar_usuarios()            # Carga los usuarios.
    if usuario not in usuarios:             # Si el usuario no existe...
        derivar_hash(contrasena, secrets.token_bytes(TAM_SALT))  # Hash falso (gasta tiempo igual).
        return False                        # Login fallido.

    datos = usuarios[usuario]               # Registro del usuario.
    salt = bytes.fromhex(datos["salt"])     # Salt de vuelta a bytes.
    hash_guardado = datos["hash"]           # Hash original almacenado.
    hash_calculado = derivar_hash(contrasena, salt).hex()  # Recalcula el hash.

    return secrets.compare_digest(hash_calculado, hash_guardado)  # Compara en tiempo constante.


def usuario_existe(usuario):
    """Indica si un usuario ya esta registrado."""
    return usuario.strip().lower() in cargar_usuarios()  # True si esta en el diccionario.


def generar_llave_maestra():
    """Genera una nueva llave maestra (reutiliza la Seccion 1)."""
    return generar_y_guardar_llave()        # Crea, guarda y devuelve la llave.


# ====================================================================
#  SECCION 3 - CIFRADO/DESCIFRADO E INTEGRIDAD  (SEGUNDO GRUPO)
# ====================================================================
def cargar_firmas():
    """Lee firmas.json (firmas HMAC) y devuelve un diccionario."""
    if not os.path.exists(RUTA_FIRMAS):      # Si no existe...
        return {}                            # ...diccionario vacio.
    with open(RUTA_FIRMAS, "r", encoding="utf-8") as archivo:  # Abre en lectura.
        try:                                 # Intenta leer como JSON.
            return json.load(archivo)        # Devuelve el diccionario de firmas.
        except json.JSONDecodeError:         # Si esta danado...
            return {}                        # ...diccionario vacio.


def guardar_firmas(firmas):
    """Guarda el diccionario de firmas en firmas.json."""
    with open(RUTA_FIRMAS, "w", encoding="utf-8") as archivo:  # Abre en escritura.
        json.dump(firmas, archivo, indent=4, ensure_ascii=False)  # Escribe el JSON.


def derivar_llave_firma(password):
    """Deriva la llave de firma a partir de la contrasena (PBKDF2 + salt fijo)."""
    return hashlib.pbkdf2_hmac(              # Deriva 32 bytes con PBKDF2-HMAC-SHA256.
        "sha256",                           # Algoritmo SHA-256.
        password.encode("utf-8"),           # Contrasena en bytes.
        SALT_FIRMA,                         # Salt fijo exclusivo para integridad (como Proyecto 1).
        ITER_ARCHIVO,                       # 100 000 iteraciones.
        dklen=32,                           # Llave de 32 bytes.
    )


def firmar_archivo(ruta, password):
    """Genera la firma HMAC-SHA256 del archivo y la guarda (sello de integridad)."""
    with open(ruta, "rb") as archivo:        # Abre el archivo en binario.
        contenido = archivo.read()           # Lee todo el contenido.
    llave = derivar_llave_firma(password)    # Deriva la llave de firma con la contrasena.
    firma = hmac.new(llave, contenido, hashlib.sha256).hexdigest()  # Calcula el HMAC en hex.
    firmas = cargar_firmas()                 # Carga las firmas guardadas.
    firmas[os.path.basename(ruta)] = firma   # Asocia el nombre del archivo a su firma.
    guardar_firmas(firmas)                   # Guarda el diccionario de firmas.
    return firma                             # Devuelve la firma generada.


def verificar_firma(ruta, password):
    """Recalcula la firma HMAC y la compara con la guardada (detecta alteraciones)."""
    nombre = os.path.basename(ruta)          # Nombre del archivo (sin ruta).
    firmas = cargar_firmas()                 # Carga las firmas guardadas.
    if nombre not in firmas:                 # Si el archivo no tiene firma registrada...
        return False                         # ...no se puede verificar.
    with open(ruta, "rb") as archivo:        # Abre el archivo en binario.
        contenido = archivo.read()           # Lee el contenido actual.
    llave = derivar_llave_firma(password)    # Re-deriva la llave de firma.
    firma_actual = hmac.new(llave, contenido, hashlib.sha256).hexdigest()  # Recalcula el HMAC.
    # compare_digest compara en tiempo constante; si un solo byte cambio, no coincide.
    return hmac.compare_digest(firma_actual, firmas[nombre])  # True si esta intacto.


def quitar_firma(ruta):
    """Elimina la firma guardada de un archivo (cuando ya no aplica)."""
    firmas = cargar_firmas()                  # Carga las firmas.
    firmas.pop(os.path.basename(ruta), None)  # Quita la entrada si existe.
    guardar_firmas(firmas)                    # Guarda las firmas.


def derivar_llave_archivo(password, salt):
    """Convierte una contrasena normal en una llave Fernet (PBKDF2 + base64)."""
    bruto = hashlib.pbkdf2_hmac(             # Deriva 32 bytes con PBKDF2-HMAC-SHA256.
        "sha256",                           # Algoritmo SHA-256.
        password.encode("utf-8"),           # Contrasena en bytes.
        salt,                               # Salt (16 bytes) de este archivo.
        ITER_ARCHIVO,                       # 100 000 iteraciones (como el Proyecto 1).
        dklen=32,                           # 32 bytes, longitud que exige Fernet.
    )
    return base64.urlsafe_b64encode(bruto)  # Codifica en base64 url-safe -> llave Fernet.


def archivo_ya_cifrado(datos):
    """Detecta si el contenido ya esta cifrado por este programa.

    Formato en disco: [salt de 16 bytes] + [token Fernet]. El token Fernet
    siempre empieza con 'gAAAAA', asi que revisamos los bytes 16 a 22.
    """
    return len(datos) >= 22 and datos[16:22] == b"gAAAAA"  # True si ya esta cifrado.


def cifrar_archivo(ruta, password):
    """Cifra un archivo EN EL MISMO lugar (no crea copias nuevas).

    Lee el archivo elegido, genera un salt, deriva la llave con la contrasena
    y reescribe el MISMO archivo con: salt + contenido cifrado.
    """
    if not os.path.exists(ruta):             # Si el archivo no existe...
        raise FileNotFoundError(f"No existe el archivo: {ruta}")  # ...error.

    with open(ruta, "rb") as archivo:        # Abre el archivo en binario lectura.
        datos = archivo.read()               # Lee todo el contenido.

    if archivo_ya_cifrado(datos):            # Si ya estaba cifrado...
        raise ValueError("El archivo ya esta cifrado.")  # ...evita doble cifrado.

    salt = secrets.token_bytes(16)           # Salt aleatorio de 16 bytes para este archivo.
    llave = derivar_llave_archivo(password, salt)  # Deriva la llave Fernet con la contrasena.
    token = Fernet(llave).encrypt(datos)     # Cifra (Fernet agrega HMAC = autenticado).

    with open(ruta, "wb") as archivo:        # Abre el MISMO archivo en binario escritura.
        archivo.write(salt + token)          # Escribe salt + cifrado (reemplaza el original).

    return ruta                              # Devuelve la misma ruta.


def descifrar_archivo(ruta, password):
    """Descifra un archivo EN EL MISMO lugar (no crea copias nuevas).

    Lee el archivo cifrado, separa el salt (16 bytes), re-deriva la llave con
    la contrasena y reescribe el MISMO archivo con el contenido original.
    """
    if not os.path.exists(ruta):             # Si el archivo no existe...
        raise FileNotFoundError(f"No existe el archivo: {ruta}")  # ...error.

    with open(ruta, "rb") as archivo:        # Abre el archivo en binario lectura.
        contenido = archivo.read()           # Lee todo el contenido.

    if not archivo_ya_cifrado(contenido):    # Si no esta cifrado por este programa...
        raise ValueError("El archivo no esta cifrado (o ya esta descifrado).")

    salt = contenido[:16]                    # Los primeros 16 bytes son el salt.
    token = contenido[16:]                   # El resto es el token cifrado.
    llave = derivar_llave_archivo(password, salt)  # Re-deriva la llave con la contrasena + salt.

    try:                                     # Intenta descifrar.
        datos = Fernet(llave).decrypt(token)  # Fernet verifica el HMAC y descifra.
    except InvalidToken:                     # Si la clave es mala o el archivo fue alterado...
        raise ValueError("Clave incorrecta o archivo manipulado.")

    with open(ruta, "wb") as archivo:        # Abre el MISMO archivo en binario escritura.
        archivo.write(datos)                 # Restaura el contenido original.

    return ruta                              # Devuelve la misma ruta.


# ====================================================================
#  SECCION 4 - GENERADOR DE CONTRASENAS SEGURAS  (AMBOS GRUPOS)
# ====================================================================
def generar_contrasena(longitud=16):
    """Genera una contrasena segura con al menos un caracter de cada tipo."""
    if longitud < LONGITUD_MINIMA:           # Si piden menos del minimo...
        longitud = LONGITUD_MINIMA           # ...se ajusta al minimo.

    todos = MINUSCULAS + MAYUSCULAS + DIGITOS + SIMBOLOS  # Todos los caracteres posibles.

    contrasena = [                           # Garantiza uno de cada tipo:
        secrets.choice(MINUSCULAS),          #   una minuscula.
        secrets.choice(MAYUSCULAS),          #   una mayuscula.
        secrets.choice(DIGITOS),             #   un digito.
        secrets.choice(SIMBOLOS),            #   un simbolo.
    ]
    contrasena += [secrets.choice(todos) for _ in range(longitud - 4)]  # Rellena el resto.

    secrets.SystemRandom().shuffle(contrasena)  # Mezcla para que no sea predecible.
    return "".join(contrasena)               # Devuelve la contrasena como texto.


def evaluar_fortaleza(contrasena):
    """Evalua si la contrasena es Debil, Media o Fuerte."""
    puntos = 0                               # Criterios cumplidos.
    if len(contrasena) >= 12:                # 12 o mas caracteres...
        puntos += 1                          # ...suma punto.
    if any(c in MINUSCULAS for c in contrasena):  # Tiene minuscula...
        puntos += 1                          # ...suma punto.
    if any(c in MAYUSCULAS for c in contrasena):  # Tiene mayuscula...
        puntos += 1                          # ...suma punto.
    if any(c in DIGITOS for c in contrasena):     # Tiene digito...
        puntos += 1                          # ...suma punto.
    if any(c in SIMBOLOS for c in contrasena):    # Tiene simbolo...
        puntos += 1                          # ...suma punto.

    if puntos <= 2:                          # 2 o menos...
        return "Debil"                       # ...debil.
    if puntos in (3, 4):                     # 3 o 4...
        return "Media"                       # ...media.
    return "Fuerte"                          # 5: fuerte.


# ====================================================================
#  SECCION 5 - ATAQUE VS DEFENSA  (AMBOS GRUPOS)
#  (Estas funciones DEVUELVEN texto para mostrarlo en la interfaz.)
# ====================================================================
def demo_1_hash_sin_salt():
    """ATAQUE: hash sin salt (MD5). DEFENSA: PBKDF2 con salt unico."""
    lineas = []                              # Lista de lineas de texto del reporte.
    lineas.append("=== DEMO 1: Hash sin salt vs PBKDF2 con salt ===")
    contrasena = "Panama123"                 # Contrasena de ejemplo.

    # MALA PRACTICA: MD5 sin salt -> misma entrada = mismo hash.
    h_a = hashlib.md5(contrasena.encode()).hexdigest()  # Hash MD5 del usuario A.
    h_b = hashlib.md5(contrasena.encode()).hexdigest()  # Hash MD5 del usuario B.
    lineas.append("[ATAQUE]  MD5 sin salt:")
    lineas.append(f"          Usuario A: {h_a}")
    lineas.append(f"          Usuario B: {h_b}")
    lineas.append("          -> Mismo hash. Vulnerable a tablas rainbow.")

    # DEFENSA: PBKDF2 con salt distinto -> hashes distintos.
    sa = secrets.token_bytes(16)             # Salt de A.
    sb = secrets.token_bytes(16)             # Salt de B.
    hs_a = derivar_hash(contrasena, sa).hex()  # Hash seguro de A.
    hs_b = derivar_hash(contrasena, sb).hex()  # Hash seguro de B.
    lineas.append("[DEFENSA] PBKDF2-HMAC-SHA256 con salt unico:")
    lineas.append(f"          Usuario A: {hs_a[:40]}...")
    lineas.append(f"          Usuario B: {hs_b[:40]}...")
    lineas.append("          -> Hashes distintos con la misma contrasena.")
    return "\n".join(lineas)                 # Une todo y lo devuelve como texto.


def demo_2_archivo_alterado():
    """ATAQUE: modificar un archivo cifrado. DEFENSA: integridad lo detecta."""
    lineas = []                              # Lineas del reporte.
    lineas.append("=== DEMO 2: Manipulacion de archivo vs integridad ===")
    ruta = os.path.join(CARPETA, "_demo_secreto.txt")  # Archivo temporal de la demo.
    clave_demo = "ClaveDemo123!"             # Contrasena de ejemplo para cifrar el archivo.

    with open(ruta, "w", encoding="utf-8") as f:  # Crea el archivo de prueba.
        f.write("Informacion confidencial de IstmoSec, S.A.")  # Contenido de ejemplo.

    cifrar_archivo(ruta, clave_demo)         # Cifra EN EL MISMO archivo (sin crear copias).
    lineas.append(f"[OK]      Archivo cifrado en el mismo lugar: {os.path.basename(ruta)}")

    # ATAQUE: alterar un byte del archivo cifrado.
    with open(ruta, "rb") as f:              # Abre el cifrado en binario.
        datos = bytearray(f.read())          # Lee como bytes modificables.
    datos[-1] = datos[-1] ^ 0x01             # Invierte un bit del ultimo byte (parte cifrada).
    with open(ruta, "wb") as f:              # Abre en escritura.
        f.write(datos)                       # Reescribe el contenido alterado.
    lineas.append("[ATAQUE]  Se modifico 1 byte del archivo cifrado.")

    # DEFENSA: al descifrar, la autenticacion (HMAC de Fernet) detecta el cambio.
    try:                                     # Intenta descifrar el archivo alterado.
        descifrar_archivo(ruta, clave_demo)  # Deberia fallar por la alteracion.
        lineas.append("[DEFENSA] (no deberia llegar aqui)")  # Caso que no ocurre.
    except Exception as e:                    # La excepcion confirma la deteccion.
        lineas.append(f"[DEFENSA] Al descifrar: {e}")  # Muestra el mensaje de error.
        lineas.append("          -> El cambio se detecta y se rechaza (HMAC de Fernet).")

    try:                                     # Limpia el archivo temporal.
        os.remove(ruta)                      # Elimina el archivo.
    except OSError:                          # Si falla...
        pass                                 # ...lo ignora.
    return "\n".join(lineas)                 # Devuelve el reporte como texto.


def demo_3_llave_hardcodeada():
    """ATAQUE: llave escrita en el codigo. DEFENSA: llave en .env."""
    lineas = []                              # Lineas del reporte.
    lineas.append("=== DEMO 3: Llave en el codigo vs variable de entorno ===")

    LLAVE_HARDCODEADA = "gAAAAABc...EJEMPLO_NO_USAR..."  # Llave de mentira (solo ilustrativa).
    lineas.append(f"[ATAQUE]  Llave escrita en el .py: {LLAVE_HARDCODEADA}")
    lineas.append("          -> Visible en el codigo y en el historial de Git.")

    if existe_llave():                       # Si ya existe la llave en .env...
        lineas.append("[DEFENSA] La llave real se carga desde .env (fuera del codigo).")
        lineas.append("          .env esta en .gitignore -> no se sube al repositorio.")
    else:                                    # Si no existe...
        generar_y_guardar_llave()            # ...la genera.
        lineas.append("[DEFENSA] Llave generada y guardada en .env (fuera del codigo).")
    return "\n".join(lineas)                 # Devuelve el reporte como texto.


def ejecutar_demos():
    """Ejecuta las 3 demostraciones y devuelve todo el texto junto."""
    partes = [                               # Llama a cada demo y guarda su texto.
        demo_1_hash_sin_salt(),              # Demo 1.
        demo_2_archivo_alterado(),           # Demo 2.
        demo_3_llave_hardcodeada(),          # Demo 3.
    ]
    return "\n\n".join(partes)               # Une las tres separadas por lineas en blanco.


# ====================================================================
#  SECCION 6 - INTERFAZ GRAFICA (Tkinter)
# ====================================================================
class FortinApp:
    """Clase principal de la aplicacion grafica (ventana del Fortin de Datos)."""

    def __init__(self, root):
        """Constructor: arma toda la ventana y sus pestanas."""
        self.root = root                          # Guarda la ventana principal.
        self.archivo_cifrar = None                # Ruta del archivo a cifrar/descifrar.
        self.archivo_verificar = None             # Ruta del archivo a verificar.

        self.root.title("Fortin de Datos - Proyecto #2")  # Titulo de la ventana.
        self.root.geometry("760x560")             # Tamano inicial de la ventana.
        self.root.configure(bg=FONDO)             # Color de fondo de la ventana.
        self.root.minsize(720, 520)               # Tamano minimo permitido.

        self._configurar_estilos()                # Aplica colores y estilos a los widgets.
        self._construir_encabezado()              # Crea la barra superior (titulo).
        self._construir_pestanas()                # Crea el cuaderno de pestanas.
        self._actualizar_estado_sesion()          # Muestra el estado inicial de la sesion.

    # ----------------------------------------------------------------
    #  Estilos visuales
    # ----------------------------------------------------------------
    def _configurar_estilos(self):
        """Define los estilos (colores, fuentes) de los componentes ttk."""
        estilo = ttk.Style()                      # Objeto de estilos de ttk.
        estilo.theme_use("clam")                  # Tema base que permite personalizar colores.

        estilo.configure("TNotebook", background=FONDO, borderwidth=0)  # Fondo del cuaderno.
        estilo.configure("TNotebook.Tab", padding=(14, 8),             # Espaciado de cada pestana.
                         font=("Segoe UI", 10, "bold"))                # Fuente de las pestanas.
        estilo.map("TNotebook.Tab",                                    # Color segun seleccion:
                   background=[("selected", TEAL), ("!selected", "#D8DEE4")],  # activa/inactiva.
                   foreground=[("selected", BLANCO), ("!selected", NAVY)])     # texto.

        estilo.configure("TFrame", background=BLANCO)                  # Fondo de los marcos.
        estilo.configure("TLabel", background=BLANCO, foreground=NAVY, # Etiquetas:
                         font=("Segoe UI", 10))                        # fuente normal.
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 12, "bold"),  # Estilo para titulos.
                         foreground=NAVY, background=BLANCO)
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"),    # Botones:
                         padding=6)                                    # espaciado interno.
        estilo.configure("Accent.TButton", background=TEAL,           # Boton de acento (teal).
                         foreground=BLANCO)
        estilo.map("Accent.TButton",                                  # Color al pasar el mouse:
                   background=[("active", TEAL_OSCURO)])
        estilo.configure("TEntry", padding=5)                         # Espaciado de los campos.
        estilo.configure("TLabelframe", background=BLANCO, foreground=NAVY)  # Marcos con titulo.
        estilo.configure("TLabelframe.Label", background=BLANCO, foreground=TEAL,  # Titulo del marco.
                         font=("Segoe UI", 10, "bold"))
        estilo.configure("TSpinbox", padding=4)                       # Espaciado del selector.

    # ----------------------------------------------------------------
    #  Encabezado
    # ----------------------------------------------------------------
    def _construir_encabezado(self):
        """Crea la barra navy superior con el titulo y el estado de sesion."""
        barra = tk.Frame(self.root, bg=NAVY, height=70)   # Marco navy del encabezado.
        barra.pack(fill="x")                              # Lo extiende a lo ancho.
        barra.pack_propagate(False)                       # Mantiene la altura fija.

        tk.Label(barra, text="FORTIN DE DATOS",           # Titulo principal.
                 bg=NAVY, fg=BLANCO,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=20, pady=10)

        tk.Label(barra, text="Proteccion de informacion en reposo",  # Subtitulo.
                 bg=NAVY, fg="#A8DADC",
                 font=("Segoe UI", 9)).pack(side="left", pady=10)

        self.lbl_sesion = tk.Label(barra, text="Sesion: invitado",   # Estado de la sesion.
                                   bg=NAVY, fg=BLANCO,
                                   font=("Segoe UI", 10, "bold"))
        self.lbl_sesion.pack(side="right", padx=20)       # A la derecha de la barra.

    # ----------------------------------------------------------------
    #  Pestanas
    # ----------------------------------------------------------------
    def _construir_pestanas(self):
        """Crea el cuaderno de pestanas y las llena con cada modulo."""
        cuaderno = ttk.Notebook(self.root)                # Contenedor de pestanas.
        cuaderno.pack(fill="both", expand=True, padx=12, pady=12)  # Lo expande en la ventana.

        # Crea un marco por cada pestana.
        tab_auth = ttk.Frame(cuaderno, padding=16)        # Pestana de autenticacion.
        tab_gen = ttk.Frame(cuaderno, padding=16)         # Pestana del generador.
        tab_cif = ttk.Frame(cuaderno, padding=16)         # Pestana de cifrado.
        tab_int = ttk.Frame(cuaderno, padding=16)         # Pestana de integridad.
        tab_llave = ttk.Frame(cuaderno, padding=16)       # Pestana de llave maestra.
        tab_demo = ttk.Frame(cuaderno, padding=16)        # Pestana de ataque/defensa.

        # Agrega cada marco al cuaderno con su titulo.
        cuaderno.add(tab_auth, text="Autenticacion")
        cuaderno.add(tab_gen, text="Generador")
        cuaderno.add(tab_cif, text="Cifrado")
        cuaderno.add(tab_int, text="Integridad")
        cuaderno.add(tab_llave, text="Llave maestra")
        cuaderno.add(tab_demo, text="Ataque/Defensa")

        # Llama al metodo que arma el contenido de cada pestana.
        self._tab_autenticacion(tab_auth)
        self._tab_generador(tab_gen)
        self._tab_cifrado(tab_cif)
        self._tab_integridad(tab_int)
        self._tab_llave(tab_llave)
        self._tab_demos(tab_demo)

    # --- Pestana 1: Autenticacion --------------------------------
    def _tab_autenticacion(self, tab):
        """Arma el formulario de registro e inicio de sesion."""
        ttk.Label(tab, text="Registro e inicio de sesion",   # Titulo de la pestana.
                  style="Titulo.TLabel").pack(anchor="w", pady=(0, 12))

        # --- Marco de registro ---
        marco_reg = ttk.Labelframe(tab, text="Registrar usuario", padding=12)  # Caja "Registrar".
        marco_reg.pack(fill="x", pady=6)                    # A lo ancho.

        ttk.Label(marco_reg, text="Usuario:").grid(row=0, column=0, sticky="w", pady=4)  # Etiqueta.
        self.reg_usuario = ttk.Entry(marco_reg, width=28)   # Campo de usuario.
        self.reg_usuario.grid(row=0, column=1, padx=8, pady=4)  # Posicion del campo.

        ttk.Label(marco_reg, text="Contrasena:").grid(row=1, column=0, sticky="w", pady=4)  # Etiqueta.
        self.reg_clave = ttk.Entry(marco_reg, width=28, show="*")  # Campo de clave (oculta con *).
        self.reg_clave.grid(row=1, column=1, padx=8, pady=4)  # Posicion.

        ttk.Button(marco_reg, text="Registrar", style="Accent.TButton",  # Boton registrar.
                   command=self.accion_registrar).grid(row=2, column=1, sticky="e", pady=6)

        # --- Marco de inicio de sesion ---
        marco_log = ttk.Labelframe(tab, text="Iniciar sesion", padding=12)  # Caja "Iniciar sesion".
        marco_log.pack(fill="x", pady=6)                    # A lo ancho.

        ttk.Label(marco_log, text="Usuario:").grid(row=0, column=0, sticky="w", pady=4)  # Etiqueta.
        self.log_usuario = ttk.Entry(marco_log, width=28)   # Campo de usuario.
        self.log_usuario.grid(row=0, column=1, padx=8, pady=4)  # Posicion.

        ttk.Label(marco_log, text="Contrasena:").grid(row=1, column=0, sticky="w", pady=4)  # Etiqueta.
        self.log_clave = ttk.Entry(marco_log, width=28, show="*")  # Campo de clave (oculta).
        self.log_clave.grid(row=1, column=1, padx=8, pady=4)  # Posicion.

        botones = ttk.Frame(marco_log)                      # Marco para alinear dos botones.
        botones.grid(row=2, column=1, sticky="e", pady=6)   # Posicion.
        ttk.Button(botones, text="Iniciar sesion", style="Accent.TButton",  # Boton login.
                   command=self.accion_login).pack(side="left", padx=4)
        ttk.Button(botones, text="Cerrar sesion",           # Boton cerrar sesion.
                   command=self.accion_logout).pack(side="left", padx=4)

    # --- Pestana 2: Generador ------------------------------------
    def _tab_generador(self, tab):
        """Arma el generador de contrasenas seguras."""
        ttk.Label(tab, text="Generador de contrasenas seguras",  # Titulo.
                  style="Titulo.TLabel").pack(anchor="w", pady=(0, 12))

        fila = ttk.Frame(tab)                               # Fila para longitud + boton.
        fila.pack(fill="x", pady=6)                         # A lo ancho.
        ttk.Label(fila, text="Longitud:").pack(side="left")  # Etiqueta.
        self.gen_longitud = ttk.Spinbox(fila, from_=8, to=64, width=6)  # Selector de longitud.
        self.gen_longitud.set(16)                           # Valor por defecto: 16.
        self.gen_longitud.pack(side="left", padx=8)         # Posicion.
        ttk.Button(fila, text="Generar", style="Accent.TButton",  # Boton generar.
                   command=self.accion_generar).pack(side="left", padx=8)

        self.gen_resultado = ttk.Entry(tab, width=50, font=("Consolas", 11))  # Campo del resultado.
        self.gen_resultado.pack(fill="x", pady=10)          # A lo ancho.

        fila2 = ttk.Frame(tab)                              # Fila para fortaleza + copiar.
        fila2.pack(fill="x")                                # A lo ancho.
        self.gen_fortaleza = ttk.Label(fila2, text="Fortaleza: -")  # Etiqueta de fortaleza.
        self.gen_fortaleza.pack(side="left")                # A la izquierda.
        ttk.Button(fila2, text="Copiar",                    # Boton copiar al portapapeles.
                   command=self.accion_copiar).pack(side="right")

    # --- Pestana 3: Cifrado --------------------------------------
    def _tab_cifrado(self, tab):
        """Arma el cifrado/descifrado de archivos EN EL MISMO lugar (requiere sesion)."""
        ttk.Label(tab, text="Cifrar / Descifrar archivos",  # Titulo.
                  style="Titulo.TLabel").pack(anchor="w", pady=(0, 8))

        ttk.Label(tab, text="El archivo se cifra y descifra EN EL MISMO lugar (no se crean copias).",
                  foreground=TEAL).pack(anchor="w")          # Aviso del comportamiento in-place.
        ttk.Label(tab, text="Requiere iniciar sesion en la pestana 'Autenticacion'.",  # Aviso.
                  foreground=TEAL).pack(anchor="w", pady=(0, 8))

        ttk.Button(tab, text="Seleccionar archivo...",      # Boton para elegir archivo.
                   command=self.seleccionar_archivo_cifrar).pack(anchor="w", pady=4)
        self.cif_ruta = ttk.Label(tab, text="Ningun archivo seleccionado.")  # Muestra la ruta.
        self.cif_ruta.pack(anchor="w", pady=4)              # Posicion.

        fila_clave = ttk.Frame(tab)                         # Fila para la contrasena del archivo.
        fila_clave.pack(anchor="w", pady=6)                 # Posicion.
        ttk.Label(fila_clave, text="Contrasena del archivo:").pack(side="left")  # Etiqueta.
        self.cif_clave = ttk.Entry(fila_clave, width=28, show="*")  # Campo de clave (oculta).
        self.cif_clave.pack(side="left", padx=8)            # Posicion.

        fila = ttk.Frame(tab)                               # Fila de botones cifrar/descifrar.
        fila.pack(anchor="w", pady=10)                      # Posicion.
        ttk.Button(fila, text="Cifrar", style="Accent.TButton",  # Boton cifrar.
                   command=self.accion_cifrar).pack(side="left", padx=4)
        ttk.Button(fila, text="Descifrar",                  # Boton descifrar.
                   command=self.accion_descifrar).pack(side="left", padx=4)

        self.cif_resultado = ttk.Label(tab, text="", font=("Segoe UI", 10, "bold"))  # Mensaje resultado.
        self.cif_resultado.pack(anchor="w", pady=8)         # Posicion.

    # --- Pestana 4: Integridad -----------------------------------
    def _tab_integridad(self, tab):
        """Arma la firma y verificacion de integridad (HMAC-SHA256) de un archivo."""
        ttk.Label(tab, text="Firmar / Verificar integridad",  # Titulo.
                  style="Titulo.TLabel").pack(anchor="w", pady=(0, 8))

        ttk.Label(tab, text="Genera un sello HMAC-SHA256 del archivo y detecta si fue alterado.",
                  foreground=TEAL).pack(anchor="w", pady=(0, 8))  # Explicacion.

        ttk.Button(tab, text="Seleccionar archivo...",      # Boton para elegir archivo.
                   command=self.seleccionar_archivo_verificar).pack(anchor="w", pady=4)
        self.int_ruta = ttk.Label(tab, text="Ningun archivo seleccionado.")  # Muestra la ruta.
        self.int_ruta.pack(anchor="w", pady=4)              # Posicion.

        fila_clave = ttk.Frame(tab)                         # Fila para la contrasena de firma.
        fila_clave.pack(anchor="w", pady=6)                 # Posicion.
        ttk.Label(fila_clave, text="Contrasena de firma:").pack(side="left")  # Etiqueta.
        self.int_clave = ttk.Entry(fila_clave, width=28, show="*")  # Campo de clave (oculta).
        self.int_clave.pack(side="left", padx=8)            # Posicion.

        fila = ttk.Frame(tab)                               # Fila con dos botones.
        fila.pack(anchor="w", pady=10)                      # Posicion.
        ttk.Button(fila, text="Firmar archivo",             # Boton: genera el sello HMAC.
                   command=self.accion_firmar).pack(side="left", padx=4)
        ttk.Button(fila, text="Verificar integridad", style="Accent.TButton",  # Boton verificar.
                   command=self.accion_verificar).pack(side="left", padx=4)

        self.int_resultado = ttk.Label(tab, text="", font=("Segoe UI", 11, "bold"))  # Resultado.
        self.int_resultado.pack(anchor="w", pady=8)         # Posicion.

    # --- Pestana 5: Llave maestra --------------------------------
    def _tab_llave(self, tab):
        """Arma la gestion de la llave maestra."""
        ttk.Label(tab, text="Llave maestra",                # Titulo.
                  style="Titulo.TLabel").pack(anchor="w", pady=(0, 12))

        self.llave_estado = ttk.Label(tab, text="")         # Etiqueta del estado de la llave.
        self.llave_estado.pack(anchor="w", pady=6)          # Posicion.
        self._actualizar_estado_llave()                     # Muestra el estado actual.

        ttk.Button(tab, text="Generar nueva llave maestra", style="Accent.TButton",  # Boton.
                   command=self.accion_generar_llave).pack(anchor="w", pady=8)

        ttk.Label(tab, text="La llave se guarda en el archivo .env, nunca en el codigo.",  # Nota.
                  foreground=TEAL).pack(anchor="w", pady=6)

    # --- Pestana 6: Ataque/Defensa -------------------------------
    def _tab_demos(self, tab):
        """Arma la pestana que ejecuta y muestra las demostraciones."""
        ttk.Label(tab, text="Demostracion: Ataque vs Defensa",  # Titulo.
                  style="Titulo.TLabel").pack(anchor="w", pady=(0, 8))

        ttk.Button(tab, text="Ejecutar demostraciones", style="Accent.TButton",  # Boton ejecutar.
                   command=self.accion_demos).pack(anchor="w", pady=6)

        self.demo_salida = scrolledtext.ScrolledText(tab, height=16, width=80,  # Area de texto.
                                                     font=("Consolas", 9),
                                                     bg="#0F1B2D", fg="#D8DEE4")  # Estilo "consola".
        self.demo_salida.pack(fill="both", expand=True, pady=8)  # Ocupa el espacio disponible.

    # ----------------------------------------------------------------
    #  ACCIONES (manejadores de los botones)
    # ----------------------------------------------------------------
    def accion_registrar(self):
        """Registra un usuario con los datos del formulario."""
        usuario = self.reg_usuario.get().strip()  # Lee el usuario del campo.
        clave = self.reg_clave.get()              # Lee la contrasena del campo.
        if not usuario:                           # Si el usuario esta vacio...
            messagebox.showwarning("Atencion", "El usuario no puede estar vacio.")  # Avisa.
            return                                # Sale.
        if len(clave) < 8:                        # Si la clave es corta...
            messagebox.showwarning("Atencion", "La contrasena debe tener al menos 8 caracteres.")
            return                                # Sale.
        if registrar_usuario(usuario, clave):     # Intenta registrar.
            messagebox.showinfo("Exito", f"Usuario '{usuario}' registrado.")  # Confirma.
            self.reg_usuario.delete(0, "end")     # Limpia el campo usuario.
            self.reg_clave.delete(0, "end")       # Limpia el campo clave.
        else:                                     # Si ya existia...
            messagebox.showerror("Error", "Ese usuario ya existe.")  # Avisa.

    def accion_login(self):
        """Inicia sesion con los datos del formulario."""
        usuario = self.log_usuario.get().strip()  # Lee el usuario.
        clave = self.log_clave.get()              # Lee la clave.
        if verificar_login(usuario, clave):       # Si las credenciales son correctas...
            sesion["usuario"] = usuario.strip().lower()  # Guarda la sesion.
            self._actualizar_estado_sesion()      # Actualiza el estado en pantalla.
            messagebox.showinfo("Bienvenido", f"Sesion iniciada como '{usuario}'.")  # Confirma.
            self.log_clave.delete(0, "end")       # Limpia la clave.
        else:                                     # Si son incorrectas...
            messagebox.showerror("Error", "Credenciales incorrectas.")  # Avisa.

    def accion_logout(self):
        """Cierra la sesion actual."""
        sesion["usuario"] = None                  # Borra el usuario de la sesion.
        self._actualizar_estado_sesion()          # Actualiza el estado en pantalla.
        messagebox.showinfo("Sesion", "Sesion cerrada.")  # Confirma.

    def accion_generar(self):
        """Genera una contrasena segura y la muestra."""
        try:                                      # Intenta leer la longitud.
            longitud = int(self.gen_longitud.get())  # Convierte el valor a numero.
        except ValueError:                        # Si no es un numero valido...
            longitud = 16                         # ...usa 16 por defecto.
        clave = generar_contrasena(longitud)      # Genera la contrasena.
        self.gen_resultado.delete(0, "end")       # Limpia el campo del resultado.
        self.gen_resultado.insert(0, clave)       # Muestra la contrasena generada.
        self.gen_fortaleza.config(text=f"Fortaleza: {evaluar_fortaleza(clave)}")  # Muestra fortaleza.

    def accion_copiar(self):
        """Copia la contrasena generada al portapapeles."""
        clave = self.gen_resultado.get()          # Lee la contrasena mostrada.
        if clave:                                 # Si hay algo que copiar...
            self.root.clipboard_clear()           # Limpia el portapapeles.
            self.root.clipboard_append(clave)     # Copia la contrasena.
            messagebox.showinfo("Copiado", "Contrasena copiada al portapapeles.")  # Confirma.

    def seleccionar_archivo_cifrar(self):
        """Abre el explorador para elegir el archivo a cifrar/descifrar."""
        ruta = filedialog.askopenfilename()       # Muestra el dialogo de seleccion.
        if ruta:                                  # Si el usuario eligio un archivo...
            self.archivo_cifrar = ruta            # Guarda la ruta.
            self.cif_ruta.config(text=ruta)       # La muestra en pantalla.

    def accion_cifrar(self):
        """Cifra el archivo seleccionado EN EL MISMO lugar (requiere sesion)."""
        if sesion["usuario"] is None:             # Si no hay sesion iniciada...
            messagebox.showwarning("Atencion", "Debes iniciar sesion primero.")  # Avisa.
            return                                # Sale.
        if not self.archivo_cifrar:               # Si no hay archivo seleccionado...
            messagebox.showwarning("Atencion", "Selecciona un archivo primero.")  # Avisa.
            return                                # Sale.
        clave = self.cif_clave.get()              # Lee la contrasena del archivo.
        if len(clave) < 8:                        # Si la contrasena es corta...
            messagebox.showwarning("Atencion", "La contrasena debe tener al menos 8 caracteres.")
            return                                # Sale.
        try:                                      # Intenta cifrar.
            cifrar_archivo(self.archivo_cifrar, clave)  # Cifra EN EL MISMO archivo.
            self.cif_resultado.config(text="Archivo cifrado en su lugar (sin crear copias).",
                                      foreground=VERDE_OK)        # Mensaje en verde.
        except Exception as e:                    # Si hay error...
            self.cif_resultado.config(text=f"Error: {e}", foreground=ROJO_ERR)  # Lo muestra en rojo.

    def accion_descifrar(self):
        """Descifra el archivo seleccionado EN EL MISMO lugar (requiere sesion)."""
        if sesion["usuario"] is None:             # Si no hay sesion...
            messagebox.showwarning("Atencion", "Debes iniciar sesion primero.")  # Avisa.
            return                                # Sale.
        if not self.archivo_cifrar:               # Si no hay archivo...
            messagebox.showwarning("Atencion", "Selecciona un archivo primero.")  # Avisa.
            return                                # Sale.
        clave = self.cif_clave.get()              # Lee la contrasena del archivo.
        if not clave:                             # Si no escribio contrasena...
            messagebox.showwarning("Atencion", "Escribe la contrasena del archivo.")  # Avisa.
            return                                # Sale.
        try:                                      # Intenta descifrar.
            descifrar_archivo(self.archivo_cifrar, clave)  # Descifra EN EL MISMO archivo.
            self.cif_resultado.config(text="Archivo descifrado en su lugar (mismo archivo).",
                                      foreground=VERDE_OK)        # Mensaje en verde.
        except Exception as e:                    # Si hay error (alteracion, clave mala)...
            self.cif_resultado.config(text=f"Error: {e}", foreground=ROJO_ERR)  # Lo muestra en rojo.

    def seleccionar_archivo_verificar(self):
        """Abre el explorador para elegir el archivo a verificar."""
        ruta = filedialog.askopenfilename()       # Dialogo de seleccion.
        if ruta:                                  # Si eligio archivo...
            self.archivo_verificar = ruta         # Guarda la ruta.
            self.int_ruta.config(text=ruta)       # La muestra.

    def accion_firmar(self):
        """Genera la firma HMAC del archivo seleccionado con la contrasena dada."""
        if not self.archivo_verificar:            # Si no hay archivo...
            messagebox.showwarning("Atencion", "Selecciona un archivo primero.")  # Avisa.
            return                                # Sale.
        clave = self.int_clave.get()              # Lee la contrasena de firma.
        if not clave:                             # Si no escribio contrasena...
            messagebox.showwarning("Atencion", "Escribe la contrasena de firma.")  # Avisa.
            return                                # Sale.
        try:                                      # Intenta firmar.
            firmar_archivo(self.archivo_verificar, clave)  # Calcula y guarda el HMAC.
            self.int_resultado.config(text="Firma HMAC generada y guardada.",  # Mensaje.
                                      foreground=VERDE_OK)  # En verde.
        except Exception as e:                    # Si hay error...
            self.int_resultado.config(text=f"Error: {e}", foreground=ROJO_ERR)  # En rojo.

    def accion_verificar(self):
        """Verifica la firma HMAC del archivo (detecta si fue alterado)."""
        if not self.archivo_verificar:            # Si no hay archivo...
            messagebox.showwarning("Atencion", "Selecciona un archivo primero.")  # Avisa.
            return                                # Sale.
        clave = self.int_clave.get()              # Lee la contrasena de firma.
        if not clave:                             # Si no escribio contrasena...
            messagebox.showwarning("Atencion", "Escribe la contrasena de firma.")  # Avisa.
            return                                # Sale.
        if verificar_firma(self.archivo_verificar, clave):  # Si la firma coincide...
            self.int_resultado.config(text="INTACTO: la firma coincide, el archivo no fue alterado.",
                                      foreground=VERDE_OK)        # En verde.
        else:                                     # Si no coincide, no hay firma o la clave es mala...
            self.int_resultado.config(text="ALTERADO, sin firma registrada o clave incorrecta.",
                                      foreground=ROJO_ERR)        # En rojo.

    def accion_generar_llave(self):
        """Genera una nueva llave maestra tras confirmar."""
        if existe_llave():                        # Si ya existe una llave...
            ok = messagebox.askyesno("Confirmar",  # Pide confirmacion.
                                     "Ya existe una llave. Generar una NUEVA reemplaza la anterior. Continuar?")
            if not ok:                            # Si dice que no...
                return                            # ...sale.
        generar_llave_maestra()                   # Genera y guarda la nueva llave.
        self._actualizar_estado_llave()           # Actualiza el estado mostrado.
        messagebox.showinfo("Llave", "Llave maestra generada y guardada en .env.")  # Confirma.

    def accion_demos(self):
        """Ejecuta las demostraciones y muestra el resultado en el area de texto."""
        texto = ejecutar_demos()                  # Obtiene el reporte completo.
        self.demo_salida.delete("1.0", "end")     # Limpia el area de texto.
        self.demo_salida.insert("1.0", texto)     # Inserta el reporte.

    # ----------------------------------------------------------------
    #  Utilidades de actualizacion de la interfaz
    # ----------------------------------------------------------------
    def _actualizar_estado_sesion(self):
        """Actualiza la etiqueta que muestra el usuario con sesion."""
        usuario = sesion["usuario"] or "invitado"  # Usuario actual o "invitado".
        self.lbl_sesion.config(text=f"Sesion: {usuario}")  # Lo muestra en el encabezado.

    def _actualizar_estado_llave(self):
        """Actualiza la etiqueta del estado de la llave maestra."""
        if existe_llave():                        # Si existe la llave...
            self.llave_estado.config(text="Estado: ya existe una llave maestra en .env.",
                                     foreground=VERDE_OK)  # Mensaje en verde.
        else:                                     # Si no existe...
            self.llave_estado.config(text="Estado: aun no hay llave maestra.",
                                     foreground=ROJO_ERR)  # Mensaje en rojo.


# ====================================================================
#  PUNTO DE ENTRADA DEL PROGRAMA
# ====================================================================
def main():
    """Crea la ventana principal y arranca la aplicacion grafica."""
    root = tk.Tk()                  # Crea la ventana raiz de Tkinter.
    app = FortinApp(root)          # Construye la aplicacion sobre esa ventana.
    root.mainloop()                # Bucle principal: mantiene la ventana abierta.


# Esta condicion es verdadera solo si se ejecuta este archivo directamente.
if __name__ == "__main__":          # Punto de entrada.
    main()                          # Lanza la interfaz grafica.
