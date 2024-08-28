import random

def GenerarMapa(alturaMin,alturaMax,anchoMin,anchoMax):
    '''
    Genera un mapa de juego con una altura y un ancho, minimo y maximo
    Ademas de rellenar el mapa con un terreno, un personaje, almenos un candado y almenos una pista.
    '''
    mapa = []
    terreno = "/"
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
    terreno = "/"
    coordenadasObjeto = GetIndiceObjeto(mapa,objeto)
    mapa[coordenadasObjeto[0]][coordenadasObjeto[1]] = terreno
    mapa[coordenadasObjeto[0]+y*(-1)][coordenadasObjeto[1]+x] = objeto

def MenuPrincipal():
    #muestre las opciones del menu
    return

def PedirOpcion(min,max):
    #pida una opcion(numero) al usuario y la devuelva
    return

def MostrarDificultades():
    #muestre las dificultades disponibles
    return

def SeleccionarDificultad():
    #Permite al usuario seleccionar una dificultad de las disponibles
    MostrarDificultades()
    PedirOpcion()
    return

def MostrarIntroduccionAlNivel():
    #Muestra el texto introductorio al nivel
    return

def MostrarPistas():
    #TO DEFINE: muestra las pistas del nivel?
    return

def EntrarEnDesafio():
    #Entra en un desafio dentro del 
    return

def MostrarTematicas():
    #Muestra las tematicas disponibles
    return

def ElegirTematica(dificultad):
    #Permite al usuario seleccionar una tematica de las disponibles a partir de la dificultad
    MostrarTematicas(dificultad)
    PedirOpcion()
    return

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
    #mapa = GenerarMapa(6,11,8,16)
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