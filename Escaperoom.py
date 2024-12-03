import random
import re
import json
import os
from readchar import readkey, key
import threading
import time
from colorama import Fore, Back, Style, init

init(autoreset=True)

# Constantes
TERRENO = " "
PERSONAJE = "O"
CANDADO = "$"
PISTA = "#"
PUNTOS_INICIALES = 1000
COSTO_PISTA = 100
PUNTOS_DESAFIO = 500
PUNTOS_MOVIMIENTO = 10

def vaciar_consola():
    """
    Limpia la consola de manera compatible con Windows y Unix/Mac.

    Returns:
        None
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def cargar_archivo_json(nombre_archivo):
    """
    Carga y lee un archivo JSON desde la carpeta Data.

    Args:
        nombre_archivo (str): Nombre del archivo JSON a cargar

    Returns:
        dict: Contenido del archivo JSON o diccionario vacio si hay error
    """
    try:
        ruta_archivo = os.path.join(os.getcwd(), "Data", nombre_archivo)
        with open(ruta_archivo, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(Fore.RED + f"Error: No se encuentra el archivo {nombre_archivo}")
        return {}
    except json.JSONDecodeError:
        print(Fore.RED + f"Error: El archivo {nombre_archivo} tiene un formato invalido.")
        return {}
    except Exception as e:
        print(Fore.RED + f"Error inesperado: {e}")
        return {}

def guardar_archivo_json(nombre_archivo, datos):
    """
    Guarda datos en un archivo JSON en la carpeta Data.

    Args:
        nombre_archivo (str): Nombre del archivo donde guardar los datos
        datos (dict): Datos a guardar en formato JSON

    Returns:
        bool: True si se guardo correctamente, False si hubo error
    """
    try:
        ruta_archivo = os.path.join(os.getcwd(), "Data", nombre_archivo)
        with open(ruta_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)
        return True
    except Exception as e:
        print(Fore.RED + f"Error al guardar {nombre_archivo}: {e}")
        return False

def generar_terreno(mapa, altura_min, altura_max, ancho_min, ancho_max):
    """
    Genera el terreno base del mapa con dimensiones aleatorias dentro de los rangos especificados.

    Args:
        mapa (list): Lista vacia donde se generara el terreno
        altura_min (int): Altura minima del mapa
        altura_max (int): Altura maxima del mapa
        ancho_min (int): Ancho minimo del mapa
        ancho_max (int): Ancho maximo del mapa

    Returns:
        None: Modifica el mapa directamente
    """
    alto_del_mapa = random.randint(altura_min,altura_max)
    ancho_minimo_del_mapa = random.randint(ancho_min,ancho_max) 

    for _ in range(alto_del_mapa):
        mapa.append([TERRENO for _ in range(ancho_minimo_del_mapa)])
        
def generar_objeto(mapa, objeto, cantidad):
    """
    Genera objetos en posiciones aleatorias del mapa.

    Args:
        mapa (list): Matriz que representa el mapa del juego
        objeto (str): Caracter que representa el objeto a generar
        cantidad (int): Cantidad de objetos a generar

    Returns:
        None: Modifica el mapa directamente
    """

    columna_spawn = random.randint(0,len(mapa)-1) 
    fila_spawn = random.randint(0,len(mapa[columna_spawn])-1)
    for _ in range(cantidad):
        while(mapa[columna_spawn][fila_spawn] != TERRENO): 
            columna_spawn = random.randint(0,len(mapa)-1) 
            fila_spawn = random.randint(0,len(mapa[columna_spawn])-1)
        mapa[columna_spawn][fila_spawn] = objeto

def generar_mapa(altura_min,altura_max,ancho_min,ancho_max):
    """
    Genera un mapa completo del juego con todos sus elementos.

    Args:
        altura_min (int): Altura minima del mapa
        altura_max (int): Altura maxima del mapa
        ancho_min (int): Ancho minimo del mapa
        ancho_max (int): Ancho maximo del mapa

    Returns:
        list: Matriz que representa el mapa generado con todos sus elementos
    """
    mapa = []
    generar_terreno(mapa,altura_min,altura_max,ancho_min,ancho_max)
    for i in [PERSONAJE, CANDADO, PISTA]:
        if(i == PERSONAJE):
            generar_objeto(mapa,i,1)
        else:
            generar_objeto(mapa,i,2) 
        
    return mapa

def renderizar_mapa(mapa):
    """
    Muestra el mapa en la consola.

    Args:
        mapa (list): Matriz que representa el mapa a mostrar

    Returns:
        None
    """
    for fila in mapa:
        print(Fore.YELLOW + str(fila))
        
def mostrar_tiempo(timer):
    """
    Muestra el tiempo transcurrido.

    Args:
        timer (Timer): El temporizador actual del juego.

    Returns:
        None
    """
    tiempo = timer.obtener_tiempo()
    print()
    print(Fore.BLUE + f"Tiempo transcurrido: {tiempo} segundos")
    print()

def leer_accion():
    """
    Lee y valida la entrada del usuario para movimientos y acciones.

    Returns:
        str: Accion validada ('w', 'a', 's', 'd', 'menu')
    """
    while True:
        k = readkey()
        if k == key.UP or k.lower() == 'w':
            return 'w'
        elif k == key.LEFT or k.lower() == 'a':
            return 'a'
        elif k == key.DOWN or k.lower() == 's':
            return 's'
        elif k == key.RIGHT or k.lower() == 'd':
            return 'd'
        elif k.lower() == 'm':
            return 'menu'

def validar_movimiento(mapa, posicion_actual, accion):
    """
    Verifica si un movimiento es valido dentro del mapa.

    Args:
        mapa (list): Matriz que representa el mapa
        posicion_actual (list): Coordenadas actuales [x, y]
        accion (str): Direccion del movimiento ('w', 'a', 's', 'd')

    Returns:
        bool: True si el movimiento es valido, False si no lo es
    """

    filas = len(mapa)
    columnas = len(mapa[0]) if filas > 0 else 0
    
    nueva_posicion = list(posicion_actual) 

    if accion.lower() == "w":
        nueva_posicion[0] -= 1
    elif accion.lower() == "s":
        nueva_posicion[0] += 1
    elif accion.lower() == "a":
        nueva_posicion[1] -= 1
    elif accion.lower() == "d":
        nueva_posicion[1] += 1
    
    if nueva_posicion[0] < 0 or nueva_posicion[0] >= filas or nueva_posicion[1] < 0 or nueva_posicion[1] >= columnas:
        return False
    return True

def get_indice_objeto(mapa,objeto):
    """
    Encuentra las coordenadas de un objeto especifico en el mapa.

    Args:
        mapa (list): Matriz que representa el mapa
        objeto (str): Caracter del objeto a buscar

    Returns:
        list: Lista con las coordenadas [y, x] donde se encuentra el objeto
    """
    indices = []
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if(mapa[y][x] == objeto):
                indices.append(y)
                indices.append(x)
    return indices

def mover_objeto(mapa,x,y,objeto):
    """
    Mueve un objeto en el mapa segun las coordenadas especificadas.

    Args:
        mapa (list): Matriz que representa el mapa
        x (int): Desplazamiento en el eje x
        y (int): Desplazamiento en el eje y
        objeto (str): Caracter del objeto a mover

    Returns:
        None: Modifica el mapa directamente
    """
    coordenadas_objeto = get_indice_objeto(mapa,objeto)
    mapa[coordenadas_objeto[0]][coordenadas_objeto[1]] = TERRENO
    mapa[coordenadas_objeto[0]+y*(-1)][coordenadas_objeto[1]+x] = objeto

def accion_personaje(mapa,accion): 
    """
    Ejecuta el movimiento del personaje segun la accion especificada.

    Args:
        mapa (list): Matriz que representa el mapa
        accion (str): Direccion del movimiento ('w', 'a', 's', 'd')

    Returns:
        None: Modifica el mapa directamente
    """
    if  (accion == "w"):
        mover_objeto(mapa,0,1,PERSONAJE)
    elif(accion == "s"):
        mover_objeto(mapa,0,-1,PERSONAJE) 
    elif(accion == "a"):
        mover_objeto(mapa,-1,0,PERSONAJE)
    elif(accion == "d"):
        mover_objeto(mapa,1,0,PERSONAJE)

def pedir_user_name(jugador_numero=0):
    """
    Solicita y valida el nombre de usuario.

    Args:
        jugador_numero (int): Numero de jugador (0 para un solo jugador)

    Returns:
        str: Nombre de usuario validado
    """
    patron = r"^[a-zA-Z]{3,9}$"
    username = input(Fore.GREEN + f"Jugador, ingrese un nombre de usuario (3-9 caracteres, sin numeros o caracteres especiales): ")
    nombre_valido = re.match(patron, username)

    while nombre_valido is None:
        print(Fore.RED + f"Nombre no valido. Intentelo de nuevo.") 
        username = input(Fore.GREEN + f"Jugador, por favor, ingrese un nombre de usuario: ")
        nombre_valido = re.match(patron, username)
    return username

def menu_principal(user):
    """
    Muestra el menu principal del juego con estilo y efectos visuales.

    Args:
        user (str): Nombre del usuario actual

    Returns:
        None
    """
    bienvenida = """
     __    __       ___       _______   _______     _______.  ______     ___      .______    _______ 
    |  |  |  |     /   \     |       \ |   ____|   /       | /      |   /   \     |   _  \  |   ____|
    |  |  |  |    /  ^  \    |  .--.  ||  |__     |   (----`|  ,----'  /  ^  \    |  |_)  | |  |__   
    |  |  |  |   /  /_\  \   |  |  |  ||   __|     \   \    |  |      /  /_\  \   |   ___/  |   __|  
    |  `--'  |  /  _____  \  |  '--'  ||  |____.----)   |   |  `----./  _____  \  |  |      |  |____ 
     \______/  /__/     \__\ |_______/ |_______|_______/     \______/__/     \__\ | _|      |_______|
                                                                                                  
    """
    print(Fore.YELLOW + Style.BRIGHT + bienvenida)
    usuario_formateado = Fore.CYAN + Style.BRIGHT + f"{user.upper()}"
    print(Fore.GREEN + f"🌟🌟 BIENVENIDO, {usuario_formateado}! 🌟🌟")
    
    print(Fore.WHITE + Style.BRIGHT + "=" * 60)

    opciones = [
        ("1", "Comenzar Juego ▶"), 
        ("2", "Ranking de Puntos 🔝"),
        ("3", "Como Jugar 📕"),
        ("4", "Salir 👋🏻")
    ]
    
    for numero, descripcion in opciones:
        print(f"{numero}. {descripcion}") 

    print(Fore.WHITE + Style.BRIGHT + "=" * 60)
    print(Fore.MAGENTA + Style.BRIGHT + "¡Elige tu opcion y empeza la aventura! ✨🚀")
    print(Fore.LIGHTGREEN_EX + "TE RECOMENDAMOS LEER LAS INSTRUCCIONES ANTES DE ARRANCAR.😉")
    print() 
    
def generar_user(username):
    """
    Genera un nuevo registro de usuario en el repositorio.

    Args:
        username (str): Nombre de usuario a registrar

    Returns:
        None
    """
    user_repository = cargar_archivo_json("user_repository.json")
    if not user_repository:
        user_repository = []

    while any(user['username'] == username for user in user_repository):
        print(Fore.RED + f"😳El nombre de usuario '{Fore.CYAN + username + Fore.RED}' ya esta en uso. Intente con otro.")
        username = pedir_user_name()
    
    nuevo_usuario = {
        "username": username,
        "id": generar_id(user_repository),
        "puntos": 0
    }
    user_repository.append(nuevo_usuario)
    
    if guardar_archivo_json("user_repository.json", user_repository):
        print(Fore.GREEN + f"😎 Usuario '{Fore.CYAN + username + Fore.GREEN}' registrado con exito.")
    else:
        print(Fore.RED + "Error al registrar el usuario.")

def generar_id(user_repository):
    """
    Genera un nuevo ID para un usuario basado en el ultimo ID registrado.

    Args:
        user_repository (list): Lista de usuarios registrados

    Returns:
        int: Nuevo ID generado
    """

    id = 0
    if(len(user_repository) != 0):
        ultimo = len(user_repository)-1 
        id = user_repository[ultimo]['id'] + 1
    return id

def pedir_opcion(min, max):
    """
    Solicita y valida una opcion numerica dentro de un rango.

    Args:
        min (int): Valor minimo aceptado
        max (int): Valor maximo aceptado

    Returns:
        int: Opcion validada dentro del rango especificado
    """
    while True:
        try:
            opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
            if min <= opcion <= max:
                print()
                return opcion
            else:
                print(Fore.RED + "Error, la opcion ingresada no esta en el rango valido.")
        except ValueError:
            print(Fore.RED + "Error, debe ingresar un numero.")

def mostrar_dificultades():
    """
    Muestra en pantalla los niveles de dificultad disponibles con estilo.

    Returns:
        None
    """
    print(Fore.CYAN + Style.BRIGHT + "=== COMENZAR JUEGO ===")
    print()
    print(Fore.YELLOW + Style.BRIGHT + "=== SELECCIONA UN NIVEL DE DIFICULTAD ===")
    
    print("1. 🟢 Facil: Para los que comienzan la aventura!")
    print("2. 🔵 Normal: ¡Un desafio equilibrado!")
    print("3. 🔴 Dificil: ¡Solo para los mas valientes!")
    print()

def nivel_de_dificultad():
    """
    Permite al usuario seleccionar un nivel de dificultad y devuelve las tematicas correspondientes con un formato atractivo.

    Returns:
        list: Lista de tematicas disponibles para la dificultad seleccionada
    """
    mostrar_dificultades()
    opcion = pedir_opcion(1, 3)

    facil = ["Breaking Bad", "Muerte Anunciada"]
    intermedio = ["Psiquiatrico", "La Casa de Papel"]
    dificil = ["Sherlock Holmes", "Mision Gubernamental"]

    if opcion == 1:
        dificultad = facil
        print(Fore.GREEN + Style.BRIGHT + "Elegiste el nivel facil! 🌱")
    elif opcion == 2:
        dificultad = intermedio
        print(Fore.BLUE + Style.BRIGHT + "¡Elegiste el nivel normal! 🚀")
    elif opcion == 3:
        dificultad = dificil
        print(Fore.RED + Style.BRIGHT + "¡Elegiste el nivel dificil! 🔥")
    return dificultad

def elegir_tematica():
    """
    Permite al usuario seleccionar una tematica segun la dificultad elegida con un formato atractivo.

    Returns:
        str: Nombre de la tematica seleccionada
    """
    dificultad = nivel_de_dificultad()
    print(Fore.YELLOW + Style.BRIGHT + "\n=== SELECCIONA UNA TEMATICA ===")

    for i, tematica in enumerate(dificultad, 1):
        print(f"📌{i}. {tematica}")
    
    print()
    seleccion = pedir_opcion(1, len(dificultad))
    print(Fore.GREEN + Style.BRIGHT + f"\nElegiste: {dificultad[seleccion - 1]}")
    
    mostrar_introduccion_a_la_tematica(dificultad[seleccion - 1])
    return dificultad[seleccion - 1]

def cargar_introducciones():
    """
    Carga las introducciones de las tematicas desde un archivo JSON.

    Returns:
        dict: Diccionario con las introducciones de cada tematica
    """
    try:
        ruta_archivo_instrucciones = os.path.join(os.getcwd(), "Data", "introducciones.json")
        with open(ruta_archivo_instrucciones, "r") as introducciones_archivo:
            introducciones = json.load(introducciones_archivo)
            return introducciones
        
    except (FileNotFoundError, json.JSONDecodeError):
        print(Fore.RED + "No se encontro el archivo o el contenido es invalido.")
        return []

    except Exception as e:
        print(Fore.RED + f"Error inesperado: {e}")
        return []

def mostrar_introduccion_a_la_tematica(tematica):   
    """
    Muestra la introduccion correspondiente a una tematica especifica con estilo.

    Args:
        tematica (str): Nombre de la tematica a mostrar

    Returns:
        None
    """
    introducciones = cargar_introducciones()
    introduccion = introducciones.get(tematica, "Introduccion no disponible.")
    
    print(Fore.CYAN + Style.BRIGHT + f"=== Introduccion a la tematica: {tematica} ===")
    print() 
    print(Fore.WHITE + "=" * 60)
    print(Fore.YELLOW + Style.BRIGHT + introduccion)
    print(Fore.WHITE + "=" * 60)
    print()
    print("¿Deseas comenzar el juego o salir? 🌟")
    print(Fore.GREEN + "1. Comenzar Juego 🚀")
    print(Fore.RED + "2. Salir ❌")
    print()
    
    seleccion = pedir_opcion(1, 2)
    if seleccion == 1:
        print(Fore.GREEN + Style.BRIGHT + "Comenzando juego... 🚀")
        print()
    elif seleccion == 2:
        print(Fore.RED + Style.BRIGHT + "Saliendo... ❌")
        print()
        exit()
    else:
        print(Fore.RED + Style.BRIGHT + "⚠️ Por favor, ingresa una opcion valida.")
        print()

def inicializar_pistas():
    """
    Inicializa el sistema de pistas cargando el archivo JSON correspondiente.

    Returns:
        tuple: Par de diccionarios (pistas, pistas_usadas)
    """
    pistas = cargar_archivo_json("pistas.json")
    pistas_usadas = {key: [] for key in pistas.keys()}
    return pistas, pistas_usadas

def mostrar_pistas(tematica, pistas, pistas_usadas):
    """
    Muestra una pista aleatoria no utilizada para la tematica especificada.

    Args:
        tematica (str): Nombre de la tematica
        pistas (dict): Diccionario con todas las pistas disponibles
        pistas_usadas (dict): Diccionario con las pistas ya utilizadas

    Returns:
        None
    """
    if tematica in pistas:
        disponibles = [pista for pista in pistas[tematica] if pista not in pistas_usadas[tematica]]
        
        if disponibles:
            pista = random.choice(disponibles)
            print()
            print(Fore.GREEN + f"Pista para {tematica}: {pista}")
            print()
            pistas_usadas[tematica].append(pista)
        else:
            print(Fore.YELLOW + f"No hay mas pistas disponibles para la tematica '{tematica}'.")
    else:
        print(Fore.RED + f"Tematica '{tematica}' no valida.")

def mostrar_desafio(tematica, desafios, desafios_usados):
    """
    Muestra y gestiona un desafio aleatorio no utilizado para la tematica especificada.

    Args:
        tematica (str): Nombre de la tematica
        desafios (dict): Diccionario con todos los desafios disponibles
        desafios_usados (dict): Diccionario con los desafios ya utilizados

    Returns:
        None
    """
    fallo = True
    if tematica in desafios:
        disponibles = [desafios for desafios in desafios[tematica] if desafios not in desafios_usados[tematica]]
        
        if disponibles:
            desafios = random.choice(disponibles) 
            while fallo:
                desafio = list(desafios.split("|"))
                print()
                print(Fore.YELLOW + ">>>>> DESAFIO <<<<<")
                print(Fore.GREEN + f"{desafio[1]}")
                print()
                opcion = pedir_opcion(1,3)
                print(Fore.BLACK, Back.BLUE + "Tu respuesta: ", opcion,"👀")
                if(int(desafio[0])==opcion):
                    fallo = False
                    print(Fore.GREEN + "\n----- Bien ahi, completaste el desafio 🤩-----\n")
                else:
                    print(Fore.RED + "\n----- Dale otra vuelta de tuerca, esa no es. 😩-----\n")
            desafios_usados[tematica].append(desafios)
        else:
            print(Fore.YELLOW + f"No hay mas desafios disponibles para la tematica '{tematica}'.")
    else:
        print(Fore.RED + f"Tematica '{tematica}' no valida.")

def inicializar_desafios():
    """
    Inicializa el sistema de desafios cargando el archivo JSON correspondiente.

    Returns:
        tuple: Par de diccionarios (desafios, desafios_usados)
    """
    desafios = cargar_archivo_json("desafios.json")
    desafios_usados = {key: [] for key in desafios.keys()}
    return desafios, desafios_usados

def modificar_puntos(puntos, accion):
    """
    Modifica la puntuacion segun la accion realizada.

    Args:
        puntos (int): Puntuacion actual
        accion (str): Tipo de accion realizada

    Returns:
        int: Nueva puntuacion despues de aplicar la modificacion
    """
    modificaciones = {
        "usar_pista": -COSTO_PISTA,
        "completar_desafio": PUNTOS_DESAFIO,
        "accion_correcta": PUNTOS_MOVIMIENTO,
        "accion_incorrecta": -PUNTOS_MOVIMIENTO
    }
    return puntos + modificaciones.get(accion, -PUNTOS_MOVIMIENTO)

def mapa_para_tematica(tematica):
    """
    Genera un mapa especifico segun la tematica seleccionada.

    Args:
        tematica (str): Nombre de la tematica

    Returns:
        tuple: (mapa, probabilidad_fin, habitaciones_max)
    """
    mapa = []
    if(tematica == "Breaking Bad" or tematica == "Muerte Anunciada"):
        mapa = generar_mapa(4,5,4,6) 
        probabilidad_fin = random.randint(40,100)
        habitaciones_max = 2
    elif(tematica == "Psiquiatrico" or tematica == "La Casa de Papel"):
        mapa = generar_mapa(7,8,5,7)
        probabilidad_fin = random.randint(-20,100)
        habitaciones_max = 3
    elif(tematica == "Sherlock Holmes" or tematica == "Mision Gubernamental"):
        mapa = generar_mapa(9,10,5,8)
        probabilidad_fin = random.randint(-100,100)
        habitaciones_max = 4
    return mapa, probabilidad_fin, habitaciones_max

def contiene_elementos(lista1, lista2):
    """
    Verifica si una secuencia de elementos esta contenida en otra lista.

    Args:
        lista1 (list): Lista a buscar
        lista2 (list): Lista donde buscar

    Returns:
        bool: True si lista1 esta contenida en lista2, False en caso contrario
    """
    for i in range(0,len(lista2) - len(lista1) + 1,2):
        if lista2[i:i+len(lista1)] == lista1: 
            return True
    return False

def verificar_timeout(timer, limite_tiempo=180):
    """
    Verifica si se excedio el tiempo limite de 3 minutos

    Args:
        timer (Timer): Objeto Timer que lleva la cuenta del tiempo
        limite_tiempo (int): Tiempo limite en segundos (default 3 minutos = 180 segundos)

    Returns:
        bool: True si se excedio el tiempo, False en caso contrario
    """
    segundos_transcurridos = timer.obtener_segundos()
    return segundos_transcurridos >= limite_tiempo

def comenzar_juego(tematica, puntos=0, nro_habitacion=1):
    """
    Inicia y gestiona una partida del juego.

    Args:
        tematica (str): Tematica seleccionada para la partida
        puntos (int): Puntos iniciales (default: 0)
        nro_habitacion (int): Numero de habitacion actual (default: 1)

    Returns:
        tuple: (puntos_finales, estado_escapo)
    """
    puntos = 1000 + puntos
    escapo = False
    timer = Timer()
    timer.iniciar()
    
    pistas, pistas_usadas = inicializar_pistas()
    desafios, desafios_usadas = inicializar_desafios()
    mapa, probabilidad_fin, habitaciones_max = mapa_para_tematica(tematica)
    if (probabilidad_fin > 50 or nro_habitacion == habitaciones_max):
        habitacion_final = True
    else:
        habitacion_final = False 
    objetos = ["#","$"]
    for i in objetos:
        if(i=="#"):
            indices_pistas = get_indice_objeto(mapa,i) 
        else:
            indices_candados = get_indice_objeto(mapa,i)
            cant_candandos = len(indices_candados)//2
    
    while not escapo and not verificar_timeout(timer):
        posicion_actual = get_indice_objeto(mapa,"O") 
        mostrar_tiempo(timer)
        
        if(len(pistas_usadas.get(tematica)) == 0):
            print("Cuando encuentres una pista aparecera aca")
        else:
            print(pistas_usadas.get(tematica))
        
        if(contiene_elementos(posicion_actual, indices_pistas)): 
            print()
            print(Fore.BLUE + "----PISTA ENCONTRADA----")
            print()
            mostrar_pistas(tematica, pistas, pistas_usadas)
            puntos = modificar_puntos(puntos, "usar_pista")
            indices_pistas.remove(posicion_actual[0])
            indices_pistas.remove(posicion_actual[1])
        elif(contiene_elementos(posicion_actual, indices_candados)):
            mostrar_desafio(tematica, desafios, desafios_usadas)
            cant_candandos -= 1
            puntos = modificar_puntos(puntos, "completar_desafio")
            indices_candados.remove(posicion_actual[0])
            indices_candados.remove(posicion_actual[1])
            if(cant_candandos == 0):
                if(habitacion_final == True):
                    print()
                    print("------ Felicitaciones 🥳🥳🥳🎉🎊🎊 lograste escapar.... Por ahora.... ------")
                    print()
                    escapo = True
                else:
                    print()
                    print(Fore.BLUE + "------ 🏃🏃‍♀️🏃‍♀️‍➡️🏃‍➡️ Entrando en la siguiente habitacion.... 🏃🏃‍♀️🏃‍♀️‍➡️🏃‍➡️------")
                    print()
                    puntos, escapo = comenzar_juego(tematica, puntos, nro_habitacion + 1)
        
        if (not escapo):
            renderizar_mapa(mapa)
            accion = leer_accion()
            
            if puntos <= 0:
                print()
                print(Fore.RED + Style.BRIGHT + "Te quedaste sin puntos. Perdiste LOOOOOSER.")
                print()
                escapo = True
                puntos = -1
            elif accion == "menu":
                print()
                print(Fore.YELLOW + "Saliendo al menu principal...")
                print()
                escapo = True
                puntos = 0
            elif validar_movimiento(mapa, posicion_actual, accion):
                accion_personaje(mapa, accion)
                puntos = modificar_puntos(puntos, accion)
                print()
                print(Fore.GREEN + f"Puntos actuales: {puntos}")
                print()
            else:
                print()
                print(Fore.RED + "Movimiento invalido: fuera de los limites del mapa.")
                print()
    
    if verificar_timeout(timer):
        print()
        print(Fore.RED + "\n¡TIEMPO AGOTADO! Perdiste :(.")
        print()
        puntos = -1
        escapo = True
    
    timer.detener()
    mostrar_tiempo_final(timer,nro_habitacion)
    return puntos, escapo

def mostrar_tiempo_final(timer,nro_habitacion):
    """
    Muestra el tiempo total de juego al finalizar la partida

    Args:
        timer (Timer): Objeto Timer que lleva la cuenta del tiempo

    Returns:
        None
    """
    print(Fore.BLUE, f"\nTiempo total de juego en la habitacion {nro_habitacion}: {timer.obtener_tiempo()}")

def instrucciones():
    """
    Muestra las instrucciones del juego en pantalla.

    Returns:
        None
    """
    os.system('clear')
    print()
    print(Fore.CYAN + "=== 📚 INSTRUCCIONES DEL JUEGO ===")
    print(Fore.YELLOW + "\nTe encuentras en un mapa donde puedes moverte libremente.")
    print(Fore.MAGENTA + "Tu objetivo es escapar resolviendo desafios, y para eso tendras que recoger pistas.")
    print(Fore.GREEN + "\nComenzaras con 1000 puntos. Cada accion que realices costara puntos, ¡cuidado!")
    print(Fore.RED + "Si te quedas sin puntos, perderas el juego. 💔")
    print(Fore.BLUE + "\n¡Pero si resuelves los desafios, ganaras puntos! 🎉")

    print(Fore.CYAN + "\nPara moverte usa las teclas: W, A, S, D o las flechitas ⬆️⬇️⬅️➡️")
    print(Fore.YELLOW + "Y para salir, presiona 'M'. 🚪")

    print(Fore.GREEN + "\n¿Listo para empezar? 🤔 (Si/No)")
    respuesta = input(Fore.WHITE + "> ").strip().lower()
    if respuesta == "si" or respuesta == "si":
        print(Fore.GREEN + "¡Vamos a comenzar! 💥")
    else:
        print(Fore.RED + "¡No hay marcha atras! 😈")
    input("\nPresiona Enter para continuar...")
    print()
    
def registrar_puntos(user, puntos):
    """
    Actualiza el registro de puntos de un usuario si supera su mejor marca.

    Args:
        user (str): Nombre del usuario
        puntos (int): Puntos a registrar

    Returns:
        None
    """
    user_repository = cargar_archivo_json("user_repository.json")
    if not user_repository:
        print(Fore.RED + "Error: No se pudo cargar el repositorio de usuarios.")
        return

    jugador = next((u for u in user_repository if u['username'] == user), None)
    if jugador:
        if puntos > jugador["puntos"]:
            jugador["puntos"] = puntos
            if guardar_archivo_json("user_repository.json", user_repository):
                print(Fore.GREEN + f"Puntos actualizados para el usuario '{user}': " + Fore.LIGHTCYAN_EX + f"{puntos}")
            else:
                print(Fore.RED + "Error al actualizar los puntos.")
        else:
            print(Fore.YELLOW + f"El usuario '{user}' ya tiene un puntaje mayor o igual: " + Fore.LIGHTCYAN_EX + f"{jugador['puntos']}")
    else:
        print(Fore.RED + f"Error: El usuario '{user}' no existe en el repositorio.")


def ranking_jugador(users, username=None):
    """
    Muestra la informacion de ranking de un jugador especifico.

    Args:
        users (list): Lista de usuarios registrados
        username (str, optional): Nombre del usuario a buscar

    Returns:
        None
    """
    if username is None:
        username = pedir_user_name()

    jugador = next((user for user in users 
                   if user.get('username', '').lower() == username.lower()), None)
    
    if jugador:
        print(Fore.GREEN + f"\n🎮 Jugador: {jugador['username']}")
        print(Fore.CYAN + f"🏆 Puntuacion maxima: {jugador.get('puntos', 0)}")
    else:
        print(Fore.RED + f"\n❌ No se encontro al jugador '{username}'")
    
    input("\nPresione Enter para continuar...")

def primeros_ultimos_ranking(usuarios, primeros):
    """
    Muestra los primeros o ultimos 10 usuarios del ranking.

    Args:
        usuarios (list): Lista de usuarios registrados
        primeros (bool): True para mostrar mejores puntuaciones, False para peores

    Returns:
        None
    """
    if not usuarios:
        print(Fore.RED + "\nNo hay usuarios registrados en el ranking. 🚫")
        input(Fore.WHITE + "\nPresiona Enter para continuar...")
        return
    
    usuarios_ordenados = sorted(
        usuarios,
        key=lambda x: x.get('puntos', 0),
        reverse=primeros
    )
    
    rank = usuarios_ordenados[:10]
    
    print(Fore.CYAN + "\n{:<6} {:<15} {:<10}".format("Puesto", "Usuario", "Puntos"))
    print("-" * 35)
    
    for i, user in enumerate(rank, 1):
        puesto = i if primeros else len(usuarios) - i + 1
        if i <= 3:
            puesto_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        else:
            puesto_icon = "⚫"
        
        print("{:<6} {:<15} {:<10}".format(
            f"{puesto} {puesto_icon}",
            user.get('username', 'N/A'),
            user.get('puntos', 0)
        ))
    
    input("\nPresiona Enter para continuar...")

def ranking(user):
    """
    Gestiona el menu de ranking y sus opciones.

    Args:
        user (str): Nombre del usuario actual

    Returns:
        None
    """
    menu_activo = True
    while menu_activo:
        vaciar_consola()
        print(Fore.LIGHTGREEN_EX + "\n=== 🏆 RANKING DE JUGADORES ===")
        print(Fore.YELLOW + "1. Ver mejores puntuaciones 🎯")
        print(Fore.YELLOW + "2. Buscar jugador 🔍")
        print(Fore.YELLOW + "3. Ver peores puntuaciones 💩")
        print(Fore.YELLOW + "4. Mi mejor puntuacion 🌟")
        print(Fore.YELLOW + "5. Salir 🚪")
        
        try:
            opcion = pedir_opcion(1, 5)
            
            user_repository = cargar_archivo_json("user_repository.json")
            if not isinstance(user_repository, list):
                user_repository = []
            
            if opcion == 1:
                primeros_ultimos_ranking(user_repository, True)
            elif opcion == 2:
                ranking_jugador(user_repository)
            elif opcion == 3:
                primeros_ultimos_ranking(user_repository, False)
            elif opcion == 4:
                ranking_jugador(user_repository, user)
            elif opcion == 5:
                print(Fore.LIGHTCYAN_EX + "\nVolviendo al menu principal... 🚶")
                menu_activo = False
                
        except Exception as e:
            print(Fore.RED + f"\n❌ Error inesperado: {e}")
            input("\nPresione Enter para continuar...")

class Timer:
    """
    Clase para gestionar el tiempo de juego.

    Methods:
        iniciar(): Inicia el contador de tiempo
        detener(): Detiene el contador de tiempo
        _contar(): Metodo interno para contar segundos
        obtener_tiempo(): Devuelve el tiempo transcurrido en formato mm:ss
    """

    def __init__(self):
        self.segundos = 0
        self.activo = True
        self.thread = threading.Thread(target=self._contar)
        
    def iniciar(self):
        """Inicia el timer en un thread separado"""
        self.activo = True
        self.thread.start()
    
    def detener(self):
        """Detiene el timer"""
        self.activo = False
        if self.thread.is_alive():
            self.thread.join()
    
    def _contar(self):
        """Funcion que cuenta el tiempo"""
        while self.activo:
            time.sleep(1)
            self.segundos += 1
    
    def obtener_tiempo(self):
        """Devuelve el tiempo en formato mm:ss"""
        minutos = self.segundos // 60
        segs = self.segundos % 60
        return f"{minutos:02d}:{segs:02d}"
    
    def obtener_segundos(self):
        """Devuelve el total de segundos transcurridos"""
        return self.segundos

def main():
    """
    Funcion principal que inicia y controla el flujo del juego.

    Returns:
        None
    """
    user = pedir_user_name()
    generar_user(user)
    jugando = True
    tematica = 0
    timer = Timer()
    while(jugando):
        menu_principal(user)
        opcion = pedir_opcion(1,4)
        
        if(opcion == 1):
            tematica = elegir_tematica()
            timer = Timer()
            timer.iniciar()
            puntos, escapo = comenzar_juego(tematica)
            
            if puntos > 0 and escapo:
                registrar_puntos(user,puntos)
            elif puntos == -1:
                if verificar_timeout(timer):
                    print(Fore.RED + "¡TIEMPO AGOTADO! El juego ha terminado. ⏰")
                else:
                    print(Fore.RED + "Te quedaste sin puntos. ¡Has perdido! 💔")
            else:
                print(Fore.YELLOW + "Abandonaste pero no pasa nada, ¡suerte la proxima! 🍀")
                
            timer.detener()       
        elif (opcion == 2):
            ranking(user)
        elif (opcion == 3):
            instrucciones()
        elif (opcion == 4):
            print(Fore.LIGHTMAGENTA_EX + "\nGracias por jugar! Saliendo... 👋")
            jugando = False
main()