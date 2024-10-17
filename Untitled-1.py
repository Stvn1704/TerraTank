import pygame


pygame.init()


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cuadro en Pygame")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


rect_x = 30
rect_y = 30
rect_width = 70
rect_height = 45
speed = 0.5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        rect_x -= speed  
    if keys[pygame.K_RIGHT]:
        rect_x += speed  
    if keys[pygame.K_UP]:
        rect_y -= speed  
    if keys[pygame.K_DOWN]:
        rect_y += speed

    screen.fill(WHITE)


    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height))


    pygame.display.flip()


pygame.quit()