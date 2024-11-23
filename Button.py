import pygame

class Buttons:
    def __init__(self, image_path, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        # Comprobar si el botón fue clickeado o si el mouse esta encima del boton
        return self.rect.collidepoint(pos)
