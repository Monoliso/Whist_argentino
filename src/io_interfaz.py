from abc import ABC, abstractmethod
from whist import Jugador, Carta

class IO_jugador(ABC):
    @abstractmethod
    def obtener_prediccion(self, cant_bazas: int, jugador: Jugador) -> int:
        ...

    @abstractmethod
    def obtener_jugada(self, cartas: list[Carta]) -> Carta:
        ...

class IO_interfaz(ABC):
    recursos: dict[Jugador, IO_jugador]

    @abstractmethod
    def obtener_jugadores(self) -> list[Jugador]:
        ...

    @abstractmethod
    def obtener_predicciones(self,
                             triunfo: Carta,
                             cartas_jugadores: dict[Jugador, list[Carta]],
                             jugadores: list[Jugador]) -> dict[Jugador, int]:
        """ Dado el triunfo de la baza, las cartas de los jugadores, y el orden para
        solicitar cada prediccion, esta función se encarga de mostrarle a cada uno
        la información pertinente para que pueda realizar la prediccion de la mano. """
        ...
    
    @abstractmethod
    def mostrar_ganador_es(self, puntaje: int, ganadores: list[Jugador], jugadores: list[Jugador]) -> None:
        ...
    
    @abstractmethod
    def mostrar_inicio_juego(self, jugadores: list[Jugador]) -> None:
        ...
    
    @abstractmethod
    def mostrar_inicio_mano(self, numero_mano: int, jugadores: list[Jugador]) -> None:
        ...