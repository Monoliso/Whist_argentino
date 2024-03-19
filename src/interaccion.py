from abc import ABC, abstractmethod
from main import Jugador, Carta

class IO(ABC):
    
    @abstractmethod
    def obtener_jugadores() -> list[Jugador]:
        ...
    
    @abstractmethod
    def obtener_prediccion() -> int:
        ...

    @abstractmethod
    def obtener_jugada(self, cartas: list[Carta]) -> Carta:
        ...

    @abstractmethod
    def mostrar_ganador_es() -> None:
        ...