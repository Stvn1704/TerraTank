import pygame
import math
import os

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Animación de tanque que apunta y dispara")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

arrow_x = 250
arrow_y = 250
speed = 5

frames = []
frame_count = 0
frame_duration = 5
current_frame = 0
 
frame_directory = "Movimiento"

for filename in sorted(os.listdir(frame_directory)):
    if filename.endswith('.gif'):
        frame = pygame.image.load(os.path.join(frame_directory, filename))
        frames.append(frame)

print(f"Se han cargado {len(frames)} cuadros.")

class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 5)

projectiles = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - arrow_x
                dy = mouse_y - arrow_y
                angle = math.atan2(dy, dx)

                projectile_x = arrow_x + 60 * math.cos(angle)
                projectile_y = arrow_y + 60 * math.sin(angle)
                projectiles.append(Projectile(projectile_x, projectile_y, angle))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - arrow_x
    dy = mouse_y - arrow_y
    angle = math.atan2(dy, dx)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        arrow_x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        arrow_x += speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        arrow_y -= speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        arrow_y += speed

    screen.fill(WHITE)

    frame_count += 1
    if frame_count >= frame_duration:
        frame_count = 0
        current_frame = (current_frame + 1) % len(frames)

    if len(frames) > 0:
        current_image = frames[current_frame]

        rotated_image = pygame.transform.rotate(current_image, -math.degrees(angle))
        rotated_rect = rotated_image.get_rect(center=(arrow_x, arrow_y))

        screen.blit(rotated_image, rotated_rect.topleft)

    for projectile in projectiles:
        projectile.update()
        projectile.draw(screen)

    pygame.display.flip()

pygame.quit()