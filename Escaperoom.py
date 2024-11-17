import random
import re
import json
import os

terreno = " "
vaciarConsola = "\n" * 50

def GenerarTerreno(mapa,alturaMin,alturaMax,anchoMin,anchoMax):
    '''
    Genera el terreno de un mapa vacio pasado por parametro, el tipo de terreno sera definido por una variable global
    el ancho y la altura sera un numero entre los minimos y maximos pasados por parametros.
    '''
    altoDelMapa = random.randint(alturaMin,alturaMax)
    anchoMinimoDelMapa = random.randint(anchoMin,anchoMax) 

    for _ in range(altoDelMapa):
        mapa.append([terreno for _ in range(anchoMinimoDelMapa)])
        
        
        

def GenerarObjeto(mapa,objeto,cantidad):
    '''
    Recibe un mapa (matriz), un objeto (caracter string) cantidad (int) Y genera en x posiciones aleatoria del mapa el objeto pasado por parametro
    x es definida por cantidad
    '''
    columnaSpawn = random.randint(0,len(mapa)-1) 
    filaSpawn = random.randint(0,len(mapa[columnaSpawn])-1)
    for _ in range(cantidad):
        while(mapa[columnaSpawn][filaSpawn] != terreno): 
            columnaSpawn = random.randint(0,len(mapa)-1) 
            filaSpawn = random.randint(0,len(mapa[columnaSpawn])-1)
        mapa[columnaSpawn][filaSpawn] = objeto

def GenerarMapa(alturaMin,alturaMax,anchoMin,anchoMax):
    '''
    Genera un mapa de juego con una altura y un ancho, minimo y maximo
    Ademas de rellenar el mapa con un terreno, un personaje, almenos un candado y almenos una pista.
    '''
    mapa = []
    #terreno = " "
    personaje = "O"
    candados = "$"
    pistas = "#"
    objetos = [personaje,candados,pistas]
    GenerarTerreno(mapa,alturaMin,alturaMax,anchoMin,anchoMax)
    for i in objetos:
        if(i == personaje):
            GenerarObjeto(mapa,i,1)
        else:
            GenerarObjeto(mapa,i,2) 
    return mapa

def RenderizarMapa(mapa):
    '''
    Muestra la salida por consola de una mapa (matriz) recibido por parametro
    '''
    for fila in mapa:
        print(fila)

def LeerAccion():
    '''
    Lee de la entrada un string ingresado por el usuario, verifica que este dentro de las acciones validas ('w', 'a', 's', 'd','menu')
    y devuelve la accion validada
    '''
    accionesValidas = {'w', 'a', 's', 'd','menu'}
    accion = input("Elija una acción ('W', 'A', 'S', 'D' para el movimiento o 'menu' para salir al menu): ").lower()
    while accion not in accionesValidas:
        print("Acción no válida. Intentálo de nuevo.")
        accion = input("Elija una acción ('W', 'A', 'S', 'D' para el movimiento o 'menu' para salir al menu): ").lower()
    return accion

def ValidarMovimiento(mapa, posicion_actual, accion):
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

def GetIndiceObjeto(mapa,objeto):
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

def MoverObjeto(mapa,x,y,objeto):
    '''
    Mueve a un objeto recibido por parametro dentro de la matriz mapa tambien recibida por parametro, tantas veces en x como diga el parametro
    y tantas veces en y como diga el parametro.
    '''
    #terreno = " "
    coordenadasObjeto = GetIndiceObjeto(mapa,objeto)
    mapa[coordenadasObjeto[0]][coordenadasObjeto[1]] = terreno
    mapa[coordenadasObjeto[0]+y*(-1)][coordenadasObjeto[1]+x] = objeto

def AccionPersonaje(mapa,accion): 
    '''
    Recibe un mapa por parametro y una accion, (w,a,s,d) llama a la funcion MoverObjeto, para mover al personaje segun la accion elegida
    '''
    personaje = "O"
    
    if  (accion == "w"):
        MoverObjeto(mapa,0,1,personaje)
    elif(accion == "s"):
        MoverObjeto(mapa,0,-1,personaje) 
    elif(accion == "a"):
        MoverObjeto(mapa,-1,0,personaje)
    elif(accion == "d"):
        MoverObjeto(mapa,1,0,personaje)


def MenuPrincipal(user):
    '''
    Funcion que se encarga de mostrar el menu principal del juego
    '''
    print()
    print(f"{user} Bienvenido a UadEscape")
    print("1. Comenzar Juego")
    print("2. Ranking de puntos")
    print("3. Como Jugar")
    print("4. Salir")
 

def PedirUserName(jugador_numero=0):
    '''
    Funcion que recibe por parametro el numero de jugado que va a jugar , pedir al usuario que ingrese el nombre, y generarlo
    devuelve el nombre de usuario validado 
    '''
    patron = r"^[a-zA-Z]{3,9}$"
    Bienvenida = lambda x : x if(x == 0) else print(f"Bienvenido Jugador {jugador_numero}") 
    Bienvenida(jugador_numero)
    username = input(f"Jugador, ingrese un nombre de usuario (3-9 caracteres, sin números o caracteres especiales): ")
    nombreValido = re.match(patron, username)

    while nombreValido is None:
        if nombreValido is None:
            print(f"Nombre no válido. Inténtelo de nuevo.")
        username = input(f"Jugador, por favor, ingrese un nombre de usuario: ")
        nombreValido = re.match(patron, username)
    return username

def PedirUserNames():
    '''Funcion auxiliar que  se encarga de pedir y generar dos usernames, para dos jugadores, los devuelve'''
    username1 = PedirUserName(1)
    username2 = PedirUserName(2)
    return username1, username2

def GenerarUser(username):
    '''
    Funcion que genera el registro del usuario nuevo generando una id, y asociandole el nombre de usuario.
    '''
    try:
        with open("userRepository.json","r") as userRepositoryArchivo:
            userRepository=json.load(userRepositoryArchivo)
        userRepository = list(userRepository)

        while any(user['Username'] == username for user in userRepository):
            print(f"El nombre de usuario ya está en uso. Intente con otro.")
            username= PedirUserName()
        
        with open("userRepository.json","w") as userRepositoryArchivo:
            userRepository.append(dict(Username=username,Id = GenerarId(userRepository),Puntos = 0 ))
            json.dump(userRepository,userRepositoryArchivo)
    except IOError:
        print("Error, no se pudo abrir el archivo")
    except FileNotFoundError:
        print("Error, no se encontro el archivo")

        


def GenerarId(userRepository):
    '''
    Funcion que genera un id para un usuario, a partir del ultimo id ingresado
    '''
    id = 0
    if(len(userRepository) != 0):
        ultimo = len(userRepository)-1 
        id = userRepository[ultimo]['Id'] + 1
    return id

def PedirOpcion(min,max):
    '''
    Funcion que se encarga de pedir un numero al usuario entre un minimo y un maximo, luego valida y devuelve la opcion elegida
    '''
    opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
    
    while opcion < min or opcion > max:
        print("Error")
        opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
    
    print()
    return opcion

def MostrarDificultades():
    '''
    Funcion que se encarga de mostrar los distintos niveles de dificultad
    '''
    print("Niveles de dificultad: ")
    print("1. Facil")
    print("2. Normal")
    print("3. Dificil")
    

def NivelDeDificultad():
    '''
    Funcion que se encarga de pedirle al usuario que ingrese que dificultad quiere elegir y que devuelve las distintas tematicas segun la dificutald
    '''
    MostrarDificultades()
    opcion = PedirOpcion(1,3)

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

def ElegirTematica():
    '''
    Funcion que se encarga de pedirle a un usuario que ingrese que tematica quiere jugar, segun que dificultad anteriormente eligio.
    Ademas se le mostrara una introduccion a la tematica elegida. Y luego se devuelve la tematica elegida
    '''
    dificultad = NivelDeDificultad()
    print("Temáticas disponibles:")
    for i, tematica in enumerate(dificultad, 1):
        print(f"{i}: {tematica}")

    seleccion = PedirOpcion(1, len(dificultad))
    MostrarIntroduccionALaTematica(dificultad[seleccion - 1])
    return dificultad[seleccion - 1]

def cargar_introducciones():
    try:
        with open("introducciones.json","r") as archivo:
            introducciones = json.load(archivo)
        return introducciones
    except FileNotFoundError:
        print("Error, no se encontro el archivo de las introducciones")
        return {}

def MostrarIntroduccionALaTematica(tematica):   
    '''
    Funcion que se encarga de mostrar la introduccion a una tematica
    '''
    introducciones = cargar_introducciones()
    introduccion = introducciones.get(tematica, "Introducción no disponible.")
    print(introduccion)

    print("¿Deseas comenzar el juego o salir?")
    print("1. Comenzar Juego")
    print("2. Salir")
    seleccion = PedirOpcion(1, 2)
    if seleccion == 1:
        print("Comenzando juego...")
    elif seleccion == 2:
        print("Saliendo...")
        exit()
    else:
        print("Por favor, ingresá una opción válida.")

def InicializarPistas():
   try:
    with open("pistas.json", "r") as archivo:
        pistas = json.load(archivo)
    pistas_usadas = {key: [] for key in pistas.keys()}
    return pistas, pistas_usadas
   except FileNotFoundError:
       print("No se encuentra el archivo de las pistas")
       return {}

def MostrarPista(tematica, pistas, pistas_usadas):
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

def MostrarDesafio(tematica, desafios, desafios_usados):
    '''
    Funcion que recibe una tematica, desafios para la misma, y los desafios que fueron usados,
      se encarga de mostrar un desafio aleatorio de los disponibles
    '''
    Fallo = True
    if tematica in desafios:
        disponibles = [desafios for desafios in desafios[tematica] if desafios not in desafios_usados[tematica]]
        
        if disponibles:
            desafios = random.choice(disponibles) 
            while Fallo:
                desafio = list(desafios.split("|"))
                print(f"{desafio[1]}")
                opcion = PedirOpcion(1,3)
                if(int(desafio[0])==opcion):
                    Fallo = False
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

def InicializarDesafios():
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

def ModificarPuntos(puntos, accion):
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

def MapaParaTematica(tematica):
    '''
    Genera un mapa aleatorio para una tematica recibida por parametro
    '''
    mapa = []
    if(tematica == "Breaking Bad" or tematica == "Muerte Anunciada"):
        mapa = GenerarMapa(4,5,4,6) 
        probabilidadFin = random.randint(40,100) # 83,3 %
        habitacionesMax = 2
    elif(tematica == "Psiquiátrico" or tematica == "La Casa de Papel"):
        mapa = GenerarMapa(7,8,5,7)
        probabilidadFin = random.randint(-20,100) # 41,6 %
        habitacionesMax = 3
    elif(tematica == "Sherlock Holmes" or tematica == "Misión Gubernamental"):
        mapa = GenerarMapa(9,10,5,8)
        probabilidadFin = random.randint(-100,100) # 25 %
        habitacionesMax = 4
    return mapa, probabilidadFin, habitacionesMax

def ContieneElementos(lista1, lista2):
    ''' Verifica si lista1 esta en lista2 en forma de secuencia'''
    #Se recorre en el largo de lista2 (Para poder recorrer toda la segunda lista), se le resta el largo de la primera lista (para poder mirar desde i + el largo de lista1 sin pasarnos del indice)
    for i in range(0,len(lista2) - len(lista1) + 1,2):
        if lista2[i:i+len(lista1)] == lista1: 
        # Aca se extrae de la lista 2 en indice i, hasta i + el largo de lista1, si esa extraccion es igual a la lista1, entnces la lista 1 esta en la lista dos de forma secuencial
            return True
    return False

def ComenzarJuego(tematica,puntos = 0,nroHabitacion = 1):
    '''
    Funcion que provoca que el juego comienze, recibe la tematica por parametro devuelve la cantidad de puntos que consiguio el usuario
    '''
    puntos = 1000 + puntos
    Escapo = False
    pistas, pistas_usadas = InicializarPistas()
    desafios, desafios_usadas =InicializarDesafios()
    mapa,probabilidadFin,habitacionesMax = MapaParaTematica(tematica)
    if (probabilidadFin > 50 or nroHabitacion == habitacionesMax):
        habitacionFinal = True
    else:
        habitacionFinal = False 
    objetos = ["#","$"]
    for i in objetos:
        if(i=="#"):
            indicesPistas = GetIndiceObjeto(mapa,i) 
        else:
            indicesCandados = GetIndiceObjeto(mapa,i)
            cantCandandos = len(indicesCandados)//2
    
    while not Escapo:
        posicion_actual = GetIndiceObjeto(mapa,"O")
        if(len(pistas_usadas.get(tematica)) == 0):
            print("Cuando encuentres una pista aparecera aca")
        else:
            print(pistas_usadas.get(tematica))
            
        
        if(ContieneElementos(posicion_actual, indicesPistas)): 
            print("----PISTA ENCONTRADA----")
            MostrarPista(tematica, pistas, pistas_usadas)
            puntos = ModificarPuntos(puntos, "usar_pista")
            indicesPistas.remove(posicion_actual[0])
            indicesPistas.remove(posicion_actual[1])
        elif(ContieneElementos(posicion_actual, indicesCandados)):
            MostrarDesafio(tematica, desafios, desafios_usadas)
            cantCandandos -= 1
            puntos = ModificarPuntos(puntos, "completar_desafio")
            indicesCandados.remove(posicion_actual[0])
            indicesCandados.remove(posicion_actual[1])
            if(cantCandandos == 0):
                if(habitacionFinal == True):
                    print("------ Felicitaciones, lograste escapar.... Por ahora.... ------")
                    Escapo = True
                else:
                    print("------ Entrando en la siguiente habitacion.... ------")
                    puntos, Escapo = ComenzarJuego(tematica,puntos,nroHabitacion+1)

        if (not Escapo):        
            RenderizarMapa(mapa)
            accion = LeerAccion()
            print(vaciarConsola)
            if accion == "menu":
                print("Saliendo al menu principal...")
                Escapo = True
                puntos = 0
            elif ValidarMovimiento(mapa, posicion_actual, accion):   
                AccionPersonaje(mapa,accion)
                puntos = ModificarPuntos(puntos,accion)
                print(f"Puntos actuales: {puntos}")
            else:
                print("Movimiento inválido: fuera de los límites del mapa.")
        
    return puntos, Escapo

def Instrucciones():
    '''
    Muestra las instrucciones para poder jugar al juego
    '''
    os.system('clear')  # Limpiar la consola
    print("Comenzaras tu aventura en un mapa donde podras moverte libremente, tu personaje (Señalizado como una 'O') debera recoger pistas (Señalizadas como '#') para resolver los desafios (Señalizados como '$') y asi escapar!")
    print("Iniciarás con una totalidad de 1000 puntos a tu favor. Si necesitas ayuda, podés usar pistas, pero estas te costarán puntos.")
    print("Cada acción que realices también te costará puntos, por lo que deberas ser cuidadoso con tus movimientos.")
    print("Si te quedas sin puntos, perderas el juego. Si lográs descifrar el desafío, ganarás puntos. Una vez cumplidos todos los desafíos, en caso de que lo hagas, habrás ganado el juego.")
    print("Buena suerte, la vas a necesitar.")

def registrarPuntos(user,puntos):
    try:
        with open("userRepository.json",mode="r") as userRepositoryArchivo:
            userRepository=json.load(userRepositoryArchivo)
        
        jugador = list(filter(lambda x: x['Username']==user,userRepository))
        if(puntos > jugador[0]["Puntos"]):
            for users in userRepository:
                if(users['Id'] == jugador[0]['Id'] ):
                    users['Puntos'] = puntos
            
            with open("userRepository.json","w") as userRepositoryArchivo:
                json.dump(userRepository,userRepositoryArchivo)
    except IOError:
        print("Error, no se pudo abrir el archivo")
    except FileNotFoundError:
        print("Error, no se encontro el archivo")


def PrimerosUltimosRanking(usuarios,primeros):
    usuariosOrdenados = list(sorted(usuarios,key= lambda x: x["Puntos"],reverse=primeros))
    if(primeros):
        x=1
    else:
        x=len(usuariosOrdenados)
    
    rank = usuariosOrdenados[:10]
    
    print(f"\tPuesto\t - \tNombre\t - \tPuntuacion Máxima")
    for users in rank:
        print(f"\t{x}\t - \t{users['Username']}\t - \t{usuarios['Puntos']}")
        if(primeros):
            x+=1
        else:
            x-=1

def RankingJugador(users,username = None):
    if(username is None):
        username = PedirUserName()

    jugador = list(filter(lambda x: x['Username']==username,users))
    try:
        print(f"{jugador[0]['Username']} tiene {jugador[0]['Puntos']} de puntuacion maxima.")
    except:
        print("El jugador no existe")

def Ranking(user):
    try:
        with open("userRepository.json",mode="r") as userRepositoryArchivo:
            userRepository=json.load(userRepositoryArchivo)
            RankList = [user for user in list(userRepository)]
    except IOError:
        print("Error, no se pudo abrir el archivo")
    except FileNotFoundError:
        print("Error, no se encontro el archivo")
    
    opcion = 0
    while(opcion != 5):
        os.system('clear')
        print()
        print("1. Ver mejores puntuaciones.")
        print("2. Buscar jugador.")
        print("3. Ver peores puntuaciones.")
        print("4. Mi mejor puntuacion.")
        print("5. Salir.")
        opcion = PedirOpcion(1,5)
        print()

        if(opcion == 1):
            PrimerosUltimosRanking(RankList,True)
        elif (opcion == 2):
            RankingJugador(RankList)
        elif (opcion == 3):
            PrimerosUltimosRanking(RankList,False)
        elif (opcion == 4):
            RankingJugador(RankList,user)
        elif (opcion == 5):
            print("Saliendo...")
        else:
            print("Opcion inexistente.")


def main():
    '''
    Programa Principal
    '''
    user = PedirUserName()
    GenerarUser(user)
    jugando = True
    tematica = 0
    while(jugando):
        os.system('clear') 
        MenuPrincipal(user)
        opcion = PedirOpcion(1,4)
        if(opcion == 1):
            tematica = ElegirTematica()
            puntos, escapo = ComenzarJuego(tematica)
            if puntos > 0 and escapo:
                print("Felicidades, escapaste")
                registrarPuntos(user,puntos)
            else:
                print("Abandonaste pero no pasa nada, suerte la proxima!")
        elif (opcion == 2):
            Ranking(user)
        elif (opcion == 3):
            Instrucciones()
        elif (opcion == 4):
            print("Gracias por Jugar! Saliendo...")
            jugando = False
    
main()