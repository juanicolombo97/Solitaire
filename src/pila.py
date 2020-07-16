class Pila:
	'''Representa una pila con operaciones de apilar, desapilar y	
	verificar si esta vacia'''

	def __init__(self):
		'''Crea una pila vacia'''
		self.items = []
		self.len = 0

	def esta_vacia(self):
		return len(self.items) == 0

	def apilar(self, x):
		'''Apila el elemento x'''
		self.items.append(x)
		self.len += 1

	def desapilar(self):
		'''Devuelve el elemento del topey lo elimina de la pila.
		Si la pila está vacía levanta una excepción.'''
		if self.esta_vacia():
			raise IndexError("La pila esta vacia.")
		self.len -= 1
		return self.items.pop()

	def ver_tope(self):
		"""Muestra la última instancia de la pila, sin modificarla"""
		if self.esta_vacia():
			raise IndexError("La pila esta vacia.")
		return self.items[-1]

	def __len__(self):
		"""Devuelve la cantidad de elementos de la lista"""
		return self.len