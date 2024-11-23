import math
import pygame
class Jugador:
    vida = 100
    daño = 10
    size = 180  # Tamaño del avión y de la hitbox

    def __init__(self, puerto_local, nombre):
        self.nombre = nombre
        self.id = puerto_local
        self.x = 0  # Posición inicial en X
        self.y = 0  # Posición inicial en Y
        self.ángulo = 0  # Ángulo inicial
        self.vida = Jugador.vida

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            print(f"{self.nombre} ha muerto")
        else:
            print(f"{self.nombre} recibió {cantidad} de daño. Vida restante: {self.vida}")

    def curarse(self, cantidad):
        self.vida += cantidad
        print(f"{self.nombre} se curó {cantidad}. Vida actual: {self.vida}")

    def actualizar_posición(self, x, y, ángulo):
        """Actualiza la posición y el ángulo del jugador."""
        self.x = x
        self.y = y
        self.ángulo = ángulo

    def obtener_hitbox(self):
        """Genera los puntos de la hitbox basada en la posición, tamaño y ángulo."""
        half_size = self.size // 2
        # Coordenadas relativas del cuadrado antes de rotar
        puntos = [
            (-half_size, -half_size),  # Esquina superior izquierda
            (half_size, -half_size),  # Esquina superior derecha
            (half_size, half_size),   # Esquina inferior derecha
            (-half_size, half_size)   # Esquina inferior izquierda
        ]

        # Rotar los puntos según el ángulo y trasladarlos a la posición del jugador
        puntos_rotados = [
            (
                self.x + px * math.cos(self.ángulo) - py * math.sin(self.ángulo),
                self.y + px * math.sin(self.ángulo) + py * math.cos(self.ángulo)
            )
            for px, py in puntos
        ]

        return puntos_rotados

    def dibujar_hitbox(self, screen, color=(255, 0, 0)):
        """Dibuja la hitbox del jugador en la pantalla."""
        puntos = self.obtener_hitbox()
        pygame.draw.polygon(screen, color, puntos, 1)  # Dibuja un polígono alrededor del hitbox


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



