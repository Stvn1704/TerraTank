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

boton_jugar = Buttons("Image/Start_BTN.png", 300, 270, 50, 50)
boton_salir = Buttons("Image/Exit_BTN.png", 300, 350, 60, 60)