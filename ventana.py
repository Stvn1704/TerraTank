import pygame
import math
import os
import clases


pygame.init()

pantalla = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Animación de tanque que apunta y dispara")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

arrow_x = 100
arrow_y = 100
speed = .5


frames = []
frame_count = 0
frame_duration = 100 #cambiar velocidad de animacion del gif
current_frame = 0


frame_directory = "Movimiento"

for filename in sorted(os.listdir(frame_directory)):
    if filename.endswith('.gif'):
        frame = pygame.image.load(os.path.join(frame_directory, filename))
        frames.append(frame)


jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - arrow_x
    dy = mouse_y - arrow_y
    angulo = math.atan2(dy, dx)

 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        arrow_x -= speed 
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        arrow_x += speed 
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        arrow_y -= speed 
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        arrow_y += speed 

  
    pantalla.fill(WHITE)

    
    frame_count += 1
    if frame_count >= frame_duration:
        frame_count = 0
        current_frame = (current_frame + 1) % len(frames)


    current_image = frames[current_frame]

  
    rotated_image = pygame.transform.rotate(current_image, -math.degrees(angulo))
    rotated_rect = rotated_image.get_rect(center=(arrow_x, arrow_y))


    pantalla.blit(rotated_image, rotated_rect.topleft)

    pygame.display.flip()

pygame.quit()
