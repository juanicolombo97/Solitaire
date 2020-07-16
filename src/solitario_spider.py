from mesa import *
from mazo import*

PILAS_6=[1,4,7,10]

class SolitarioSpider:
    """
    Solitario Spider

    Este solitario tiene:
                            2 Mazos (un palo)
                            8 Fundaciones
                            10 Pilas

    En las fundaciones pueden apilarse cartas de la K a la A consecutivas y solo se pueden mover secuencias completas.

    En las pilas se pueden solo apilar cartas consecutivas descendentes.

    Al inicio se reparten 5 cartas en cada pila con excepción de las pilas 1, 4, 7 y 10 donde se reparten 6.

    Todas las cartas se reparten boca abajo con excepción de la última carta de cada pila que se pone boca arriba.

    El objetivo del juego es completar todos los pilones de las fundaciones.

    Las cartas se pueden mover entre las pilas del tablero para armar juegos.

    En caso de que al realizar un movimiento la carta del tope de una pila del tablero quede boca abajo la misma debe darse vuelta automáticamente.

    Para mover a la fundación se debe haber armado una secuencia de la K a la A que se mueve completa.

    Cuando se le piden cartas al mazo se reparte una carta boca arriba sobre cada una de las pilas del tablero.

    Implementación: Si se indica como origen una pila y no hay indicado un destino, el juego intentará apilar el pilón superior de la pila en una de las fundaciones."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        #Se crean los mazos
        self.mesa.mazo = crear_mazo(mazos=2,palos=1)
       
        #Se crean las 8 fundaciones, de un solo palo
        for x in range(8):
            self.mesa.fundaciones.append(
                PilaCartas(
                    valor_inicial = 13,
                    criterio_apilar = criterio(orden = DESCENDENTE),
                    criterio_mover = criterio(orden = ASCENDENTE),
                    ))

        #Creamos las 10 pilas

        for j in range(10):
            self.mesa.pilas_tablero.append(
                PilaCartas(
                pila_visible=True,
                criterio_apilar = criterio(orden = DESCENDENTE),
                criterio_mover = criterio(orden = ASCENDENTE),
                ))
            for i in range(5 + (1 if (j + 1) in PILAS_6 else 0)):
                self.mesa.pilas_tablero[j].apilar(self.mesa.mazo.desapilar(), forzar = True)
            self.mesa.pilas_tablero[j].tope().voltear()


    def termino(self):
        """Avisa cuando se termina el juego"""
        for fundacion in self.mesa.fundaciones:
            if len(fundacion) < 13:
                return False
        return True

    def jugar(self, jugada):
        """Efectúa una movida.
        La jugada es una lista de pares (PILA, numero).
        Si no puede realizarse la jugada se levanta una excepción SolitarioError descriptiva."""
        j0, p0 = jugada[0]
        j1, p1 = jugada[1] if len(jugada) == 2 else (SALIR, 0)

        if len(jugada) == 1 and j0 == MAZO:
            # Pide cartas al mazo
            self.repartir_mazo()

        elif len(jugada) == 1 and j0 == PILA_TABLERO:
            # Trata de ubicar una subpila de la pila en una fundación
            for fundacion in self.mesa.fundaciones:
                try:
                    self.mover_pila(self.mesa.pilas_tablero[p0], fundacion)
                    return
                except SolitarioError:
                    pass
            raise SolitarioError("No hay ninguna fundación a la que se pueda mover la pila.")

        elif len(jugada) == 2 and j0 == PILA_TABLERO and j1 in (FUNDACION,PILA_TABLERO):
            # Mueve una subpila de una pila del tablero a otra pila o fundación, si es posible
            destino = self.mesa.fundaciones[p1] if j1 == FUNDACION else self.mesa.pilas_tablero[p1]
            self.mover_pila(self.mesa.pilas_tablero[p0], destino)

        elif len(jugada) == 2 and j0 == FUNDACION and len(self.mesa.fundaciones[p0]) == 13 and j1 in (FUNDACION,PILA_TABLERO):
            # Mueve toda la fundación como una secuencia completa al destino
            destino = self.mesa.fundaciones[p1] if j1 == FUNDACION else self.mesa.pilas_tablero[p1]
            self.mover_pila(self.mesa.fundaciones[p0], destino)

        else:
            raise SolitarioError("Movimiento Inválido.")

            
    def mover_pila(self,origen,destino):
        '''Mueve (si es posible) una subpila del origen al destino'''
        if origen.es_vacia():
            raise SolitarioError('La pila esta vacia')

        destino.mover(origen)

        if destino in self.mesa.fundaciones:
            # En caso de que trate de apilar en una fundación una subpila no completa
            if len(destino) < 13:
                origen.mover(destino)
                raise SolitarioError("Solo se pueden apilar secuencias completas en las fundaciones.")

        if origen.tope().boca_abajo:
            origen.tope().voltear()


    def repartir_mazo(self):
        '''Reparte una carta dada vuelta a cada pila desde el mazo'''
        for j in range(10):
            self.mesa.pilas_tablero[j].apilar(self.mesa.mazo.desapilar(), forzar = True)
            self.mesa.pilas_tablero[j].tope().voltear()

