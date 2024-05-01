from dataclasses import dataclass
from enum import IntEnum, StrEnum, auto

class Palo(StrEnum):
    PICA = '♠️'
    TREBOL = '♣️'
    CORAZON = '♥️'
    DIAMANTE = '♦️'
    
class Valor(IntEnum):
    DOS = 2
    TRES = auto()
    CUATRO = auto()
    CINCO = auto()
    SEIS = auto()
    SIETE = auto()
    OCHO = auto()
    NUEVE = auto()
    DIEZ = auto()
    J = auto()
    Q = auto()
    K = auto()
    A = auto()

    def __str__(self) -> str:
        match self:
            case Valor.J: return "J"
            case Valor.Q: return "Q"
            case Valor.K: return "K"
            case Valor.A: return "A"
            case _: return super().__str__()

@dataclass(order=True)
class Carta:
    valor: Valor
    palo: Palo

@dataclass
class Jugador:
    nombre: str

    def __hash__(self):
        return hash(str(self.nombre))

@dataclass
class Mano:
    """ Invariantes de una mano. """
    cant_bazas: int
    triunfo: Carta
    predicciones: dict[Jugador, int]


def obtener_nuevo_puntaje(puntos_juego: dict[Jugador, int],
                          bazas_ganadas: dict[Jugador, int],
                          predicciones: dict[Jugador, int]
                          ) -> dict[Jugador, int]:
    for jugador in puntos_juego:
        if(bazas_ganadas[jugador] == predicciones[jugador]):
            puntos_juego[jugador] += (10 + bazas_ganadas[jugador])
        else: 
            puntos_juego[jugador] += bazas_ganadas[jugador]
    return puntos_juego

def determinar_ganador_juego(puntaje_juego: dict[Jugador, int]) -> tuple[int, list[Jugador]]:
    """ Devuelve el o los jugadores con mayor puntaje. """

    mayor_puntaje = max(puntaje_juego.values())
    ganador_es: list[Jugador] = [jugador for jugador, puntaje in puntaje_juego.items() if puntaje == mayor_puntaje]
    return mayor_puntaje, ganador_es