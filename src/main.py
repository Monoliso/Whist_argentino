# import collections, functools, operator
from whist import Jugador, Palo, Valor, Carta, determinar_ganador_juego, determinar_ganador_baza, actualizar_orden_jugadores
from io_interfaz import IO_interfaz
from terminal import Terminal as IO
import random

def main():
    interfaz = IO()
    jugadores = interfaz.obtener_jugadores()
    try: interfaz.mostrar_ganador_es(*whist(interfaz, jugadores), jugadores)
    except Exception: print("🤷")
    
def whist(interfaz: IO_interfaz, orden_jugadores: list[Jugador]) -> tuple[int, list[Jugador]]:
    """ Permite jugar una partida de Whist.
        
        @return: Tupla con el puntaje y el/los ganadores."""

    if not orden_jugadores: raise Exception("No se ingresaron jugadores")
    puntos_juego = dict.fromkeys(orden_jugadores, 0)
    # orden_jugadores[0].mostrar_inicio_juego(orden_jugadores)
    # Mostrar a los usuarios pertinentes el inicio de la partida.

    BAZAS_POR_MANO = [i+1 for i in range(8)] + [i for i in range(8, 0, -1)]
    for nro_mano in BAZAS_POR_MANO:
        try:
            triunfo = repartir_cartas(interfaz, orden_jugadores, nro_mano)
            predicciones = interfaz.obtener_predicciones(triunfo, orden_jugadores)
            bazas_ganadas = obtener_bazas_ganadas(interfaz, nro_mano, triunfo, predicciones, orden_jugadores)
            puntos_juego = obtener_nuevo_puntaje(interfaz, puntos_juego, bazas_ganadas, predicciones)
        except Exception: print("🤷")
        orden_jugadores = orden_jugadores[1:] + [orden_jugadores[0]]  # Rotar lista de jugadores

    return determinar_ganador_juego(puntos_juego)

def repartir_cartas(interfaz: IO_interfaz,
                    jugadores: list[Jugador],
                    numero_bazas: int) -> Carta:
    """ Dada una lista de jugadores y la cantidad de bazas que se juega,
        se le reparten la cantidad de cartas correspondiente a cada jugador y
        se devuelve el triunfo de la baza. """

    mazo: list[Carta] = [Carta(x, y) for y in Palo for x in Valor]
    cartas_jugador = dict.fromkeys(jugadores, list())
    random.shuffle(mazo)

    triunfo = mazo[numero_bazas*len(jugadores)]
    for indice, jugador in enumerate(jugadores):
        cartas_jugador = mazo[numero_bazas*indice:numero_bazas*(indice+1)]
        cartas_jugador.sort() # Esto es simplemente para comodidad del usuario
        try: interfaz.entregar_cartas(jugador, cartas_jugador, triunfo)
        except Exception: print("🤷")
    
    return triunfo

# Removí un argumento, el de las cartas de los jugadores
def obtener_bazas_ganadas(interfaz: IO_interfaz,
                          nro_mano: int,
                          triunfo: Carta,
                          predicciones: dict[Jugador, int],
                          orden_jugadores: list[Jugador]) -> dict[Jugador, int]:
    """ Permite jugar una mano del juego. Maneja la entrada y la salida al usuario.
    Devuelve los puntos que se realizaron en la mano. """

    bazas_ganadas = dict.fromkeys(orden_jugadores, int(0))
    mesa = list()

    for baza in range(nro_mano):
        for jugador in orden_jugadores:
            try: mesa += interfaz.obtener_jugada_valida()
            except Exception: print("🤷")
        ganador_baza = determinar_ganador_baza(mesa, orden_jugadores, triunfo)
        bazas_ganadas[ganador_baza] += 1
        orden_jugadores = actualizar_orden_jugadores(orden_jugadores, ganador_baza)
        interfaz.mostrar_ganador_baza(mesa, orden_jugadores)
    return bazas_ganadas

def obtener_nuevo_puntaje(interfaz: IO_interfaz,
                          puntos_juego: dict[Jugador, int],
                          bazas_ganadas: dict[Jugador, int],
                          predicciones: dict[Jugador, int]
                          ) -> dict[Jugador, int]:
    puntos_mano = dict()
    for jugador in puntos_juego:
        puntos_mano[jugador] = bazas_ganadas[jugador] + (10 if bazas_ganadas[jugador] == predicciones[jugador] else 0)
        puntos_juego[jugador] += puntos_mano[jugador]

    try: interfaz.mostrar_puntajes(jugador, puntos_mano, puntos_juego)
    except Exception: print("🤷")
    return puntos_juego

if __name__ == "__main__":
    main()
