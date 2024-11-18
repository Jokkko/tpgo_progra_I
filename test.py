import pytest

from Escaperoom import generar_terreno,generar_objeto,validar_movimiento, get_indice_objeto, mover_objeto, modificar_puntos,inicializar_pistas, inicializar_desafios


def test_generar_terreno():
    mapa = []
    generar_terreno(mapa, 5, 10, 5, 10)
    assert len(mapa) >= 5 and len(mapa) <= 10
    assert len(mapa[0]) >= 5 and len(mapa[0]) <= 10

def test_generar_objeto():
    mapa = []
    generar_terreno(mapa, 5, 5, 5, 5)  
    generar_objeto(mapa, 'O', 1)  
    count = sum(row.count('O') for row in mapa)
    assert count == 1

def test_validar_movimiento():
    mapa = [[' ']*5 for _ in range(5)]
    assert validar_movimiento(mapa, [2, 2], 'w') == True 
    assert validar_movimiento(mapa, [2, 2], 's') == True  
    assert validar_movimiento(mapa, [2, 2], 'a') == True
    assert validar_movimiento(mapa, [2, 2], 'd') == True
    assert validar_movimiento(mapa, [0, 0], 'w') == False
    assert validar_movimiento(mapa, [4, 4], 's') == False

def test_get_indice_objeto():
    mapa = [
        [' ', ' ', 'O'],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    indices = get_indice_objeto(mapa, 'O')
    assert indices == [0, 2]

def test_mover_objeto():
    mapa = [
        [' ', ' ', ' '],
        [' ', 'O', ' '],  
        [' ', ' ', ' ']
    ]
        
    mover_objeto(mapa, 0, 1, 'O')

    assert mapa[0][1] == 'O'
    assert mapa[1][1] == ' '

def test_modificar_puntos():
    assert modificar_puntos(1000, 'usar_pista') == 900
    assert modificar_puntos(1000, 'completar_desafio') == 1500
    assert modificar_puntos(1000, 'accion_correcta') == 1010
    assert modificar_puntos(1000, 'accion_incorrecta') == 990
    assert modificar_puntos(1050, 'usar_pista') == 950  

def test_inicializar_pistas():
    pistas, pistas_usadas = inicializar_pistas()
    assert isinstance(pistas, dict)
    assert isinstance(pistas_usadas, dict)
    assert len(pistas) > 0
    assert all(not usado for usado in pistas_usadas.values())

def test_inicializar_desafios():
    desafios, desafios_usados = inicializar_desafios()
    assert isinstance(desafios, dict)
    assert isinstance(desafios_usados, dict)
    assert len(desafios) > 0
    assert all(not usado for usado in desafios_usados.values())