from mesa import *
from mazo import*
FUNDACIONES = 6
PILAS = 4
class SolitarioEliminador:
    """
        Solitario Eliminador

        Este solitario tiene:
                                1 Mazo
                                6 Fundaciones
                                4 Pilas

        Al inicio se reparten todas las cartas del mazo en igual cantidad sobre las pilas.

        Todas las cartas se reparten boca arriba.

        En las fundaciones hay que apilar cartas con la restricción que sea consecutiva con el valor de la carta tope.

        En las pilas no se pueden ni apilar ni mover a otras pilas, solo se pueden mover a las fundaciones.

        El juego termina cuando se eliminan todas las cartas de las pilas.
    """

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        self.mesa.mazo = crear_mazo() #Se crea el mazo
        
        # Se crean las fundaciones

        for i in range(FUNDACIONES):
            self.mesa.fundaciones.append(
                PilaCartas(
                    criterio_apilar = criterio(orden= CONSECUTIVA),
                    ))

        # Creamos las pilas

        for x in range(PILAS ):
            self.mesa.pilas_tablero.append(
                    PilaCartas(pila_visible=True),
                    )
        
        j = 0    
        while not self.mesa.mazo.es_vacia():
            # Se barajan las cartas en las pilas dadas vueltas
            carta = self.mesa.mazo.desapilar()
            carta.voltear()
            self.mesa.pilas_tablero[j % 4].apilar(carta)
            j += 1

    
    def termino(self):
        """Avisa si el juego se terminó."""
        for pila in self.mesa.pilas_tablero:
            if not pila.es_vacia():
                return False
        return True

    def jugar(self, jugada):
        """Efectúa una movida.
        La jugada es una lista de pares (PILA, numero).
        Si no puede realizarse la jugada se levanta una excepción SolitarioError descriptiva."""
        j0,p0 = jugada[0]
        j1,p1 = jugada[1] if len(jugada) == 2 else (SALIR, 0)

        if len(jugada) == 1 and j0 == PILA_TABLERO:
            # En el caso que solo se elegir una pila del tablero, trata de ubicar la carta del tope en una fundición si es posible
            for fundacion in self.mesa.fundaciones:
                try:
                    self.mover_carta(self.mesa.pilas_tablero[p0],fundacion)
                    return
                except SolitarioError:
                    pass
            raise SolitarioError('No puede moverse la carta a la fundacion indicada')
        if len(jugada) == 2 and j0 == PILA_TABLERO and j1 == FUNDACION:
            # Especificaron origen y destino, intentamos mover del tablero adonde corresponda.
            self.mover_carta(self.mesa.pilas_tablero[p0],self.mesa.fundaciones[p1])

        else:
            # No hay más jugadas válidas según nuestras reglas.
            raise SolitarioError("Movimiento inválido")

            
    def mover_carta(self,origen,destino):
        '''Mueve las cartas desde una pila a una fundación'''
        if origen.es_vacia():
                raise SolitarioError('La pila esta vacia')

        destino.apilar(origen.tope())
        origen.desapilar()



