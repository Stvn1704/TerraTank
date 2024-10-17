""" aqui hice lo basico basico de clases, no se como funciona el movimiento de un personaje en el mapa
 asi que no tengo idea de si es con ubicaciones tipo coordenadas, por eso hice la calse mapa
 se puede eliminar si se requiere, de resto imagino seran los metodos necesarios para las interacciones en el juego"""

class Personaje:
    def __init__(self, nombre, vida, daño, posicion=(0, 0)):
        self.nombre = nombre
        self.vida = vida
        self.daño = daño
        self.posicion = posicion
    
    def mover(self, nueva_posicion):
        self.posicion = nueva_posicion
        print(f"{self.nombre} se ha movido a la posición {self.posicion}")
    
    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            print(f"{self.nombre} ha muerto")
        else:
            print(f"{self.nombre} recibió {cantidad} de daño. Vida restante: {self.vida}")
    
    def curarse(self, cantidad):
        self.vida += cantidad
        print(f"{self.nombre} se curó {cantidad}. Vida actual: {self.vida}")


class Obstaculo:
    def __init__(self, tipo, posicion):
        self.tipo = tipo
        self.posicion = posicion

    def __repr__(self):
        return f"Obstáculo({self.tipo}) en {self.posicion}"


class ObjetoCuracion:
    def __init__(self, cantidad, posicion):
        self.cantidad = cantidad
        self.posicion = posicion
    
    def usar(self, personaje):
        personaje.curarse(self.cantidad)
        print(f"{personaje.nombre} ha recogido un objeto de curación en la posición {self.posicion}")


class Mapa:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.obstaculos = []
        self.objetos_curacion = []

    def agregar_obstaculo(self, obstaculo):
        self.obstaculos.append(obstaculo)
    
    def agregar_objeto_curacion(self, objeto):
        self.objetos_curacion.append(objeto)
    
    def mostrar_mapa(self):
        print(f"Mapa de {self.ancho}x{self.alto}")
        for obstaculo in self.obstaculos:
            print(obstaculo)
        for objeto in self.objetos_curacion:
            print(f"Objeto de curación en {objeto.posicion}, que cura {objeto.cantidad}")


jugador = Personaje("Héroe", 100, 20)

mapa = Mapa(10, 10)

mapa.agregar_obstaculo(Obstaculo("Roca", (3, 3)))

mapa.agregar_objeto_curacion(ObjetoCuracion(30, (5, 5)))

jugador.mover((4, 4))

jugador.recibir_daño(40)

objeto_curacion = ObjetoCuracion(20, (4, 4))
objeto_curacion.usar(jugador)

mapa.mostrar_mapa()
