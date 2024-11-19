import random
import re
import json
import os
from readchar import readkey, key
import threading
import time

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
        dict: Contenido del archivo JSON o diccionario vacío si hay error
    """
    try:
        ruta_archivo = os.path.join(os.getcwd(), "Data", nombre_archivo)
        with open(ruta_archivo, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo {nombre_archivo}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {nombre_archivo} tiene un formato inválido.")
        return {}
    except Exception as e:
        print(f"Error inesperado: {e}")
        return {}

def guardar_archivo_json(nombre_archivo, datos):
    """
    Guarda datos en un archivo JSON en la carpeta Data.

    Args:
        nombre_archivo (str): Nombre del archivo donde guardar los datos
        datos (dict): Datos a guardar en formato JSON

    Returns:
        bool: True si se guardó correctamente, False si hubo error
    """
    try:
        ruta_archivo = os.path.join(os.getcwd(), "Data", nombre_archivo)
        with open(ruta_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar {nombre_archivo}: {e}")
        return False

def generar_terreno(mapa, altura_min, altura_max, ancho_min, ancho_max):
    """
    Genera el terreno base del mapa con dimensiones aleatorias dentro de los rangos especificados.

    Args:
        mapa (list): Lista vacía donde se generará el terreno
        altura_min (int): Altura mínima del mapa
        altura_max (int): Altura máxima del mapa
        ancho_min (int): Ancho mínimo del mapa
        ancho_max (int): Ancho máximo del mapa

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
        objeto (str): Carácter que representa el objeto a generar
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
        altura_min (int): Altura mínima del mapa
        altura_max (int): Altura máxima del mapa
        ancho_min (int): Ancho mínimo del mapa
        ancho_max (int): Ancho máximo del mapa

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
        print(fila)
        
def mostrar_tiempo(timer):
    """
    Muestra el tiempo transcurrido en el formato mm:ss.

    Args:
        timer (Timer): Objeto Timer que lleva la cuenta del tiempo

    Returns:
        None
    """
    print(f"Tiempo: {timer.obtener_tiempo()}")
    print()

def leer_accion():
    """
    Lee y valida la entrada del usuario para movimientos y acciones.

    Returns:
        str: Acción validada ('w', 'a', 's', 'd', 'menu')
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
    Verifica si un movimiento es válido dentro del mapa.

    Args:
        mapa (list): Matriz que representa el mapa
        posicion_actual (list): Coordenadas actuales [x, y]
        accion (str): Dirección del movimiento ('w', 'a', 's', 'd')

    Returns:
        bool: True si el movimiento es válido, False si no lo es
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
    Encuentra las coordenadas de un objeto específico en el mapa.

    Args:
        mapa (list): Matriz que representa el mapa
        objeto (str): Carácter del objeto a buscar

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
    Mueve un objeto en el mapa según las coordenadas especificadas.

    Args:
        mapa (list): Matriz que representa el mapa
        x (int): Desplazamiento en el eje x
        y (int): Desplazamiento en el eje y
        objeto (str): Carácter del objeto a mover

    Returns:
        None: Modifica el mapa directamente
    """
    coordenadas_objeto = get_indice_objeto(mapa,objeto)
    mapa[coordenadas_objeto[0]][coordenadas_objeto[1]] = TERRENO
    mapa[coordenadas_objeto[0]+y*(-1)][coordenadas_objeto[1]+x] = objeto

def accion_personaje(mapa,accion): 
    """
    Ejecuta el movimiento del personaje según la acción especificada.

    Args:
        mapa (list): Matriz que representa el mapa
        accion (str): Dirección del movimiento ('w', 'a', 's', 'd')

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


def menu_principal(user):
    """
    Muestra el menú principal del juego.

    Args:
        user (str): Nombre del usuario actual

    Returns:
        None
    """
    print()
    print(f"{user} Bienvenido a UadEscape")
    print("1. Comenzar Juego")
    print("2. Ranking de puntos")
    print("3. Como Jugar")
    print("4. Salir")
 

def pedir_user_name(jugador_numero=0):
    """
    Solicita y valida el nombre de usuario.

    Args:
        jugador_numero (int): Número de jugador (0 para un solo jugador)

    Returns:
        str: Nombre de usuario validado
    """
    patron = r"^[a-zA-Z]{3,9}$"
    bienvenida = lambda x : x if(x == 0) else print(f"Bienvenido jugador {jugador_numero}") 
    bienvenida(jugador_numero)
    username = input(f"Jugador, ingrese un nombre de usuario (3-9 caracteres, sin números o caracteres especiales): ")
    nombre_valido = re.match(patron, username)

    while nombre_valido is None:
        if nombre_valido is None:
            print(f"Nombre no válido. Inténtelo de nuevo.")
        username = input(f"Jugador, por favor, ingrese un nombre de usuario: ")
        nombre_valido = re.match(patron, username)
    return username

def pedir_user_names():
    """
    Solicita nombres de usuario para dos jugadores.

    Returns:
        tuple: Par de nombres de usuario (user_name1, user_name2)
    """

    user_name1 = pedir_user_name(1)
    user_name2 = pedir_user_name(2)
    return user_name1, user_name2

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
        print(f"El nombre de usuario '{username}' ya está en uso. Intente con otro.")
        username = pedir_user_name()
    
    nuevo_usuario = {
        "username": username,
        "id": generar_id(user_repository),
        "puntos": 0
    }
    user_repository.append(nuevo_usuario)
    
    if guardar_archivo_json("user_repository.json", user_repository):
        print(f"Usuario '{username}' registrado con éxito.")
    else:
        print("Error al registrar el usuario.")

def generar_id(user_repository):
    """
    Genera un nuevo ID para un usuario basado en el último ID registrado.

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
    Solicita y valida una opción numérica dentro de un rango.

    Args:
        min (int): Valor mínimo aceptado
        max (int): Valor máximo aceptado

    Returns:
        int: Opción validada dentro del rango especificado
    """
    while True:
        try:
            opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
            if min <= opcion <= max:
                print()
                return opcion
            print("Error, la opción ingresada no está en el rango válido.")
        except ValueError:
            print("Error, debe ingresar un número.")

def mostrar_dificultades():
    """
    Muestra en pantalla los niveles de dificultad disponibles.

    Returns:
        None
    """

    print("Niveles de dificultad: ")
    print("1. Facil")
    print("2. Normal")
    print("3. Dificil")
    

def nivel_de_dificultad():
    """
    Permite al usuario seleccionar un nivel de dificultad y devuelve las temáticas correspondientes.

    Returns:
        list: Lista de temáticas disponibles para la dificultad seleccionada
    """
    mostrar_dificultades()
    opcion = pedir_opcion(1,3)

    facil = ["Breaking Bad","Muerte Anunciada"]
    intermedio = ["Psiquiátrico","La Casa de Papel"]
    dificil = ["Sherlock Holmes","Misión Gubernamental"]

    if opcion == 1:
        dificultad = facil
    elif opcion == 2:
        dificultad = intermedio
    elif opcion == 3:
        dificultad = dificil

    return dificultad

def elegir_tematica():
    """
    Permite al usuario seleccionar una temática según la dificultad elegida.

    Returns:
        str: Nombre de la temática seleccionada
    """
    dificultad = nivel_de_dificultad()
    print("Temáticas disponibles:")
    for i, tematica in enumerate(dificultad, 1):
        print(f"{i}: {tematica}")

    seleccion = pedir_opcion(1, len(dificultad))
    mostrar_introduccion_a_la_tematica(dificultad[seleccion - 1])
    return dificultad[seleccion - 1]

def cargar_introducciones():
    """
    Carga las introducciones de las temáticas desde un archivo JSON.

    Returns:
        dict: Diccionario con las introducciones de cada temática
    """
    try:
        ruta_archivo_instrucciones = os.path.join(os.getcwd(), "Data", "introducciones.json")
        with open(ruta_archivo_instrucciones, "r") as introducciones_archivo:
            introducciones = json.load(introducciones_archivo)
            return introducciones
        
    except (FileNotFoundError, json.JSONDecodeError):
        print("No se encontró el archivo o el contenido es inválido.")
        return []

    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def mostrar_introduccion_a_la_tematica(tematica):   
    """
    Muestra la introducción correspondiente a una temática específica.

    Args:
        tematica (str): Nombre de la temática a mostrar

    Returns:
        None
    """
    introducciones = cargar_introducciones()
    introduccion = introducciones.get(tematica, "Introducción no disponible.")
    print(introduccion)

    print("¿Deseas comenzar el juego o salir?")
    print("1. Comenzar Juego")
    print("2. Salir")
    seleccion = pedir_opcion(1, 2)
    if seleccion == 1:
        print("Comenzando juego...")
    elif seleccion == 2:
        print("Saliendo...")
        exit()
    else:
        print("Por favor, ingresá una opción válida.")

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
    Muestra una pista aleatoria no utilizada para la temática especificada.

    Args:
        tematica (str): Nombre de la temática
        pistas (dict): Diccionario con todas las pistas disponibles
        pistas_usadas (dict): Diccionario con las pistas ya utilizadas

    Returns:
        None
    """
    if tematica in pistas:
        disponibles = [pista for pista in pistas[tematica] if pista not in pistas_usadas[tematica]]
        
        if disponibles:
            pista = random.choice(disponibles)
            print(f"Pista para {tematica}: {pista}")
            pistas_usadas[tematica].append(pista)
        else:
            print(f"No hay más pistas disponibles para la temática '{tematica}'.")
    else:
        print(f"Temática '{tematica}' no válida.")

def mostrar_desafio(tematica, desafios, desafios_usados):
    """
    Muestra y gestiona un desafío aleatorio no utilizado para la temática especificada.

    Args:
        tematica (str): Nombre de la temática
        desafios (dict): Diccionario con todos los desafíos disponibles
        desafios_usados (dict): Diccionario con los desafíos ya utilizados

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
                print(f"{desafio[1]}")
                opcion = pedir_opcion(1,3)
                if(int(desafio[0])==opcion):
                    fallo = False
                    print()
                    print("----- Bien, completaste el desafio -----")
                    print()
                else:
                    print()
                    print("----- Dale otra vuelta de tuerca, esa no es. -----")
                    print()

            desafios_usados[tematica].append(desafios)
        else:
            print(f"No hay más desafios disponibles para la temática '{tematica}'.")
    else:
        print(f"Temática '{tematica}' no válida.")

def inicializar_desafios():
    """
    Inicializa el sistema de desafíos cargando el archivo JSON correspondiente.

    Returns:
        tuple: Par de diccionarios (desafios, desafios_usados)
    """
    desafios = cargar_archivo_json("desafios.json")
    desafios_usados = {key: [] for key in desafios.keys()}
    return desafios, desafios_usados

def modificar_puntos(puntos, accion):
    """
    Modifica la puntuación según la acción realizada.

    Args:
        puntos (int): Puntuación actual
        accion (str): Tipo de acción realizada

    Returns:
        int: Nueva puntuación después de aplicar la modificación
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
    Genera un mapa específico según la temática seleccionada.

    Args:
        tematica (str): Nombre de la temática

    Returns:
        tuple: (mapa, probabilidad_fin, habitaciones_max)
    """
    mapa = []
    if(tematica == "Breaking Bad" or tematica == "Muerte Anunciada"):
        mapa = generar_mapa(4,5,4,6) 
        probabilidad_fin = random.randint(40,100)
        habitaciones_max = 2
    elif(tematica == "Psiquiátrico" or tematica == "La Casa de Papel"):
        mapa = generar_mapa(7,8,5,7)
        probabilidad_fin = random.randint(-20,100)
        habitaciones_max = 3
    elif(tematica == "Sherlock Holmes" or tematica == "Misión Gubernamental"):
        mapa = generar_mapa(9,10,5,8)
        probabilidad_fin = random.randint(-100,100)
        habitaciones_max = 4
    return mapa, probabilidad_fin, habitaciones_max

def contiene_elementos(lista1, lista2):
    """
    Verifica si una secuencia de elementos está contenida en otra lista.

    Args:
        lista1 (list): Lista a buscar
        lista2 (list): Lista donde buscar

    Returns:
        bool: True si lista1 está contenida en lista2, False en caso contrario
    """
    for i in range(0,len(lista2) - len(lista1) + 1,2):
        if lista2[i:i+len(lista1)] == lista1: 
            return True
    return False

def comenzar_juego(tematica, puntos=0, nro_habitacion=1):
    """
    Inicia y gestiona una partida del juego.

    Args:
        tematica (str): Temática seleccionada para la partida
        puntos (int): Puntos iniciales (default: 0)
        nro_habitacion (int): Número de habitación actual (default: 1)

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
    
    while not escapo:
        posicion_actual = get_indice_objeto(mapa,"O")
        mostrar_tiempo(timer)
        
        if(len(pistas_usadas.get(tematica)) == 0):
            print("Cuando encuentres una pista aparecera aca")
        else:
            print(pistas_usadas.get(tematica))
        
        if(contiene_elementos(posicion_actual, indices_pistas)): 
            print("----PISTA ENCONTRADA----")
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
                    print("------ Felicitaciones, lograste escapar.... Por ahora.... ------")
                    escapo = True
                else:
                    print("------ Entrando en la siguiente habitacion.... ------")
                    puntos, escapo = comenzar_juego(tematica,puntos,nro_habitacion+1)

        if (not escapo):
            renderizar_mapa(mapa)
            accion = leer_accion()
            
            if puntos <= 0:
                print("Te quedaste sin puntos. Perdiste LOOOOOSER.")
                escapo = True
                puntos = -1
            elif accion == "menu":
                print("Saliendo al menu principal...")
                escapo = True
                puntos = 0
            elif validar_movimiento(mapa, posicion_actual, accion):   
                accion_personaje(mapa,accion)
                puntos = modificar_puntos(puntos,accion)
                print(f"Puntos actuales: {puntos}")
            else:
                print("Movimiento inválido: fuera de los límites del mapa.")
    
    timer.detener()
    return puntos, escapo

def instrucciones():
    """
    Muestra las instrucciones del juego en pantalla.

    Returns:
        None
    """
    os.system('clear')
    print("Comenzaras tu aventura en un mapa donde podras moverte libremente, tu personaje (Señalizado como una 'O') debera recoger pistas (Señalizadas como '#') para resolver los desafios (Señalizados como '$') y asi escapar!")
    print("Iniciarás con una totalidad de 1000 puntos a tu favor. Si necesitas ayuda, podés usar pistas, pero estas te costarán puntos.")
    print("Cada acción que realices también te costará puntos, por lo que deberas ser cuidadoso con tus movimientos.")
    print("Si te quedas sin puntos, perderas el juego. Si lográs descifrar el desafío, ganarás puntos. Una vez cumplidos todos los desafíos, en caso de que lo hagas, habrás ganado el juego.")
    print("Buena suerte, la vas a necesitar.")

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
        print("Error: No se pudo cargar el repositorio de usuarios.")
        return

    jugador = next((u for u in user_repository if u['username'] == user), None)
    if jugador:
        if puntos > jugador["puntos"]:
            jugador["puntos"] = puntos
            if guardar_archivo_json("user_repository.json", user_repository):
                print(f"Puntos actualizados para el usuario '{user}': {puntos}")
            else:
                print("Error al actualizar los puntos.")
        else:
            print(f"El usuario '{user}' ya tiene un puntaje mayor o igual: {jugador['puntos']}")
    else:
        print(f"Error: El usuario '{user}' no existe en el repositorio.")

def ranking_jugador(users, username=None):
    """
    Muestra la información de ranking de un jugador específico.

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
        print(f"\nJugador: {jugador['username']}")
        print(f"Puntuación máxima: {jugador.get('puntos', 0)}")
    else:
        print(f"\nNo se encontró al jugador '{username}'")
    
    input("\nPresione Enter para continuar...")

def primeros_ultimos_ranking(usuarios, primeros):
    """
    Muestra los primeros o últimos 10 usuarios del ranking.

    Args:
        usuarios (list): Lista de usuarios registrados
        primeros (bool): True para mostrar mejores puntuaciones, False para peores

    Returns:
        None
    """
    if not usuarios:
        print("\nNo hay usuarios registrados en el ranking.")
        input("\nPresione Enter para continuar...")
        return
    
    usuarios_ordenados = sorted(
        usuarios,
        key=lambda x: x.get('puntos', 0),
        reverse=primeros
    )
    
    rank = usuarios_ordenados[:10]
    
    print("\n{:<6} {:<15} {:<10}".format("Puesto", "Usuario", "Puntos"))
    print("-" * 35)
    
    for i, user in enumerate(rank, 1):
        puesto = i if primeros else len(usuarios) - i + 1
        print("{:<6} {:<15} {:<10}".format(
            puesto,
            user.get('username', 'N/A'),
            user.get('puntos', 0)
        ))
    
    input("\nPresione Enter para continuar...")

def ranking(user):
    """
    Gestiona el menú de ranking y sus opciones.

    Args:
        user (str): Nombre del usuario actual

    Returns:
        None
    """
    menu_activo = True
    while menu_activo:
        vaciar_consola()
        print("\n=== RANKING DE JUGADORES ===")
        print("1. Ver mejores puntuaciones")
        print("2. Buscar jugador")
        print("3. Ver peores puntuaciones")
        print("4. Mi mejor puntuación")
        print("5. Salir")
        
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
                print("\nVolviendo al menú principal...")
                menu_activo = False
                
        except Exception as e:
            print(f"\nError inesperado: {e}")
            input("\nPresione Enter para continuar...")

class Timer:
    """
    Clase para gestionar el tiempo de juego.

    Methods:
        iniciar(): Inicia el contador de tiempo
        detener(): Detiene el contador de tiempo
        _contar(): Método interno para contar segundos
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
        """Función que cuenta el tiempo"""
        while self.activo:
            time.sleep(1)
            self.segundos += 1
    
    def obtener_tiempo(self):
        """Devuelve el tiempo en formato mm:ss"""
        minutos = self.segundos // 60
        segs = self.segundos % 60
        return f"{minutos:02d}:{segs:02d}"

def main():
    """
    Función principal que inicia y controla el flujo del juego.

    Returns:
        None
    """
    user = pedir_user_name()
    generar_user(user)
    jugando = True
    tematica = 0
    while(jugando):
        menu_principal(user)
        opcion = pedir_opcion(1,4)
        if(opcion == 1):
            tematica = elegir_tematica()
            puntos, escapo = comenzar_juego(tematica)
            if puntos > 0 and escapo:
                print("Felicidades, escapaste")
                registrar_puntos(user,puntos)
            elif puntos == -1:
                print("Te quedaste sin puntos. Perdiste LOOOOOSER.")
            else:
                print("Abandonaste pero no pasa nada, suerte la proxima!")
        elif (opcion == 2):
            ranking(user)
        elif (opcion == 3):
            instrucciones()
        elif (opcion == 4):
            print("Gracias por Jugar! Saliendo...")
            jugando = False
    
main()