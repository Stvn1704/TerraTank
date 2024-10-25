import pygame
import socket
import json
import os
import math

# Definición de la clase Jugador
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.size = 100  # Puedes ajustar el tamaño según tus necesidades

# Obtener el nombre del jugador antes de inicializar Pygame
nombre = input("Ingresa nombre: ")

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TerraPlane")

# Inicializar el reloj para la sincronización de frames
clock = pygame.time.Clock()

# Configuración del socket
server_address = ('localhost', 5555)  # Asegúrate de que coincida con el servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexión al servidor
try:
    client_socket.connect(server_address)  # Conectar al servidor
    print("Conexión exitosa al servidor.")
except ConnectionRefusedError:
    print("No se pudo conectar al servidor. Asegúrate de que esté en ejecución.")
    exit()

# Instanciar el jugador
Jugador1 = Jugador(nombre)  # Asegúrate de que la clase Jugador esté definida correctamente
client_socket.send(nombre.encode('utf-8'))  # Enviar el nombre del jugador al servidor

# Configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Cargar imagen de fondo
background_image = pygame.image.load('fondo_nuevo.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH * 12, HEIGHT * 12))

# Obtener dimensiones de la imagen de fondo
background_width = background_image.get_width()
background_height = background_image.get_height()

# Posición inicial del avión (centrado en la pantalla)
arrow_x = WIDTH // 2
arrow_y = HEIGHT // 2

# Velocidades
player_speed = 25  # Velocidad del avión
bullet_speed = 25  # Velocidad de las balas

# Inicializar offset (desplazamiento del fondo)
offset_x = 0
offset_y = 0

frames = []
frame_count = 0
frame_duration = 5
current_frame = 0

frame_directory = "Movimiento"
new_frame_size = (Jugador1.size, Jugador1.size)

# Cargar los cuadros de animación del avión
for filename in sorted(os.listdir(frame_directory)):
    if filename.endswith('.gif'):
        frame = pygame.image.load(os.path.join(frame_directory, filename))
        resized_frame = pygame.transform.scale(frame, new_frame_size)
        frames.append(resized_frame)

print(f"Se han cargado {len(frames)} cuadros.")

# Clase para los proyectiles (balas)
class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = bullet_speed

    def update(self):
        # Actualiza la posición del proyectil sin límites
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 5)

projectiles = []

# Márgenes de seguridad para el movimiento del avión
safety_margin = 100

# Inicializar el bucle del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Disparar con el botón del ratón
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botón izquierdo
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - arrow_x
            dy = mouse_y - arrow_y
            angle = math.atan2(dy, dx)

            projectile_x = arrow_x + 60 * math.cos(angle)
            projectile_y = arrow_y + 60 * math.sin(angle)
            projectiles.append(Projectile(projectile_x, projectile_y, angle))

     # Movimiento del avión con límites del fondo
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        arrow_x -= player_speed
        if arrow_x < safety_margin:
            arrow_x = safety_margin
            offset_x = max(0, offset_x - player_speed)  # Mover el fondo a la izquierda

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        arrow_x += player_speed
        if arrow_x > WIDTH - safety_margin:
            arrow_x = WIDTH - safety_margin
            offset_x = min(background_width - WIDTH, offset_x + player_speed)  # Mover el fondo a la derecha

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        arrow_y -= player_speed
        if arrow_y < safety_margin:
            arrow_y = safety_margin
            offset_y = max(0, offset_y - player_speed)  # Mover el fondo hacia arriba

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        arrow_y += player_speed
        if arrow_y > HEIGHT - safety_margin:
            arrow_y = HEIGHT - safety_margin
            offset_y = min(background_height - HEIGHT, offset_y + player_speed)  # Mover el fondo hacia abajo

    # Enviar la posición del jugador al servidor
    data = {"type": "move", "x": arrow_x, "y": arrow_y}
    client_socket.send(json.dumps(data).encode('utf-8'))

    # Actualizar el fondo
    screen.blit(background_image, (-offset_x, -offset_y))

    # Rotar el avión hacia el puntero del ratón
    if len(frames) > 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - arrow_x
        dy = mouse_y - arrow_y
        angle = math.atan2(dy, dx)

        current_image = frames[current_frame]
        rotated_image = pygame.transform.rotate(current_image, -math.degrees(angle))
        rotated_rect = rotated_image.get_rect(center=(arrow_x, arrow_y))
        screen.blit(rotated_image, rotated_rect.topleft)

    # Actualizar y dibujar los proyectiles (balas)
    for projectile in projectiles:
        projectile.update()
        projectile.draw(screen)

    # Dibujar el mini mapa
    mini_map_width = 200
    mini_map_height = 200
    mini_map_rect = pygame.Rect(20, HEIGHT - mini_map_height - 20, mini_map_width, mini_map_height)

    # Dibujar el rectángulo del mini mapa
    pygame.draw.rect(screen, BLACK, mini_map_rect, 2)

    # Dibujar el fondo del mini mapa
    mini_map_scale_x = mini_map_width / background_image.get_width()
    mini_map_scale_y = mini_map_height / background_image.get_height()

    mini_map_background = pygame.transform.scale(background_image, (int(background_image.get_width() * mini_map_scale_x), int(background_image.get_height() * mini_map_scale_y)))
    screen.blit(mini_map_background, mini_map_rect.topleft)

    # Calcular la posición del avión en el mini mapa de manera proporcional
    mini_map_arrow_x = ((arrow_x + offset_x) / background_image.get_width()) * mini_map_width + mini_map_rect.x
    mini_map_arrow_y = ((arrow_y + offset_y) / background_image.get_height()) * mini_map_height + mini_map_rect.y

    # Limitar la posición del punto verde dentro del rectángulo del minimapa
    mini_map_arrow_x = max(mini_map_rect.x, min(mini_map_arrow_x, mini_map_rect.right))
    mini_map_arrow_y = max(mini_map_rect.y, min(mini_map_arrow_y, mini_map_rect.bottom))

    # Dibujar la posición del avión en el mini mapa
    pygame.draw.circle(screen, GREEN, (int(mini_map_arrow_x), int(mini_map_arrow_y)), 5)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la tasa de frames
    clock.tick(60)  # Limitar a 60 FPS# Actualizar el fondo
    screen.blit(background_image, (-offset_x, -offset_y))

    # Rotar el avión hacia el puntero del ratón
    if len(frames) > 0:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - arrow_x
        dy = mouse_y - arrow_y
        angle = math.atan2(dy, dx)

        current_image = frames[current_frame]
        rotated_image = pygame.transform.rotate(current_image, -math.degrees(angle))
        rotated_rect = rotated_image.get_rect(center=(arrow_x, arrow_y))
        screen.blit(rotated_image, rotated_rect.topleft)

    # Actualizar y dibujar los proyectiles (balas)
    for projectile in projectiles:
        projectile.update()
        projectile.draw(screen)

    # Dibujar el mini mapa
    mini_map_width = 200
    mini_map_height = 200
    mini_map_rect = pygame.Rect(20, HEIGHT - mini_map_height - 20, mini_map_width, mini_map_height)

    # Dibujar el rectángulo del mini mapa
    pygame.draw.rect(screen, BLACK, mini_map_rect, 2)

    # Dibujar el fondo del mini mapa
    mini_map_scale_x = mini_map_width / background_image.get_width()
    mini_map_scale_y = mini_map_height / background_image.get_height()

    mini_map_background = pygame.transform.scale(background_image, (int(background_image.get_width() * mini_map_scale_x), int(background_image.get_height() * mini_map_scale_y)))
    screen.blit(mini_map_background, mini_map_rect.topleft)

    # Calcular la posición del avión en el mini mapa de manera proporcional
    mini_map_arrow_x = ((arrow_x + offset_x) / background_image.get_width()) * mini_map_width + mini_map_rect.x
    mini_map_arrow_y = ((arrow_y + offset_y) / background_image.get_height()) * mini_map_height + mini_map_rect.y

    # Limitar la posición del punto verde dentro del rectángulo del minimapa
    mini_map_arrow_x = max(mini_map_rect.x, min(mini_map_arrow_x, mini_map_rect.right))
    mini_map_arrow_y = max(mini_map_rect.y, min(mini_map_arrow_y, mini_map_rect.bottom))

    # Dibujar la posición del avión en el mini mapa
    pygame.draw.circle(screen, GREEN, (int(mini_map_arrow_x), int(mini_map_arrow_y)), 5)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la tasa de frames
    clock.tick(60)  # Limitar a 60 FPS

# Cierre de la conexión y Pygame
client_socket.close()
pygame.quit()

