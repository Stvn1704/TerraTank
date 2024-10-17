import pygame
import math
import os

# Inicializamos Pygame
pygame.init()

# Definimos el tamaño de la ventana
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Animación de tanque que apunta y dispara")

# Definimos colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definimos la posición inicial y velocidad
arrow_x = 100
arrow_y = 100
speed = 5

# Cargar los cuadros de la animación
frames = []
frame_count = 0
frame_duration = 5  # Cuántos ciclos de reloj mostrar cada cuadro
current_frame = 0

# Cargar imágenes de un directorio específico
frame_directory = "Movimiento"  # Cambia esto al directorio donde están tus cuadros

for filename in sorted(os.listdir(frame_directory)):
    if filename.endswith('.gif'):  # Asegúrate de que sean archivos PNG
        frame = pygame.image.load(os.path.join(frame_directory, filename))
        frames.append(frame)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calcular el ángulo entre el tanque y el mouse
    dx = mouse_x - arrow_x
    dy = mouse_y - arrow_y
    angle = math.atan2(dy, dx)

    # Mover el tanque con las teclas de flechas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        arrow_x -= speed  # Mover a la izquierda
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        arrow_x += speed  # Mover a la derecha
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        arrow_y -= speed  # Mover hacia arriba
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        arrow_y += speed  # Mover hacia abajo

    # Limpiar la pantalla
    screen.fill(WHITE)

    # Actualizar el cuadro de la animación
    frame_count += 1
    if frame_count >= frame_duration:
        frame_count = 0
        current_frame = (current_frame + 1) % len(frames)  # Avanzar al siguiente cuadro

    # Obtener el cuadro actual de la animación
    current_image = frames[current_frame]

    # Rotar la imagen según el ángulo calculado
    rotated_image = pygame.transform.rotate(current_image, -math.degrees(angle))
    rotated_rect = rotated_image.get_rect(center=(arrow_x, arrow_y))

    # Dibujar la imagen rotada
    screen.blit(rotated_image, rotated_rect.topleft)

    # Actualizar la pantalla
    pygame.display.flip()

# Salimos de Pygame
pygame.quit()
