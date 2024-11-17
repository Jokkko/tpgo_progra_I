import random
import re
import json
import os

terreno = " "
vaciar_consola = "\n" * 50

def generar_terreno(mapa,altura_min,altura_max,ancho_min,ancho_max):
    '''
    Genera el terreno de un mapa vacio pasado por parametro, el tipo de terreno sera definido por una variable global
    el ancho y la altura sera un numero entre los minimos y maximos pasados por parametros.
    '''
    alto_del_mapa = random.randint(altura_min,altura_max)
    ancho_minimo_del_mapa = random.randint(ancho_min,ancho_max) 

    for _ in range(alto_del_mapa):
        mapa.append([terreno for _ in range(ancho_minimo_del_mapa)])
        
def generar_objeto(mapa,objeto,cantidad):
    '''
    Recibe un mapa (matriz), un objeto (caracter string) cantidad (int) Y genera en x posiciones aleatoria del mapa el objeto pasado por parametro
    x es definida por cantidad
    '''
    columna_spawn = random.randint(0,len(mapa)-1) 
    fila_spawn = random.randint(0,len(mapa[columna_spawn])-1)
    for _ in range(cantidad):
        while(mapa[columna_spawn][fila_spawn] != terreno): 
            columna_spawn = random.randint(0,len(mapa)-1) 
            fila_spawn = random.randint(0,len(mapa[columna_spawn])-1)
        mapa[columna_spawn][fila_spawn] = objeto

def generar_mapa(altura_min,altura_max,ancho_min,ancho_max):
    '''
    Genera un mapa de juego con una altura y un ancho, minimo y maximo
    Ademas de rellenar el mapa con un terreno, un personaje, almenos un candado y almenos una pista.
    '''
    mapa = []
    personaje = "O"
    candados = "$"
    pistas = "#"
    objetos = [personaje,candados,pistas]
    generar_terreno(mapa,altura_min,altura_max,ancho_min,ancho_max)
    for i in objetos:
        if(i == personaje):
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

def leer_accion():
    '''
    Lee de la entrada un string ingresado por el usuario, verifica que este dentro de las acciones validas ('w', 'a', 's', 'd','menu')
    y devuelve la accion validada
    '''
    acciones_validas = {'w', 'a', 's', 'd','menu'}
    accion = input("Elija una acción ('W', 'A', 'S', 'D' para el movimiento o 'menu' para salir al menu): ").lower()
    while accion not in acciones_validas:
        print("Acción no válida. Intentálo de nuevo.")
        accion = input("Elija una acción ('W', 'A', 'S', 'D' para el movimiento o 'menu' para salir al menu): ").lower()
    return accion

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
    mapa[coordenadas_objeto[0]][coordenadas_objeto[1]] = terreno
    mapa[coordenadas_objeto[0]+y*(-1)][coordenadas_objeto[1]+x] = objeto

def accion_personaje(mapa,accion): 
    '''
    Recibe un mapa por parametro y una accion, (w,a,s,d) llama a la funcion mover_objeto, para mover al personaje segun la accion elegida
    '''
    personaje = "O"
    
    if  (accion == "w"):
        mover_objeto(mapa,0,1,personaje)
    elif(accion == "s"):
        mover_objeto(mapa,0,-1,personaje) 
    elif(accion == "a"):
        mover_objeto(mapa,-1,0,personaje)
    elif(accion == "d"):
        mover_objeto(mapa,1,0,personaje)


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
    Funcion que genera el registro del usuario nuevo generando una id, y asociandole el nombre de usuario.
    '''
    try:
        ruta_archivo_user = os.path.join(os.getcwd(), "Data", "user_repository.json")
        try:
            with open(ruta_archivo_user, "r") as user_repository_archivo:
                user_repository = json.load(user_repository_archivo)
        except (FileNotFoundError, json.JSONDecodeError):
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

        with open(ruta_archivo_user, "w") as archivo:
            json.dump(user_repository, archivo, indent=4)

        print(f"Usuario '{username}' registrado con éxito.")

    except (FileNotFoundError, IOError) as e:
        print(f"Error de archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


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
        print("Error")
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
    Carga las pistas desde un archivo JSON ubicado en la carpeta Data.
    Si el archivo no existe, retorna un diccionario vacío.
    '''
    try:
        ruta_archivo_pistas = os.path.join(os.getcwd(), "Data", "pistas.json")
        with open(ruta_archivo_pistas, "r") as pistas_archivo:
            pistas = json.load(pistas_archivo)
        pistas_usadas = {key: [] for key in pistas.keys()}
        return pistas, pistas_usadas

    except FileNotFoundError:
        print("Error: No se encuentra el archivo de las pistas.")
        return {}, {}
    except json.JSONDecodeError:
        print("Error: El archivo de pistas tiene un formato inválido.")
        return {}, {}
    except Exception as e:
        print(f"Error inesperado: {e}")
        return {}, {}

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
    Funcion que se encarga de incializar los distintos desafios para que el usuario pueda utilizarlos en el juego.
    Devuelve los desafios disponibles y los jugados
    '''
    try:
        with open("desafios.json","r") as archivo:
            desafios = json.load(archivo)
        desafios_usados = {key: [] for key in desafios.keys()}
        return desafios, desafios_usados
    except FileNotFoundError:
        print("No se encontro el archivo de los desafios")
        return {}

def modificar_puntos(puntos, accion):
    '''
    Modifica los puntos pasados por parametros segun la accion pasada por parametros, luego devuelve los puntos modificados
    '''
    if accion == "usar_pista":
        puntos -= 100
    elif accion == "completar_desafio":
        puntos += 500
    elif accion == "accion_correcta":
        puntos += 10
    else:
        puntos -= 10
    return puntos

def mapa_para_tematica(tematica):
    '''
    Genera un mapa aleatorio para una tematica recibida por parametro
    '''
    mapa = []
    if(tematica == "Breaking Bad" or tematica == "Muerte Anunciada"):
        mapa = generar_mapa(4,5,4,6) 
        probabilidad_fin = random.randint(40,100) # 83,3 %
        habitaciones_max = 2
    elif(tematica == "Psiquiátrico" or tematica == "La Casa de Papel"):
        mapa = generar_mapa(7,8,5,7)
        probabilidad_fin = random.randint(-20,100) # 41,6 %
        habitaciones_max = 3
    elif(tematica == "Sherlock Holmes" or tematica == "Misión Gubernamental"):
        mapa = generar_mapa(9,10,5,8)
        probabilidad_fin = random.randint(-100,100) # 25 %
        habitaciones_max = 4
    return mapa, probabilidad_fin, habitaciones_max

def contiene_elementos(lista1, lista2):
    ''' Verifica si lista1 esta en lista2 en forma de secuencia'''
    #Se recorre en el largo de lista2 (Para poder recorrer toda la segunda lista), se le resta el largo de la primera lista (para poder mirar desde i + el largo de lista1 sin pasarnos del indice)
    for i in range(0,len(lista2) - len(lista1) + 1,2):
        if lista2[i:i+len(lista1)] == lista1: 
        # Aca se extrae de la lista 2 en indice i, hasta i + el largo de lista1, si esa extraccion es igual a la lista1, entnces la lista 1 esta en la lista dos de forma secuencial
            return True
    return False

def comenzar_juego(tematica,puntos = 0,nro_habitacion = 1):
    '''
    Funcion que provoca que el juego comienze, recibe la tematica por parametro devuelve la cantidad de puntos que consiguio el usuario
    '''
    puntos = 1000 + puntos
    escapo = False
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
            print(vaciar_consola)
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
        
    return puntos, escapo

def instrucciones():
    '''
    Muestra las instrucciones para poder jugar al juego
    '''
    os.system('clear')  # Limpiar la consola
    print("Comenzaras tu aventura en un mapa donde podras moverte libremente, tu personaje (Señalizado como una 'O') debera recoger pistas (Señalizadas como '#') para resolver los desafios (Señalizados como '$') y asi escapar!")
    print("Iniciarás con una totalidad de 1000 puntos a tu favor. Si necesitas ayuda, podés usar pistas, pero estas te costarán puntos.")
    print("Cada acción que realices también te costará puntos, por lo que deberas ser cuidadoso con tus movimientos.")
    print("Si te quedas sin puntos, perderas el juego. Si lográs descifrar el desafío, ganarás puntos. Una vez cumplidos todos los desafíos, en caso de que lo hagas, habrás ganado el juego.")
    print("Buena suerte, la vas a necesitar.")

def registrar_puntos(user, puntos):
    '''
    Actualiza los puntos de un usuario en el archivo 'user_repository.json' si el nuevo puntaje es mayor al existente.
    '''
    try:
        ruta_archivo_puntos = os.path.join(os.getcwd(), "Data", "user_repository.json")
        with open(ruta_archivo_puntos, mode="r") as user_repository_archivo:
            user_repository = json.load(user_repository_archivo)

        jugador = next((u for u in user_repository if u['Username'] == user), None)
        if jugador:
            if puntos > jugador["Puntos"]:
                jugador["Puntos"] = puntos
                with open(ruta_archivo_puntos, "w") as user_repository_archivo:
                    json.dump(user_repository, user_repository_archivo, indent=4)
                print(f"Puntos actualizados para el usuario '{user}': {puntos}")
            else:
                print(f"El usuario '{user}' ya tiene un puntaje mayor o igual: {jugador['puntos']}")
        else:
            print(f"Error: El usuario '{user}' no existe en el repositorio.")

    except FileNotFoundError:
        print("Error: No se encontró el archivo 'user_repository.json'.")
    except json.JSONDecodeError:
        print("Error: El archivo 'user_repository.json' tiene un formato inválido.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def primeros_ultimos_anking(usuarios,primeros):
    usuarios_ordenados = list(sorted(usuarios,key= lambda x: x["Puntos"],reverse=primeros))
    if(primeros):
        x=1
    else:
        x=len(usuarios_ordenados)
    
    rank = usuarios_ordenados[:10]
    
    print(f"\tPuesto:\t - \tNombre:\t - \tPuntuacion Máxima:")
    for users in rank:
        print(f"\t{x}\t - \t{users['username']}\t - \t{usuarios['puntos']}")
        if(primeros):
            x+=1
        else:
            x-=1

def ranking_jugador(users,username = None):
    if(username is None):
        username = pedir_user_name()

    jugador = list(filter(lambda x: x['Username']==username,users))
    try:
        print(f"{jugador[0]['Username']} tiene {jugador[0]['Puntos']} de puntuacion maxima.")
    except:
        print("El jugador no existe")

def ranking(user):
    try:
        ruta_archivo_ranking = os.path.join(os.getcwd(), "Data", "user_repository.json")
        with open(ruta_archivo_ranking, mode="r") as user_repository_archivo:
            user_repository = json.load(user_repository_archivo)
            rank_list = user_repository
    except (IOError, FileNotFoundError):
        print("Error al abrir o encontrar el archivo 'user_repository.json'.")
        return
    
    opcion = 0
    while(opcion != 5):
        os.system('clear')
        print()
        print("1. Ver mejores puntuaciones.")
        print("2. Buscar jugador.")
        print("3. Ver peores puntuaciones.")
        print("4. Mi mejor puntuacion.")
        print("5. Salir.")
        opcion = pedir_opcion(1,5)
        print()

        if(opcion == 1):
            primeros_ultimos_anking(rank_list,True)
        elif (opcion == 2):
            ranking_jugador(rank_list)
        elif (opcion == 3):
            primeros_ultimos_anking(rank_list,False)
        elif (opcion == 4):
            ranking_jugador(rank_list,user)
        elif (opcion == 5):
            print("Saliendo...")
        else:
            print("Opcion inexistente.")


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