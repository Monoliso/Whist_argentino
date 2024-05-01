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
    
    def __repr__(self):
        # return f"Carta(valor={self.valor.name}, palo={self.palo.name})"
        return f"Carta({self.valor.name}, \"{self.palo.value}\")"

@dataclass
class Jugador:
    nombre: str

    def __hash__(self):
        return hash(str(self.nombre))

def determinar_ganador_baza(mesa: list[Carta], jugadores: list[Jugador], triunfo: Carta) -> Jugador:
    """ Devuelve el jugador que ganó la baza. """
    
    baza_palo = mesa[0].palo
    def comparar_cartas(carta: Carta):
        if carta.palo == triunfo.palo: return (2, carta.valor)
        if carta.palo == baza_palo: return (1, carta.valor)
        return (0, carta.valor)

    # max_index, _ = max(enumerate(mesa), key=lambda x: comparar_cartas(x[1]))
    # return jugadores[max_index]
    ganador, _ = max(zip(jugadores, mesa), key=lambda x: comparar_cartas(x[1]))
    return ganador

def determinar_ganador_juego(puntaje_juego: dict[Jugador, int]) -> tuple[int, list[Jugador]]:
    """ Devuelve el o los jugadores con mayor puntaje. """

    mayor_puntaje = max(puntaje_juego.values())
    ganador_es: list[Jugador] = [jugador for jugador, puntaje in puntaje_juego.items() if puntaje == mayor_puntaje]
    return mayor_puntaje, ganador_es

def actualizar_orden_jugadores(jugadores: list[Jugador], ganador_baza: Jugador) -> list[Jugador]:
    """ Devuelve una lista con el orden actualizado de los jugadores en una mano. """

    numero_ganador = jugadores.index(ganador_baza)
    nueva_lista = jugadores[numero_ganador:] + jugadores[:numero_ganador]
    return nueva_lista