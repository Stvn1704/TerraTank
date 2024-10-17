import pygame


pygame.init()


screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Cuadro en Pygame")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


rect_x = 50
rect_y = 50
rect_width = 100
rect_height = 75


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(WHITE)


    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height))


    pygame.display.flip()


pygame.quit()