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
                    pedir_nombre()  # Llamamos a la función para pedir el nombre
                    return  # Terminamos el ciclo del menú, una vez que se ingresa el nombre
                if boton_salir.is_clicked(mouse_pos):
                    pygame.quit()

        screen.blit(fondo_1, (0, 0))
        screen.blit(logo, (230, 50))  
        boton_jugar.draw(screen)
        boton_salir.draw(screen)

        pygame.display.flip()

# Función para pedir el nombre del jugador
def pedir_nombre():
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 48)
    input_text = ""  # Aquí se almacenará el texto ingresado por el jugador

    # Fondo y elementos de la pantalla
    fondo_cargar = pygame.image.load("Image/BG.png")
    fondo_1 = pygame.transform.scale(fondo_cargar, (800, 600))
    prompt = font.render("Ingresa tu nombre:", True, (255, 255, 255))
    input_surface = font.render(input_text, True, (255, 255, 255))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Cuando se presiona Enter, confirmamos el nombre
                    if input_text:  # Solo iniciamos si el campo no está vacío
                        play(input_text)  # Llamamos a la función principal pasando el nombre
                        return  # Terminamos el ciclo de pedir el nombre
                elif event.key == pygame.K_BACKSPACE:  # Si se presiona Backspace, eliminamos un caracter
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  # Añadimos el caracter ingresado

            screen.blit(fondo_1, (0, 0))  # Fondo
            screen.blit(prompt, (250, 200))  # Texto que indica que se ingrese el nombre
            input_surface = font.render(input_text, True, (255, 255, 255))  # Texto del nombre ingresado
            screen.blit(input_surface, (250, 300))  # Mostramos el nombre que se va escribiendo

            pygame.display.flip()



# Llamada inicial al menú
Menu()