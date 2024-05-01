# import collections, functools, operator
from whist import Jugador, Palo, Valor, Carta, determinar_ganador_juego, obtener_nuevo_puntaje
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

        # obtener_nuevo_puntaje(puntos_juego, bazas_ganadas, predicciones)
        # try: interfaz.mostrar_puntajes(puntos_mano, puntos_juego)
        # except Exception: print("🤷")
        
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
                          mano: Mano,
                          orden_jugadores: list[Jugador]) -> dict[Jugador, int]:
        """ Permite jugar una mano del juego. Maneja la entrada y la salida al usuario.
        Devuelve los puntos que se realizaron en la mano. """

        bazas_ganadas = dict.fromkeys(orden_jugadores, int(0))

        for baza in range(mano.cant_bazas):
            mesa = dict()
            carta_baza = tuple()
            for numero, jugador in enumerate(orden_jugadores):
                cartas_jugador: list = cartas_jugadores[jugador]
                impresion.imprimir_seleccion_carta(triunfo, mesa, jugador, cartas_jugador, predicciones)

                jugada = obtener_jugada_valida(jugador, cartas_jugador, carta_baza, triunfo)
                if numero == 0:
                    carta_baza = jugada
                cartas_jugador.remove(jugada)
                cartas_jugadores[jugador] = cartas_jugador
                mesa[jugada] = jugador
                if numero != len(orden_jugadores)-1:
                    impresion.imprimir_transicion(orden_jugadores[numero+1])
                    
            ganador_baza = logica.determinar_ganador_baza(mesa, carta_baza, triunfo)
            bazas_ganadas[ganador_baza] += 1
            orden_jugadores = logica.actualizar_orden_jugadores(orden_jugadores, ganador_baza)

            impresion.imprimir_ganador_baza(triunfo, mesa, ganador_baza)
            if baza < numero_bazas-1:
                impresion.imprimir_transicion(orden_jugadores[0])
        puntos_mano = logica.determinar_puntos_mano(bazas_ganadas, predicciones)
        return puntos_mano

if __name__ == "__main__":
    main()

"""
    Qué abstracción queremos hacer?
    Quiero separar todo lo que pueda la lógica de su forma de interactuar.
    Quisiera encapsular de la forma más perfecta posible conjuntos y funciones que permitan jugar al whist.
    De esta forma puedo conseguir la construcción más correcta del juego.

    Luego tenemos una interfaz común para todos. Supongamos cada uno una dirección en una computadora.
    El programa es en realidad un cliente y un servidor, para poder manejar la lógica propia del juego y la de un boludo manejando la maquinita.

    2 formas: servidor sin clientes.
    Puede haber un servidor sin clientes? Sí, estaría esperando. Ahora bien, quien usa el programa siempre es el cliente.
    Nadie "usa" el servidor.
    El servidor debería recibir al menos un cliente como argumento.
    
    Aunque pensandolo por otro lado. Si quiero hacerlo perfecto, en vez de hacerlo programa lo hago
    código concurrente de otro módulo.
    Luego que main se encargue de brindar el acceso a los usuarios y boludeces. Como lo estuve haciendo.
 """