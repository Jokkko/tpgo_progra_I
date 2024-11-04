import random
import re
import json

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
    #muestre las opciones del menu
    #se puede usar center aca
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
    '''
    Funcion que se encarga de incializar las distintas pistas para que el usuario pueda utilizarlas en el juego. Devuelve las pistas disponibles
    y las usadas
    '''
    pistas = {
        "Breaking Bad": [
            "Busca en el laboratorio un objeto que brilla en la oscuridad.",
            "El equipo de protección personal es clave para el éxito. Revisa las cajas.",
            "Las fórmulas están escondidas en los documentos; no olvides mirar en las carpetas.",
            "La química puede ser peligrosa. Estudia los frascos con atención."
        ],
        "Muerte Anunciada": [
            "Revisa la habitación donde se celebró la fiesta, hay más de lo que parece.",
            "Algunos invitados saben más de lo que dicen. Escucha con atención.",
            "Los periódicos antiguos pueden contener pistas sobre el asesinato.",
            "Un objeto olvidado podría ser la clave para resolver el misterio."
        ],
        "Psiquiátrico": [
            "Las habitaciones son un laberinto; sigue las marcas en la pared.",
            "El diario del último paciente podría revelarte información crucial.",
            "Revisa los cuadros; algunos pueden esconder secretos oscuros."
        ],
        "La Casa de Papel": [
            "El plano del banco tiene detalles que podrían ser útiles. No lo ignores.",
            "Cada miembro del equipo tiene una habilidad única; úsalas a tu favor.",
            "Hay cámaras en todo el lugar; busca la manera de desactivarlas."
        ],
        "Sherlock Holmes": [
            "La carta en la mesa contiene un mensaje cifrado; decodifícalo.",
            "No todos los sospechosos son lo que parecen; investiga sus coartadas."
        ],
        "Misión Gubernamental": [
            "Un dispositivo escondido puede cambiar el curso de la misión; búscalo.",
            "Las comunicaciones pueden estar interceptadas. Encuentra el canal seguro."
        ]
    }

    pistas_usadas = {key: [] for key in pistas.keys()}
    
    return pistas, pistas_usadas

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
    desafios = {
        "Breaking Bad": [
            "2|Entras en el laboratorio y en la oscuridad comienzas a mirar tu alrededor ¿Que haces?\n1.Prender la luz\t\t2.Mirar a tu alrededor\t\t3.Gritar",
            "2|Encuentras unas cajas que puedes abrir, al revisarlas encuentras distintos objetos, ¿Cual agarras?\n1.Libro de cocina\t\t2.Equipo de proteccion personal\t\t3.Efectivo",
            "3|En el escritorio encontras muchas cosas tiradas, ¿Cual agarras? \n1.Una bolsa con cristales extraños\t\t2.Libros de ciencia\t\t3.Unas carpetas con documentos",
            "2|En un costado encontras muchas cosas de quimica, ¿Que investigas? \n1.Anotaciones con formulas\t\t2.Unos frascos con liquido brillante\t\t3.Un mechero"
        ],
        "Muerte Anunciada": [
            "2|Estas en una habitacion con 3 puertas, estas dan a otras habitaciones ¿Cual Investigamos? \n1.El baño\t\t2.Una habitacion donde parece que hubo una fiesta\t\t3.Una habitacion antigua",
            "2|En la habitacion hay mucha gente, ¿Que deseas hacer? \n1.Hablar con ellos\t\t2.Escuchar sus converzaciones\t\t3.Gritarles que hagan silencio",
            "3|Miras al suelo y visualizas muchas cosas tiradas, ¿Que agarras? \n1.Latas de cerveza vacias\t\t2.Posters antiguos\t\t3.Unos periodicos igual de antiguos",
            "2|Entras en una habitacion que parece muy antigua y encontras diversos objetos, ¿Con cual te quedas?. \n1.Una pelota de basket\t\t2.Un objeto extraño que parece abandonado\t\t3.Un peluche destrozado"
        ],
        "Psiquiátrico": [
            "3|Estas dentro de una habitacion con muchas puertas ¿Que haces para no perderte?\n1.Entras siempre en la habitacion de la derecha\t\t2.Haces izquierda derecha en bucle\t\t3.Seguis unas marcas en la pared",
            "1|Encontraste los diarios de los distintos pacientes, ¿Cual agarras?\n1.El del ultimo paciente\t\t2.Uno aleatorio\t\t3.El diario del primer paciente",
            "1|Miras la pared y observas algunas cosas en la pared, ¿Alguna hara algo? \n1.Mover los cuadros\t\t2.Mirar por la ventana\t\t3.Intentar romper la ventana"
        ],
        "La Casa de Papel": [
            "3|Tenemos que encontrar una forma de escapar y tenemos solo 3 objetos, ¿Que podriamos usar para escapar?\n1.Fuerza Bruta \t\t2.Usar a los rehenes \t\t3.El plano del banco",
            "1|Hay unas rejas adelante sin embargo parecen debiles, ¿Como podriamos romperlas?\n1.Pedirle a Helsinki que las rompa\t\t2.Dispararles \t\t3.Darles una patada ",
            "1|El pasillo esta lleno de guardias, ¿Que hacemos?\n1.Entrar en la sala de camaras \t\t2.Seguir por el pasillo con sigilo \t\t3.Quedarse escondido"
        ],
        "Sherlock Holmes": [
            "3|Hay una carta con un mensaje, dice '\n murcielago\n 0123456789\n y abajo pone este texto b9t9n 70724669' ¿Que boton presionamos?\n1.El boton Turquesa \t\t2.El boton Celeste \t\t3.El boton Amarillo",
            "3|El primer sospechoso dijo que estaba en su casa. Sin embargo, no me convence ¿Que deberia hacer?\n1.Creerle \t\t2.Obligarle a decir la verdad \t\t3.Investigar a fondo "
        ],
        "Misión Gubernamental": [
            "3|Te encuentras en la habitacion, y ves un escritorio, te parece un buen comienzo ¿Que haces?\n1.Revisas los cajones \t\t2.Abres las puertas del escritorio \t\t3.Miras por abajo",
            "3|En esta hoja dice que no hay ningun canal seguro, sin embargo algo me dice lo contrario ¿Que canal probamos?\n1.D4NG3R \t\t2.3ST3 N0 \t\t3.S4F3"
        ]
    }

    desafios_usados = {key: [] for key in desafios.keys()}
    
    return desafios, desafios_usados

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
    elif(tematica == "Psiquiátrico" or tematica == "La Casa de Papel"):
        mapa = GenerarMapa(7,8,5,7)
    elif(tematica == "Sherlock Holmes" or tematica == "Misión Gubernamental"):
        mapa = GenerarMapa(9,10,5,8)
    return mapa

def ContieneElementos(lista1, lista2):
    ''' Verifica si lista1 esta en lista2 en forma de secuencia'''
    #Se recorre en el largo de lista2 (Para poder recorrer toda la segunda lista), se le resta el largo de la primera lista (para poder mirar desde i + el largo de lista1 sin pasarnos del indice)
    for i in range(0,len(lista2) - len(lista1) + 1,2):
        if lista2[i:i+len(lista1)] == lista1: 
        # Aca se extrae de la lista 2 en indice i, hasta i + el largo de lista1, si esa extraccion es igual a la lista1, entnces la lista 1 esta en la lista dos de forma secuencial
            return True
    return False

def ComenzarJuego(tematica):
    '''
    Funcion que provoca que el juego comienze, recibe la tematica por parametro devuelve la cantidad de puntos que consiguio el usuario
    '''
    puntos = 1000
    Escapo = False
    pistas, pistas_usadas = InicializarPistas()
    desafios, desafios_usadas =InicializarDesafios()
    mapa = MapaParaTematica(tematica)
    objetos = ["#","$"]
    for i in objetos:
        if(i=="#"):
            indicesPistas = GetIndiceObjeto(mapa,i) 
        else:
            indicesCandados = GetIndiceObjeto(mapa,i)
    
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
        elif(ContieneElementos(posicion_actual, indicesCandados)):
            MostrarDesafio(tematica, desafios, desafios_usadas)
            puntos = ModificarPuntos(puntos, "completar_desafio")
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
    return puntos

def Instrucciones():
    '''
    Muestra las instrucciones para poder jugar al juego
    '''
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


def FirstsLastsRanking(users,firsts):
    usersOrdered = list(sorted(users,key= lambda x: x["Puntos"],reverse=firsts))
    if(firsts):
        x=1
    else:
        x=len(usersOrdered)
    
    rank = usersOrdered[:10]
    
    print(f"\tPuesto\t - \tNombre\t - \tPuntuacion Máxima")
    for users in rank:
        print(f"\t{x}\t - \t{users['Username']}\t - \t{users['Puntos']}")
        if(firsts):
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

'''
def Last10Ranking(users):
    usersOrdered = list(sorted(users,key= lambda x: x["Puntos"]))
    x=len(usersOrdered)
    last10 = usersOrdered[:10]
    print(f"# - Nombre - Puntuacion Máxima")
    for users in last10:
        print(f"{x} - {users['Username']} - {users['Puntos']}")
        x-=1
'''

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
        print()
        print("1. Ver mejores puntuaciones.")
        print("2. Buscar jugador.")
        print("3. Ver peores puntuaciones.")
        print("4. Mi mejor puntuacion.")
        print("5. Salir.")
        opcion = PedirOpcion(1,5)
        print()

        if(opcion == 1):
            FirstsLastsRanking(RankList,True)
        elif (opcion == 2):
            RankingJugador(RankList)
        elif (opcion == 3):
            FirstsLastsRanking(RankList,False)
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
        MenuPrincipal(user)
        opcion = PedirOpcion(1,4)
        if(opcion == 1):
            tematica = ElegirTematica()
            puntos = ComenzarJuego(tematica)
            if puntos > 0:
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