import random

def GenerarMapa(alturaMin,alturaMax,anchoMin,anchoMax):
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
    accion = input("Elija una accion ('W','A','S','D' para el movimiento. 'I' para interactuar): ")
    while(accion.lower() != 'w' and accion.lower() != 's' and accion.lower() != 'a' and
          accion.lower() != 'd' and accion.lower() != 'i'):
        print("No existe tal accion. Intente denuevo.")
        accion = input("Elija una accion ('W','A','S','D' para el movimiento. 'I' para interactuar): ")
    return accion


#def AccionPersonaje(accion):
#    if(accion == "w"):
        



mapa = GenerarMapa(6,11,8,16)

RenderizarMapa(mapa)
#AccionPersonaje(LeerAccion())