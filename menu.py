import pygame
from Button import *
from client import *
pygame.init()

# Configuración de los botones
def set_Botones():
    Boton_alto = 50
    Boton_ancho = 220
    boton_jugar = Buttons("Image/Start_BTN.png", 300, 270, Boton_ancho, Boton_alto)
    boton_salir = Buttons("Image/Exit_BTN.png", 300, 350, Boton_ancho, Boton_alto)
    return boton_jugar, boton_salir

# Función para el menú principal
def Menu():
    screen = pygame.display.set_mode((800, 600))
    fondo_cargar = pygame.image.load("Image/BG.png")
    fondo_1 = pygame.transform.scale(fondo_cargar, (800, 600))

    logo_cargar = pygame.image.load("Image/Logo2.png") 
    logo = pygame.transform.scale(logo_cargar, (375, 500)) 

    boton_jugar, boton_salir = set_Botones()

    while True:
        pos_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if boton_jugar.is_clicked(mouse_pos):
                    play()  # Llamamos directamente a la función principal
                    return  # Terminamos el ciclo del menú
                if boton_salir.is_clicked(mouse_pos):
                    pygame.quit()

        screen.blit(fondo_1, (0, 0))
        screen.blit(logo, (230, 50))  
        boton_jugar.draw(screen)
        boton_salir.draw(screen)

        pygame.display.flip()

# Llamada inicial al menú
Menu()
