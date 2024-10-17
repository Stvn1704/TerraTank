import pygame
import math

# Inicializamos Pygame
pygame.init()

# Definimos el tamaño de la ventana
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Flecha que apunta y dispara")

# Definimos colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definimos la posición, tamaño y velocidad de la flecha
arrow_x = 250
arrow_y = 250
arrow_width = 60
arrow_height = 10
speed = 1

# Crear una superficie para la flecha (una flecha dibujada)
arrow_surf = pygame.Surface((arrow_width, arrow_height), pygame.SRCALPHA)  # Superficie con transparencia
pygame.draw.polygon(arrow_surf, BLACK, [(0, 5), (50, 5), (50, 0), (60, 10), (50, 20), (50, 15), (0, 15)])

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calcular el ángulo entre la flecha y el mouse
    dx = mouse_x - arrow_x
    dy = mouse_y - arrow_y
    angle = math.atan2(dy, dx)  # Ángulo en radianes

    # Mover la flecha con las teclas de flechas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        arrow_x -= speed  # Mover a la izquierda
    if keys[pygame.K_RIGHT]:
        arrow_x += speed  # Mover a la derecha
    if keys[pygame.K_UP]:
        arrow_y -= speed  # Mover hacia arriba
    if keys[pygame.K_DOWN]:
        arrow_y += speed  # Mover hacia abajo

    # Limpiar la pantalla
    screen.fill(WHITE)

    # Rotar la superficie de la flecha según el ángulo calculado
    rotated_surf = pygame.transform.rotate(arrow_surf, -math.degrees(angle))
    rotated_rect = rotated_surf.get_rect(center=(arrow_x, arrow_y))

    # Dibujar la flecha rotada
    screen.blit(rotated_surf, rotated_rect.topleft)

    # Actualizar la pantalla
    pygame.display.flip()

# Salimos de Pygame
pygame.quit()
