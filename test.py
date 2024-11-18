import pytest

from Escaperoom import GenerarTerreno,GenerarObjeto,GenerarMapa, ValidarMovimiento, GetIndiceObjeto, MoverObjeto, ModificarPuntos,InicializarPistas, InicializarDesafios


def test_generar_terreno():
    mapa = []
    GenerarTerreno(mapa, 5, 10, 5, 10)
    assert len(mapa) >= 5 and len(mapa) <= 10
    assert len(mapa[0]) >= 5 and len(mapa[0]) <= 10

def test_generar_objeto():
    mapa = []
    GenerarTerreno(mapa, 5, 5, 5, 5)  
    GenerarObjeto(mapa, 'O', 1)  
    assert any('O' in row for row in mapa)

def test_validar_movimiento():
    mapa = [[' ']*5 for _ in range(5)]
    assert ValidarMovimiento(mapa, [0, 0], 's') == True  
    assert ValidarMovimiento(mapa, [4, 4], 'd') == False  

def test_get_indice_objeto():
    mapa = [[' ', ' ', 'O'], [' ', ' ', ' '], [' ', ' ', ' ']]
    indices = GetIndiceObjeto(mapa, 'O')
    assert indices == [0, 2]

def test_mover_objeto():
    mapa = [[' ', ' ', 'O'], [' ', ' ', ' '], [' ', ' ', ' ']]
    MoverObjeto(mapa, 0, 1, 'O')
    assert mapa[0][2] == 'O'
    assert mapa[0][0] == ' '

def test_modificar_puntos():
    assert ModificarPuntos(1000, 'usar_pista') == 900
    assert ModificarPuntos(1000, 'completar_desafio') == 1500
    assert ModificarPuntos(1000, 'accion_correcta') == 1010
    assert ModificarPuntos(1000, 'accion_incorrecta') == 990

def test_inicializar_pistas():
    pistas, pistas_usadas = InicializarPistas()
    assert isinstance(pistas, dict)
    assert isinstance(pistas_usadas, dict)

def test_inicializar_desafios():
    desafios, desafios_usados = InicializarDesafios()
    assert isinstance(desafios, dict)
    assert isinstance(desafios_usados, dict)