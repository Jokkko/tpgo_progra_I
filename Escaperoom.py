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
    Limpia la consola de manera compatible con Windows y Unix/Mac
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def cargar_archivo_json(nombre_archivo):
    '''
    Función genérica para cargar archivos JSON
    Retorna el contenido del archivo o un diccionario vacío si hay error
    '''
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
    '''
    Función genérica para guardar datos en archivos JSON
    '''
    try:
        ruta_archivo = os.path.join(os.getcwd(), "Data", nombre_archivo)
        with open(ruta_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar {nombre_archivo}: {e}")
        return False

def generar_terreno(mapa,altura_min,altura_max,ancho_min,ancho_max):
    '''
    Genera el terreno de un mapa vacio pasado por parametro, el tipo de terreno sera definido por una variable global
    el ancho y la altura sera un numero entre los minimos y maximos pasados por parametros.
    '''
    alto_del_mapa = random.randint(altura_min,altura_max)
    ancho_minimo_del_mapa = random.randint(ancho_min,ancho_max) 

    for _ in range(alto_del_mapa):
        mapa.append([TERRENO for _ in range(ancho_minimo_del_mapa)])
        
def generar_objeto(mapa,objeto,cantidad):
    '''
    Recibe un mapa (matriz), un objeto (caracter string) cantidad (int) Y genera en x posiciones aleatoria del mapa el objeto pasado por parametro
    x es definida por cantidad
    '''
    columna_spawn = random.randint(0,len(mapa)-1) 
    fila_spawn = random.randint(0,len(mapa[columna_spawn])-1)
    for _ in range(cantidad):
        while(mapa[columna_spawn][fila_spawn] != TERRENO): 
            columna_spawn = random.randint(0,len(mapa)-1) 
            fila_spawn = random.randint(0,len(mapa[columna_spawn])-1)
        mapa[columna_spawn][fila_spawn] = objeto

def generar_mapa(altura_min,altura_max,ancho_min,ancho_max):
    '''
    Genera un mapa de juego con una altura y un ancho, minimo y maximo
    Ademas de rellenar el mapa con un terreno, un personaje, almenos un candado y almenos una pista.
    '''
    mapa = []
    generar_terreno(mapa,altura_min,altura_max,ancho_min,ancho_max)
    for i in [PERSONAJE, CANDADO, PISTA]:
        if(i == PERSONAJE):
            generar_objeto(mapa,i,1)
        else:
            generar_objeto(mapa,i,2) 
        
    return mapa

def renderizar_mapa(mapa):
    '''
    Muestra la salida por consola de una mapa (matriz) recibido por parametro
    '''
    for fila in mapa:
        print(fila)
        
def mostrar_tiempo(timer):
    """
    Muestra el tiempo transcurrido en la esquina superior
    """
    print(f"Tiempo: {timer.obtener_tiempo()}")
    print()

def leer_accion():
    '''
    Lee de la entrada un string ingresado por el usuario, verifica que este dentro de las acciones validas ('w', 'a', 's', 'd','menu')
    y devuelve la accion validada
    '''
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
    '''
    Recibe por parametro un mapa (matriz) una posicion_actual (lista) que hacen referencia a los ejes x y de una matriz, y recibe una accion
    'w', 'a', 's', 'd' verifica que la matriz desde la posicion_actual tenga espacio para moverse en cada eje segun w a s d
    '''
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
    '''
    Recibe por parametro un mapa y un objeto, se encarga de guardar todos los pares [x y] donde ese objeto se encuentre en la matriz y los devuelve
    en una lista 
    '''
    indices = []
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if(mapa[y][x] == objeto):
                indices.append(y)
                indices.append(x)
    return indices

def mover_objeto(mapa,x,y,objeto):
    '''
    Mueve a un objeto recibido por parametro dentro de la matriz mapa tambien recibida por parametro, tantas veces en x como diga el parametro
    y tantas veces en y como diga el parametro.
    '''
    coordenadas_objeto = get_indice_objeto(mapa,objeto)
    mapa[coordenadas_objeto[0]][coordenadas_objeto[1]] = TERRENO
    mapa[coordenadas_objeto[0]+y*(-1)][coordenadas_objeto[1]+x] = objeto

def accion_personaje(mapa,accion): 
    '''
    Recibe un mapa por parametro y una accion, (w,a,s,d) llama a la funcion mover_objeto, para mover al personaje segun la accion elegida
    '''
    if  (accion == "w"):
        mover_objeto(mapa,0,1,PERSONAJE)
    elif(accion == "s"):
        mover_objeto(mapa,0,-1,PERSONAJE) 
    elif(accion == "a"):
        mover_objeto(mapa,-1,0,PERSONAJE)
    elif(accion == "d"):
        mover_objeto(mapa,1,0,PERSONAJE)


def menu_principal(user):
    '''
    Funcion que se encarga de mostrar el menu principal del juego
    '''
    print()
    print(f"{user} Bienvenido a UadEscape")
    print("1. Comenzar Juego")
    print("2. Ranking de puntos")
    print("3. Como Jugar")
    print("4. Salir")
 

def pedir_user_name(jugador_numero=0):
    '''
    Funcion que recibe por parametro el numero de jugado que va a jugar , pedir al usuario que ingrese el nombre, y generarlo
    devuelve el nombre de usuario validado 
    '''
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
    '''Funcion auxiliar que  se encarga de pedir y generar dos usernames, para dos jugadores, los devuelve'''
    user_name1 = pedir_user_name(1)
    user_name2 = pedir_user_name(2)
    return user_name1, user_name2

def generar_user(username):
    '''
    Genera el registro del usuario nuevo generando una id, y asociándole el nombre de usuario.
    '''
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
    '''
    Funcion que genera un id para un usuario, a partir del ultimo id ingresado
    '''
    id = 0
    if(len(user_repository) != 0):
        ultimo = len(user_repository)-1 
        id = user_repository[ultimo]['id'] + 1
    return id

def pedir_opcion(min,max):
    '''
    Funcion que se encarga de pedir un numero al usuario entre un minimo y un maximo, luego valida y devuelve la opcion elegida
    '''
    opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
    
    while opcion < min or opcion > max:
        print("Error, la opción ingresada no es válida.")
        opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
    
    print()
    return opcion

def mostrar_dificultades():
    '''
    Funcion que se encarga de mostrar los distintos niveles de dificultad
    '''
    print("Niveles de dificultad: ")
    print("1. Facil")
    print("2. Normal")
    print("3. Dificil")
    

def nivel_de_dificultad():
    '''
    Funcion que se encarga de pedirle al usuario que ingrese que dificultad quiere elegir y que devuelve las distintas tematicas segun la dificutald
    '''
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
    '''
    Funcion que se encarga de pedirle a un usuario que ingrese que tematica quiere jugar, segun que dificultad anteriormente eligio.
    Ademas se le mostrara una introduccion a la tematica elegida. Y luego se devuelve la tematica elegida
    '''
    dificultad = nivel_de_dificultad()
    print("Temáticas disponibles:")
    for i, tematica in enumerate(dificultad, 1):
        print(f"{i}: {tematica}")

    seleccion = pedir_opcion(1, len(dificultad))
    mostrar_introduccion_a_la_tematica(dificultad[seleccion - 1])
    return dificultad[seleccion - 1]

def cargar_introducciones():
    '''
    Carga las introducciones desde el archivo JSON ubicado en la carpeta Data.
    Si el archivo no existe o contiene un JSON inválido, retorna una lista vacía.
    '''
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
    '''
    Funcion que se encarga de mostrar la introduccion a una tematica
    '''
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
    '''
    Carga las pistas desde un archivo JSON
    '''
    pistas = cargar_archivo_json("pistas.json")
    pistas_usadas = {key: [] for key in pistas.keys()}
    return pistas, pistas_usadas

def mostrar_pistas(tematica, pistas, pistas_usadas):
    '''
    Funcion que recibe una tematica, pistas para la misma, y las pistas que fueron usadas, se encarga de mostrar una pista aleatoria de las disopnibles
    '''
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
    '''
    Funcion que recibe una tematica, desafios para la misma, y los desafios que fueron usados,
      se encarga de mostrar un desafio aleatorio de los disponibles
    '''
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
    '''
    Carga los desafíos desde un archivo JSON
    '''
    desafios = cargar_archivo_json("desafios.json")
    desafios_usados = {key: [] for key in desafios.keys()}
    return desafios, desafios_usados

def modificar_puntos(puntos, accion):
    '''
    Modifica los puntos según la acción realizada
    '''
    modificaciones = {
        "usar_pista": -COSTO_PISTA,
        "completar_desafio": PUNTOS_DESAFIO,
        "accion_correcta": PUNTOS_MOVIMIENTO,
        "accion_incorrecta": -PUNTOS_MOVIMIENTO
    }
    return puntos + modificaciones.get(accion, -PUNTOS_MOVIMIENTO)

def mapa_para_tematica(tematica):
    '''
    Genera un mapa aleatorio para una tematica recibida por parametro
    '''
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
    ''' Verifica si lista1 esta en lista2 en forma de secuencia'''
    for i in range(0,len(lista2) - len(lista1) + 1,2):
        if lista2[i:i+len(lista1)] == lista1: 
            return True
    return False

def comenzar_juego(tematica, puntos=0, nro_habitacion=1):
    '''
    Funcion que provoca que el juego comienze
    '''
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
            
            if accion == "menu":
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
    '''
    Muestra las instrucciones para poder jugar al juego
    '''
    os.system('clear')
    print("Comenzaras tu aventura en un mapa donde podras moverte libremente, tu personaje (Señalizado como una 'O') debera recoger pistas (Señalizadas como '#') para resolver los desafios (Señalizados como '$') y asi escapar!")
    print("Iniciarás con una totalidad de 1000 puntos a tu favor. Si necesitas ayuda, podés usar pistas, pero estas te costarán puntos.")
    print("Cada acción que realices también te costará puntos, por lo que deberas ser cuidadoso con tus movimientos.")
    print("Si te quedas sin puntos, perderas el juego. Si lográs descifrar el desafío, ganarás puntos. Una vez cumplidos todos los desafíos, en caso de que lo hagas, habrás ganado el juego.")
    print("Buena suerte, la vas a necesitar.")

def registrar_puntos(user, puntos):
    '''
    Actualiza los puntos de un usuario si el nuevo puntaje es mayor al existente
    '''
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
    '''
    Muestra el ranking de un jugador específico
    '''
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
    '''
    Muestra los primeros o últimos 10 usuarios del ranking
    primeros: True para mejores puntuaciones, False para peores
    '''
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
    '''
    Menú principal del ranking
    '''
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
    '''
    Programa Principal
    '''
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