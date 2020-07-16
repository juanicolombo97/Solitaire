from carta import *
from pila import *
import random

class SolitarioError(Exception):
    """Tipo de Exception para todos los errores del Solitario."""
    # No tocar nada acá, el pass está bien como toda implementación :).
    pass


class PilaCartas:
    """Representa una pila de cartas en el tablero."""

    def __init__(self, pila_visible=False, valor_inicial=None, puede_desapilar=True, criterio_apilar=None, criterio_mover=None):
        """Se construye una pila vacía. El comportamiento estará regido por:
            pila_visible: Bool. ¿Al imprimir la pila se muestra sólo la carta
                del tope o son visibles todas las cartas de la pila?
            valor_inicial: Número 1 al 13. Si está presente sólo se puede
                apilar ese valor sobre una pila vacía.
            puede_desapilar: Bool. ¿En la pila se apila y se desapila o sólo
                se puede apilar?
            criterio_apilar: f(a, b). Si la pila no está vacía y tope() == a,
                f(a, b) indica si puede apilarse la carta b sobre la pila.
            criterio_mover: f(a, b). Siendo la pila una secuencia de cartas
                [cn, ..., c2, c1, c0], donde c0 es el tope, voy a poder mover
                en bloque parte de la pila siempre y cuando f(c1, c0),
                f(c2, c1), etc. hasta que la función falle.
        Todos los parámetros son optativos y tienen valores por omisión. En
        el caso de los parámetros que sean None, los mismos no se
        considerarán como restricciones (por ejemplo, si valor_inicial == None
        se desactivará el chequeo de valor_inicial)."""
        self.pila_visible = pila_visible
        self.valor_inicial = valor_inicial
        self.puede_desapilar = puede_desapilar
        self.criterio_apilar = criterio_apilar
        self.criterio_mover = criterio_mover
        self.cartas = Pila()

    def es_vacia(self):
        """Indica si la pila se encuentra vacía."""
        return self.cartas.esta_vacia()

    def tope(self):
        """Devuelve la carta tope de la pila.
        Levanta SolitarioError en caso de error."""
        if self.cartas.esta_vacia():
            raise SolitarioError("La pila no tiene cartas.")
        return self.cartas.ver_tope()

    def apilar(self, carta, forzar=False):
        """Apila una carta en la pila. Si forzar es True desactiva los chequeos
        sobre el valor_inicial y el criterio_apilar.
        Levanta SolitarioError en caso de no poder apilar."""
        if not forzar:
            if self.valor_inicial != None and self.es_vacia() and carta.valor != self.valor_inicial:
                raise SolitarioError("No es posible apilar la carta. No coinciden los valores.")
            elif self.criterio_apilar != None and not self.es_vacia() and not self.criterio_apilar(self.tope(), carta):
                raise SolitarioError("No es posible apilar la carta. No cumple el criterio para apilar.")
            self.cartas.apilar(carta)
        else:
            self.cartas.apilar(carta)


    def desapilar(self):
        """Desapila una carta. Levanta SolitarioError en caso de no poder
        desapilar."""
        if not self.puede_desapilar:
            raise SolitarioError("La pila no puede desapilar.")
        if self.es_vacia():
            raise SolitarioError("La pila de cartas esta vacia.")
        return self.cartas.desapilar()

    def mover(self, origen):
        """Siendo origen otra PilaCartas intenta mover un subpilón de cartas
        de origen sobre la pila.
        Las primera carta que se apile sobre la pila debe validar
        criterio_apilar mientras que la cantidad de cartas máxima a mover
        desde origen dependerá de criterio_mover.
        Independientemente del criterio_mover no podrán moverse cartas que se
        encuentren boca abajo y sobre una carta boca abajo puede apilarse
        cualquier valor.
        Debe levantarse SolitarioError en caso de no poder mover ninguna carta
        de origen a la pila."""
        aux = PilaCartas()
        se_hicieron_movimientos = False
        while not origen.es_vacia() and not origen.tope().boca_abajo:
            # Recorre la pila de cartas boca arriba
            try:
                # Intenta apilarlas en el destino, en caso de ser posible sale de bucle
                self.apilar(origen.tope())
                origen.desapilar()
                while not aux.es_vacia():
                    self.apilar(aux.desapilar())
                se_hicieron_movimientos = True
                break
            except SolitarioError:
                # Si no es posible se guarda la variable en un auxiliar
                aux.apilar(origen.desapilar())
                # Compara con el criterio de mover en caso falso no sigue buscando coincidencias
                if not self.criterio_mover(aux.tope(), origen.tope()):
                    break
        while not aux.es_vacia():
            origen.apilar(aux.desapilar(), forzar = True)
        if not se_hicieron_movimientos:
            raise SolitarioError("No se puede mover ninguna carta.")

    def mezclar(self):
        '''Toma una pila de cartas y las mezcla'''
        lista = []
        while not self.es_vacia():
            elemento = self.cartas.desapilar()
            lista.append(elemento)
        random.shuffle(lista)
        while lista != []:
            self.apilar(lista.pop())


    def __str__(self):
        """Devuelve una representación de la pila.
        La misma será una X si la pila¿'' estuviera vacía.
        Si pila_visible == True se representará a la pila como todas las
        cartas de base a tope separadas por espacios. Si no sólo se
        representará según el tope."""
        if self.es_vacia():
            return "X"
        aux = PilaCartas()
        resultado = ""
        if self.pila_visible:
            while not self.es_vacia():
                aux.apilar(self.desapilar())
            while not aux.es_vacia():
                elemento = aux.desapilar()
                resultado += str(elemento) + " "
                self.apilar(elemento, forzar = True)
            return resultado
        else:
            return str(self.tope())

    
    def __repr__(self):
        """Ídem __str__."""
        return self.__str__()

    def __len__(self):
        """Devuelve la cantidad de cartas de la pila"""
        return len(self.cartas)