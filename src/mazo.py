from pila_cartas import *
from carta import *
import random

MISMO_COLOR_NEGRO = 0
MISMO_COLOR_ROJO = 1

def crear_mazo(mazos=1, palos=4):
    """Devuelve una PilaCartas con las cartas boca abajo y mezcladas.
    Cada mazo de los mazos tiene 52 cartas, y puede ser completado con 1, 2 o 4 palos.
    En caso de que estén los 4 palos el mazo se conformará con la serie del 1 al 13
    para cada uno de ellos, en caso de ser sólo 2 palos serán 2 veces la serie 1 al 13
    para dos palos del mismo color y en caso de ser 1 sólo palo será 4 veces la serie 1 al 13
    para ese palo."""
   
    mazo = PilaCartas()
    mismo_color = random.randint(0,1)
    palo_random = random.randint(0,3)
    palo = 0
    i = 0
    for v in range(52 * mazos):
	    if palos == 4:
		    carta = Carta((v % 13) + 1,palo)
		    mazo.apilar(carta)
		    if (v % 13)  == 0 and v != 0:
			    palo += 1
	    if palos == 2:
		    if MISMO_COLOR_ROJO:
			    palo = [CORAZONES, DIAMANTES]
			    carta = Carta((v % 13) + 1,palo[i % 2])
			    mazo.apilar(carta)
			    if (v % 13)  == 0 and v != 0:
				    i += 1
		    if MISMO_COLOR_NEGRO:
			    palo = [PICAS, TREBOLES]
			    i = 0
			    carta = Carta((v % 13) + 1,palo[i % 2])
			    mazo.apilar(carta)
			    if (v % 13)  == 0 and v != 0:
				    i += 1
	    if palos == 1:
		    carta = Carta ((v % 13) + 1, palo_random)
		    mazo.apilar(carta)
    mazo.mezclar()
    return mazo

