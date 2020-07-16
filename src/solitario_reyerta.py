from mesa import *
from mazo import *

CANTIDAD_RECORRIDOS_MAXIMOS = 3

class SolitarioReyerta:
	'''
	Solitario Reyerta

	Este solitario tiene:
							1 Mazo
							4 Fundaciones
							4 Pilas

	En las fundaciones pueden apilarse cartas por orden de valor ascendente de la A a la K, sin importar los palos.

	En las pilas no pueden apilarse ni moverse cartas. De estas pilas sólo se ve la carta del tope.

	Al inicio se extraen los ases del mazo y se apilan en las fundaciones.

	El objetivo del juego es completar todos los pilones de las fundaciones.

	Cada vez que se le pidan cartas al mazo se repartirá una carta boca arriba sobre cada una de las pilas.

	En el caso de que no hubiera ninguna carta en el mazo, deben retirarse todas las cartas de las pilas del tablero,

	mezclarlas de nuevo y volver a ponerlas en el mazo sólo dos veces (es decir, el mazo puede recorrerse tres veces).

	Implementación: Si se indica como origen una pila y no hay indicado un destino, el juego intentará apilar esa carta en una de las fundaciones.'''

	def __init__(self, mesa):
		"""Inicializa con una mesa creada."""
		self.mesa = mesa
		self.recorridos_mazo = 1

	def armar(self):
		"""Arma el tablero a la configuración inicial."""
		self.mesa.mazo = crear_mazo() # Creamos un mazo.

		for i in range(4):
			# Creamos 4 fundaciones vacias
			self.mesa.fundaciones.append(
						PilaCartas(
							criterio_apilar=criterio(orden=ASCENDENTE),
						))
			# Creamos 4 pilas del tablero vacias
			self.mesa.pilas_tablero.append(
								PilaCartas()
								)
		# Ponemos los 4 aces en las fundaciones
		aux = Pila()
		i = 0
		while not self.mesa.mazo.es_vacia():
			carta = self.mesa.mazo.desapilar()
			if carta.valor == 1:
				carta.voltear()
				self.mesa.fundaciones[i].apilar(carta)
				i += 1
			else:
				aux.apilar(carta)
		while not aux.esta_vacia():
			self.mesa.mazo.apilar(aux.desapilar())

		# Ponemos una carta en cada pila del tablero
		self._colocar_carta_pilas_tablero()

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

		if len(jugada) == 1 and j0 == PILA_TABLERO:
		# Sólo especificaron una pila de origen, intentamos mover a alguna fundación.
			for fundacion in self.mesa.fundaciones:
				try:
					self._carta_a_pila(self.mesa.pilas_tablero[p0], fundacion)
					return
				except SolitarioError:
					pass
			raise SolitarioError("No puede moverse esa carta a la fundación")

		elif len(jugada) == 1 and j0 == MAZO:
		# Pidio cartas al mazo. Se reparte una carta a cada pila del tablero.
			if self.mesa.mazo.es_vacia():
			#En el caso que no tenga cartas para repartir devuelven todas las cartas de las pilas al mazo, se mezcla y se vuelven a repartir
				if self.recorridos_mazo == CANTIDAD_RECORRIDOS_MAXIMOS:
					raise SolitarioError(f"Ya se recorrió el mazo el máximo de veces {CANTIDAD_RECORRIDOS_MAXIMOS}")
				for pila_tablero in self.mesa.pilas_tablero:
					while not pila_tablero.es_vacia():
						carta = pila_tablero.desapilar()
						carta.voltear()
						self.mesa.mazo.apilar(carta)
				print("Barajando mazo, recorridos restantes {}".format(CANTIDAD_RECORRIDOS_MAXIMOS - self.recorridos_mazo))
				self.mesa.mazo.mezclar()
				self.recorridos_mazo += 1
				self._colocar_carta_pilas_tablero()
			else:
				self._colocar_carta_pilas_tablero()


		elif len(jugada) == 2 and j0 == PILA_TABLERO and j1 == FUNDACION:
		# Especificaron tabla y fundacion donde colocar
			self._carta_a_pila(self.mesa.pilas_tablero[p0], self.mesa.fundaciones[p1])
		else:
		# No hay más jugadas válidas según nuestras reglas.
			raise SolitarioError("Movimiento inválido")

	def _carta_a_pila(self, origen, pila):
		"""Mueve la carta del tope entre dos pilas, si se puede, levanta SolitarioError si no."""
		if origen.es_vacia():
			raise SolitarioError("La pila está vacía")

		# Dejamos que PilaCarta haga las validaciones
		pila.apilar(origen.tope())
		origen.desapilar()

		if not origen.es_vacia() and origen.tope().boca_abajo:
			origen.tope().voltear()

	def _colocar_carta_pilas_tablero(self):
		"""Seteamos las pilas con una carta del mazo boca arriba"""
		for i in range(4):
			if not self.mesa.mazo.es_vacia():
				self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar())
				self.mesa.pilas_tablero[i].tope().voltear()
