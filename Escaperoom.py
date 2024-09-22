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

def MostrarPistas():
    #TO DEFINE: muestra las pistas del nivel?
    pass

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