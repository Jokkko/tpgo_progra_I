import random
import re

terreno = " "
userRepository = []

def GenerarTereno(mapa,alturaMin,alturaMax,anchoMin,anchoMax):
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
    GenerarTereno(mapa,alturaMin,alturaMax,anchoMin,anchoMax)
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
    accion = input("Elija una accion ('W','A','S','D' para el movimiento.): ")
    while(accion.lower() != 'w' and accion.lower() != 's' and accion.lower() != 'a' and
          accion.lower() != 'd'):
        print("No existe tal accion. Intente denuevo.")
        accion = input("Elija una accion ('W','A','S','D' para el movimiento.")
    return accion

def GetIndiceObjeto(mapa,objeto):
    indices = []
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if(mapa[y][x] == objeto):
                indices.append(y)
                indices.append(x)
    return indices

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

def MoverObjeto(mapa,x,y,objeto):
    #terreno = " "
    coordenadasObjeto = GetIndiceObjeto(mapa,objeto)
    mapa[coordenadasObjeto[0]][coordenadasObjeto[1]] = terreno
    mapa[coordenadasObjeto[0]+y*(-1)][coordenadasObjeto[1]+x] = objeto

def MenuPrincipal():
    #muestre las opciones del menu
    #se puede usar center aca
    pass

def PedirUserName(jugador_numero):
    # Función auxiliar para pedir un nombre de usuario válido
    patron = r"^[a-zA-Z]{3,9}$"
    
    username = input(f"Jugador {jugador_numero}, por favor, ingrese su nombre de usuario.\nNo puede contener más de 10 caracteres ni menos de 3, ni números o caracteres especiales: ")
    nombreValido = re.match(patron, username)
    
    while nombreValido is None or any(user['Username'] == username for user in userRepository):
        if nombreValido is None:
            print(f"Nombre no válido para el Jugador {jugador_numero}. Inténtelo de nuevo.")
        else:
            print(f"El nombre de usuario ya está en uso. Intente con otro.")
        username = input(f"Jugador {jugador_numero}, por favor, ingrese su nombre de usuario:\n")
        nombreValido = re.match(patron, username)
    
    GenerarUser(username)
    return username

def PedirUserNames():
    # Llama a la función auxiliar para ambos jugadores
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
    #pide una opcion(numero) al usuario y la devuelva
    opcion = int(input("Elija una opcion entre: ",min, "y", max))
    
    while opcion < min or opcion > max:
        print("Error")
        opcion = int(input("elija una opcion entre: ",min, "y", max))
    
    return opcion

def MostrarDificultades():
    #muestre las dificultades disponibles
    print("Niveles de dificultad: ")
    print("1. Facil")
    print("2. Normal")
    print("3. Dificil")
    

def nivelDeDificultad():
    #Permite al usuario seleccionar una dificultad de las disponibles
    MostrarDificultades()
    opcion = PedirOpcion(1,3)

    facil = ["Breaking bad","Muerte anunciada"]
    intermedio = ["Psiquiatrico","La casa de papel"]
    dificil = ["Sherlock Holmes","Mision gubernamental"]

    if opcion == 1:
        dificultad = facil
    elif opcion == 2:
        dificultad = intermedio
    elif opcion == 3:
        dificultad = dificil

    return dificultad

    

def ElegirTematica():
    dificultad = nivelDeDificultad() 
    print("Temáticas disponibles:")
    for i, tematica in enumerate(dificultad, start=1):
        print(f"{i}: {tematica}")

    seleccion = PedirOpcion(1, len(dificultad)) 
    MostrarIntroduccionALaTematica(dificultad[seleccion - 1]) 

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

def inicializar_pistas():
    # Diccionario de pistas
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
        # filtra por las pistas no utilizadas
        disponibles = [pista for pista in pistas[tematica] if pista not in pistas_usadas[tematica]]
        
        if disponibles:
            #elije una pista entre disponibles de forma aleatorias
            pista = random.choice(disponibles)
            print(f"Pista para {tematica}: {pista}")
            # marca la pista como usada y la suma a la lista de pistas usadas
            pistas_usadas[tematica].append(pista)
        else:
            print(f"No hay más pistas disponibles para la temática '{tematica}'.")
    else:
        print(f"Temática '{tematica}' no válida.")


def EntrarEnDesafio():
    #Entra en un desafio dentro del 
    pass

def ComenzarJuego(tematica):
    #Funcion que comienza el juego para la tematica dada
    Escapo = False
    mapa = []
    MostrarIntroduccionALaTematica(tematica)
    if(tematica == 1):
        mapa = GenerarMapa(4,5,4,6) 
        while(not Escapo):
            AccionPersonaje(mapa,LeerAccion())
            pass
    elif(tematica == 2):
        mapa = GenerarMapa(4,5,4,6) 
        while(not Escapo):
            AccionPersonaje(mapa,LeerAccion())
            pass
    #segun cada tematica


vaciarConsola = "\n" * 50

def main():

    ##PARA TESTEAR MOVIMIENTO
    mapa = GenerarMapa(6,11,8,16)
    PedirUserName()
    #while(True): 
    #    print(vaciarConsola)
    #    RenderizarMapa(mapa)
    #    AccionPersonaje(mapa,LeerAccion())
    jugando = True
    dificultad = 0
    tematica = 0
    while(jugando):
        MenuPrincipal()
        opcion = PedirOpcion()
        if(opcion == 1):
            dificultad = SeleccionarDificultad()
            tematica = ElegirTematica(dificultad)
            ComenzarJuego(tematica)
        elif (opcion == 0):
            print("Saliendo...")
            jugando = False
    
main()