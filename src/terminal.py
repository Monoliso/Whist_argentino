from io_interfaz import IO_interfaz, IO_jugador
from whist import Jugador, Carta
import random

def clear() -> None:
    """ Limpia la terminal """

    print("\033[H\033[J", end="")

class TerminalJugador(IO_jugador):
    def obtener_prediccion(self,
                           triunfo: Carta,
                           cartas_jugadores: dict[Jugador, list[Carta]],
                           cant_bazas: int,
                           jugador: Jugador) -> int:
        clear()
        input(f"Turno de {jugador.nombre}. Presione Enter cuando tenga el dispositivo en mano.")
        clear()
        condicion: bool = False
        while not condicion:
            imprimir_canto_predicciones()
            try: prediccion = int(input(f"{jugador.nombre}, cuantas bazas cree que ganará?: "))
            except ValueError: print("Debe ingresar un número")
            else:
                # Hay que corroborar que se ingrese un número Y que se encuentre en el rango.
                if prediccion >= 0 and prediccion <= cant_bazas: condicion = True
                else: print("El número excede la cantidad de bazas posible")
        return prediccion

    def obtener_jugada(self, cartas: list[Carta]) -> Carta:
        ...

class Terminal(IO_interfaz):

    def obtener_jugadores(self) -> list[Jugador]:
        clear()
        entrada_usuario = input("Ingrese los nombres de los jugadores separados por coma: ")
        jugadores_lista = entrada_usuario.split(',')
        nombre_jugadores = [jugador.replace(' ', '') for jugador in jugadores_lista]
        
        if len(nombre_jugadores) < 3 or len(nombre_jugadores) > 6:
            input("La cantidad de jugadores no es correcta, debe ser de 3 a 6 jugadores."
                " Vuelva a intentarlo.")
            return self.obtener_jugadores()
        
        random.shuffle(nombre_jugadores)
        resultado = [Jugador(jugador) for jugador in nombre_jugadores]
        self.recursos = dict.fromkeys(resultado, TerminalJugador())
        return resultado

    def obtener_predicciones(self,
                             cant_bazas: int,
                             triunfo: Carta,
                             cartas_jugadores: dict[Jugador, list[Carta]],
                             jugadores: list[Jugador]) -> dict[Jugador, int]:
        predicciones_mano = dict.fromkeys(jugadores, int(0))
        for jugador in jugadores:
            predicciones_mano[jugador] = \
                self.recursos[jugador].obtener_prediccion(triunfo, cartas_jugadores, cant_bazas, jugador)
        return predicciones_mano

    def mostrar_ganador_es(self, puntaje: int, ganadores: list[Jugador], jugadores: list[Jugador]) -> None:
        ...

    def mostrar_inicio_juego(self, jugadores: list[Jugador]) -> None:
        nombre_jugadores = [jugador.nombre for jugador in jugadores]
        input("\nBienvenidos al Whist, esperamos que disfruten del juego.")
        input(f"El orden de los jugadores es: {nombre_jugadores}.")
        input("Empieza el juego.")

    def mostrar_inicio_mano(self, numero_mano: int, jugadores: list[Jugador]) -> None:
        clear()
        input(f"Comienza la mano de {numero_mano}. Ahora es el turno de {jugadores[0].nombre}.")
        clear()
        input(f"Turno de {jugadores[0].nombre}. Presione Enter cuando tenga el dispositivo en mano.")



def imprimir_canto_predicciones(triunfo: Carta,
                                jugador: Jugador,
                                cartas_jugador: list[Carta],
                                predicciones_previas: dict[Jugador, int]) -> None:

    print(f"Carta triunfo de la mano actual:")
    imprimir_mazo([triunfo], False)
    print(f"Cartas de {jugador.nombre}:")
    imprimir_mazo(cartas_jugador, True)
    if predicciones_previas:
        print(f"Prediccion de cada jugador (nombre, predicción): {predicciones_previas}")

def imprimir_mazo(lista_de_cartas: list[Carta], enumerado: bool) -> None:
    """ Esta función imprime en pantalla horizontalmente una lista de cartas.
        Acepta como parámetro si se encuentra enumerada.  """
    # [xG: desplazar el cursor x columnas
    # [xA: ascender el cursor x filas
    # [xB: descender el cursor x filas

    nro_columnas = 1
    nro_carta = 1
    for carta in lista_de_cartas:
        if carta[0] != "10":
            print(
                f"\033[{nro_columnas}G┌─────┐\n"
                f"\033[{nro_columnas}G│{carta[0]}    │\n"
                f"\033[{nro_columnas}G│  {carta[1]}  │\n"
                f"\033[{nro_columnas}G│    {carta[0]}│\n"
                f"\033[{nro_columnas}G└─────┘")
        else:
            print(
                f"\033[{nro_columnas}G┌─────┐\n"
                f"\033[{nro_columnas}G│10   │\n"
                f"\033[{nro_columnas}G│  {carta[1]}  │\n"
                f"\033[{nro_columnas}G│   10│\n"
                f"\033[{nro_columnas}G└─────┘")
        if enumerado:
            print(f"\033[{nro_columnas}G   {nro_carta}\t")
            print("\033[7A")
        else:
            print("\033[6A")
        nro_columnas += 8
        nro_carta += 1
    if enumerado:
        print("\033[6B")
    else:
        print("\033[5B")
        

def obtener_jugada_valida(jugador: str, cartas_jugador: "list[tuple]",
                          palo_baza: tuple, triunfo: tuple) -> "tuple[str, str]":
    condicion = True
    while condicion:
        jugada = entrada.ingresar_jugada(jugador)
        if (jugada > (largo:=len(cartas_jugador)) or jugada <= 0):
            input(f"Debe seleccionar una carta dentro del rango 1-{largo}.")
        elif not palo_baza:
            condicion = False
        else:
            validacion_jugada = logica.corroborar_jugada(cartas_jugador, jugada,
                                                         palo_baza[1], triunfo[1])
            if validacion_jugada[0]:
                condicion = False
            else:
                impresion.imprimir_error_jugada(validacion_jugada[1], palo_baza[1],
                                                validacion_jugada[2])
    return cartas_jugador[jugada-1]