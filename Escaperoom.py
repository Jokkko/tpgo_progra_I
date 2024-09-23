import random
import re

terreno = " "
userRepository = []
vaciarConsola = "\n" * 50

def GenerarTerreno(mapa,alturaMin,alturaMax,anchoMin,anchoMax):
    '''
    Genera el terreno de un mapa vacio pasado por parametro, el tipo de terreno sera definido por parametro
    el ancho y la altura sera un numero entre los minimos y maximos pasados por parametros.
    '''
    altoDelMapa = random.randint(alturaMin,alturaMax)
    anchoMinimoDelMapa = random.randint(anchoMin,anchoMax) 

    for _ in range(altoDelMapa):
        fila = []
        for _ in range(anchoMinimoDelMapa):
            fila.append(terreno)
        mapa.append(fila)

def GenerarObjeto(mapa,objeto,cantidad):
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
    for fila in mapa:
        print(fila)

def LeerAccion():
    accionesValidas = {'w', 'a', 's', 'd','menu'}
    accion = input("Elija una acción ('W', 'A', 'S', 'D' para el movimiento o 'menu' para salir al menu): ").lower()
    while accion not in accionesValidas:
        print("Acción no válida. Intentálo de nuevo.")
        accion = input("Elija una acción ('W', 'A', 'S', 'D' para el movimiento o 'menu' para salir al menu): ").lower()
    return accion

def ValidarMovimiento(mapa, posicion_actual, accion):
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
    indices = []
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if(mapa[y][x] == objeto):
                indices.append(y)
                indices.append(x)
    return indices

def MoverObjeto(mapa,x,y,objeto):
    #terreno = " "
    coordenadasObjeto = GetIndiceObjeto(mapa,objeto)
    mapa[coordenadasObjeto[0]][coordenadasObjeto[1]] = terreno
    mapa[coordenadasObjeto[0]+y*(-1)][coordenadasObjeto[1]+x] = objeto

def AccionPersonaje(mapa,accion): 
    personaje = "O"
    
    if  (accion == "w"):
        MoverObjeto(mapa,0,1,personaje)
    elif(accion == "s"):
        MoverObjeto(mapa,0,-1,personaje) 
    elif(accion == "a"):
        MoverObjeto(mapa,-1,0,personaje)
    elif(accion == "d"):
        MoverObjeto(mapa,1,0,personaje)


def MenuPrincipal():
    #muestre las opciones del menu
    #se puede usar center aca
    print("Bienvenido a ESCAPEROOM SIMULATOR")
    print("1. Comenzar Juego")
    print("2. Ranking de puntos")
    print("3. Como Jugar")
    print("4. Salir")
    

def PedirUserName(jugador_numero=1):
    patron = r"^[a-zA-Z]{3,9}$"
    username = input(f"Jugador {jugador_numero}, ingrese su nombre de usuario (3-9 caracteres, sin números o caracteres especiales): ")
    nombreValido = re.match(patron, username)

    while nombreValido is None or any(user['Username'] == username for user in userRepository):
        if nombreValido is None:
            print(f"Nombre no válido para el Jugador {jugador_numero}. Inténtelo de nuevo.")
        else:
            print(f"El nombre de usuario ya está en uso. Intente con otro.")
        username = input(f"Jugador {jugador_numero}, por favor, ingrese su nombre de usuario: ")
        nombreValido = re.match(patron, username)

    GenerarUser(username)
    return username

def PedirUserNames():
    username1 = PedirUserName(1)
    username2 = PedirUserName(2)
    return username1, username2

def GenerarUser(username):
    userRepository.append(dict(Username=username,Id = GenerarId() ))

def GenerarId():
    id = 0
    if(len(userRepository) != 0):
        ultimo = len(userRepository)-1 
        id = userRepository[ultimo]['Id'] + 1
    return id

def PedirOpcion(min,max):
    opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
    
    while opcion < min or opcion > max:
        print("Error")
        opcion = int(input(f"Elija una opcion entre {min} y {max}: "))
    
    print()
    return opcion

def MostrarDificultades():
    print("Niveles de dificultad: ")
    print("1. Facil")
    print("2. Normal")
    print("3. Dificil")
    

def NivelDeDificultad():
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
    dificultad = NivelDeDificultad()
    print("Temáticas disponibles:")
    for i, tematica in enumerate(dificultad, 1):
        print(f"{i}: {tematica}")

    seleccion = PedirOpcion(1, len(dificultad))
    MostrarIntroduccionALaTematica(dificultad[seleccion - 1])
    return dificultad[seleccion - 1]

def MostrarIntroduccionALaTematica(tematica):   
    introducciones = {
    "Breaking Bad": "Te encontrás en el laboratorio de metanfetaminas de Walter White.\n"
                    "Tu misión es encontrar la fórmula secreta antes de que la DEA llegue.\n"
                    "Cada segundo cuenta, y las decisiones que tomes definen tu destino.\n"
                    "¿Estás listo para arriesgarlo todo?",

    "Muerte Anunciada": "La historia comienza con un asesinato, y el reloj corre en tu contra.\n"
                        "Debes desentrañar la verdad detrás del crimen y descubrir al culpable antes de que se consuma la fatalidad.\n"
                        "Recordá, cada pista que encuentres te acercará a la verdad… o te alejará de ella.",

    "Psiquiátrico": "Te despertás en un oscuro y olvidado psiquiátrico.\n"
                    "Tu objetivo es escapar de las garras de una mente retorcida.\n"
                    "Explorá las habitaciones llenas de secretos, resuelve enigmas y desvela la historia perturbadora de este lugar.\n"
                    "Solo los más astutos lograrán salir con cordura.",

    "La Casa de Papel": "Sos parte de un equipo de criminales audaces que ha tomado una institución bancaria como rehén.\n"
                       "Tu misión es ejecutar el plan maestro del Profesor: robar millones y salir sin ser atrapados.\n"
                       "Cada decisión cuenta, y el tiempo corre. ¡Prepárate para la adrenalina!",

    "Sherlock Holmes": "En esta sala, un crimen intrigante tuvo lugar y solo vos podés resolverlo.\n"
                        "Con la astucia y la deducción como tus armas, examiná las pistas, interrogá a los sospechosos y desentrañá el misterio que desafía incluso a la mente más brillante.\n"
                      "La verdad está a tu alcance… si sos lo suficientemente perspicaz.",

    "Misión Gubernamental": "Te encontrás en el corazón de una operación encubierta.\n"
                            "Una amenaza inminente pone en riesgo la seguridad nacional.\n"
                            "Como agente especial, debes reunir pruebas, desactivar dispositivos y prevenir un desastre antes de que sea demasiado tarde.\n"
                            "La presión es alta, y cada segundo puede significar la diferencia entre el éxito y el fracaso."
}
    print(introducciones.get(tematica, "Introducción no disponible."))

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
            "No todos los sospechosos son lo que parecen; investiga sus alibis."
        ],
        "Misión Gubernamental": [
            "Un dispositivo escondido puede cambiar el curso de la misión; búscalo.",
            "Las comunicaciones pueden estar interceptadas. Encuentra el canal seguro."
        ]
    }

    pistas_usadas = {key: [] for key in pistas.keys()}
    
    return pistas, pistas_usadas

def MostrarPista(tematica, pistas, pistas_usadas):
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

def ModificarPuntos(puntos, accion):
    if accion == "usar_pista":
        return puntos - 100
    elif accion == "completar_desafio":
        return puntos + 50
    elif accion == "accion_correcta":
        return puntos + 10
    else:
        return puntos - 10
    return puntos

def MapaParaTematica(tematica):
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
    puntos = 1000
    Escapo = False
    pistas, pistas_usadas = InicializarPistas()
    mapa = MapaParaTematica(tematica)
    objetos = ["#","$"]
    for i in objetos:
        if(i=="#"):
            indicesPistas = GetIndiceObjeto(mapa,i) 
        else:
            indicesCandados = GetIndiceObjeto(mapa,i)
    
    while not Escapo:
        posicion_actual = GetIndiceObjeto(mapa,"O")
        print(pistas_usadas.get(tematica))
        if(ContieneElementos(posicion_actual, indicesPistas)): 
            MostrarPista(tematica, pistas, pistas_usadas)
        elif(ContieneElementos(posicion_actual, indicesCandados)):
            pass
        RenderizarMapa(mapa)
        accion = LeerAccion()
        if accion == 'menu':
            print("Saliendo al menu principal...")
            Escapo = True
            puntos = 0
            
        if ValidarMovimiento(mapa, posicion_actual, accion):        
            AccionPersonaje(mapa,accion)
            puntos = ModificarPuntos(puntos,accion)
            print(f"Puntos actuales: {puntos}")
        else:
            print("Movimiento inválido: fuera de los límites del mapa.")
    return puntos
    
    #esto deberiamos definirlo mejor cuando tengamos todo el develop actualizado 
    #if accion == "usar_pista": 
    #    puntos = modificar_puntos(puntos, "usar_pista")
    #elif accion == "completar_desafio": 
    #    puntos = modificar_puntos(puntos, "completar_desafio")
    #elif accion == "accion_correcta":
    #    puntos = modificar_puntos(puntos, "accion_correcta")

def Instrucciones():
    print("Comenzaras tu aventura en un mapa donde podras moverte libremente, tu personaje (Señalizado como una 'O') debera recoger pistas (Señalizadas como '#') para resolver los desafios (Señalizados como '$') y asi escapar!")
    print("Iniciarás con una totalidad de 1000 puntos a tu favor. Si necesitas ayuda, podés usar pistas, pero estas te costarán puntos.")
    print("Cada acción que realices también te costará puntos, por lo que deberas ser cuidadoso con tus movimientos.")
    print("Si te quedas sin puntos, perderas el juego. Si lográs descifrar el desafío, ganarás puntos. Una vez cumplidos todos los desafíos, en caso de que lo hagas, habrás ganado el juego.")
    print("Buena suerte, la vas a necesitar.")

def main():

    ##PARA TESTEAR MOVIMIENTO
    #mapa = GenerarMapa(6,11,8,16)
    #while(True): 
    #    print(vaciarConsola)
    #    RenderizarMapa(mapa)
    #    AccionPersonaje(mapa,LeerAccion())
    PedirUserName()
    jugando = True
    tematica = 0
    while(jugando):
        MenuPrincipal()
        opcion = PedirOpcion(1,4)
        if(opcion == 1):
            tematica = ElegirTematica()
            puntos = ComenzarJuego(tematica)
            if puntos > 0:
                print("Felicidades, escapaste")
            else:
                print("Abandonaste pero no pasa nada, suerte la proxima!")
        elif (opcion == 2):
           pass
        elif (opcion == 3):
            Instrucciones()
        elif (opcion == 4):
            print("Gracias por Jugar! Saliendo...")
            jugando = False
    
main()