from main import Jugador, Carta
from interaccion import IO

class Terminal(IO):

    def obtener_jugadores(self) -> list[Jugador]:
        ...
    
    def obtener_prediccion(self) -> int:
        ...

    def obtener_jugada(self, cartas: list[Carta]) -> Carta:
        ...

    def mostrar_ganador_es(self) -> None:
        ...