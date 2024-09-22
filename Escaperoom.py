import random
import re

terreno = " "

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
    GenerarTereno(mapa,alturaMin,alturaMax,anchoMin,anchoMax,terreno)
    GenerarObjeto(mapa,personaje,1,terreno)
    GenerarObjeto(mapa,candados,2,terreno)
    GenerarObjeto(mapa,pistas,2,terreno)
    return mapa

def GenerarTereno(mapa,alturaMin,alturaMax,anchoMin,anchoMax,terreno):
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

def GenerarObjeto(mapa,objeto,cantidad,terreno):
    columnaSpawn = random.randint(0,len(mapa)-1) 
    filaSpawn = random.randint(0,len(mapa[columnaSpawn])-1)
    for _ in range(cantidad):
        while(mapa[columnaSpawn][filaSpawn] != terreno): 
            columnaSpawn = random.randint(0,len(mapa)-1) 
            filaSpawn = random.randint(0,len(mapa[columnaSpawn])-1)
        mapa[columnaSpawn][filaSpawn] = objeto

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

def PedirUserName():
    #Pide al usuario un nombre, (usar regex aca)
    username = input("Porfavor Ingrese su nombre de usuario, \nNo puede contener mas de 10 caracteres ni menos de 3, numeros, ni caracteres especiales:")
    patron = r"^[a-zA-Z]{3,9}$"
    nombreValido = re.match(patron,username)
    while(nombreValido == None):
        print("Nombre no valido. Intentelo denuevo")    
        username = input("Porfavor Ingrese su nombre de usuario, \nno puede contener mas de 10 caracteres ni menos de 3, numeros, ni caracteres especiales:")
        nombreValido = re.match(patron,username)
    return username

def PedirOpcion(min,max):
    #pida una opcion(numero) al usuario y la devuelva
    pass

def MostrarDificultades():
    #muestre las dificultades disponibles
    pass

def SeleccionarDificultad():
    #Permite al usuario seleccionar una dificultad de las disponibles
    MostrarDificultades()
    PedirOpcion()
    pass

def MostrarIntroduccionAlNivel():
    #Muestra el texto introductorio al nivel
    pass

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

def MostrarTematicas():
    #Muestra las tematicas disponibles
    pass

def ElegirTematica(dificultad):
    #Permite al usuario seleccionar una tematica de las disponibles a partir de la dificultad
    MostrarTematicas(dificultad)
    PedirOpcion()
    pass

def ComenzarJuego(tematica):
    #Funcion que comienza el juego para la tematica dada
    Escapo = False
    mapa = []
    MostrarIntroduccionAlNivel(tematica)
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
    while(True): 
        print(vaciarConsola)
        RenderizarMapa(mapa)
        AccionPersonaje(mapa,LeerAccion())
    #jugando = True
    #dificultad = 0
    #tematica = 0
    #while(jugando):
    #    MenuPrincipal()
    #    opcion = PedirOpcion()
    #    if(opcion == 1):
    #        dificultad = SeleccionarDificultad()
    #        tematica = ElegirTematica(dificultad)
    #        ComenzarJuego(tematica)
    #    elif (opcion == 0):
    #        print("Saliendo...")
    #        jugando = False
    


main()