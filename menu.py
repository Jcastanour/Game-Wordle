# Modulos y librerias importados:
import pygame
import sys
from Game import *

# Inicialización de las funcionalidades de pygame
pygame.init()
WIDTH = 600
HEIGHT = 800

#Imagenes
jugar_imagen = pygame.image.load("jugar.png")
exit_imagen = pygame.image.load("exit.png")
cuatro_imagen = pygame.image.load("4.png")
cinco_imagen = pygame.image.load("5.png")
seis_imagen = pygame.image.load("6.png")
siete_imagen = pygame.image.load("7.png")
ocho_imagen = pygame.image.load("8.png")

# Inicializamos la pantalla con su respectivo tamaño(px):
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Menu principal")

class Escena:
    MENU_PRINCIPAL = 0
    MENU_JUGAR = 1
    JUEGO = 2

def menu_principal():
    global running
    global escena
    screen.fill(BLUE)
    jugar = screen.blit(jugar_imagen, (200, 200))
    exit = screen.blit(exit_imagen, (200, 400))

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if jugar.collidepoint(event.pos):
                escena = Escena.MENU_JUGAR
            if exit.collidepoint(event.pos):
                running = False

# Definimos botones que se inicializan al entrar en el menu de jugar
def menu_jugar():
    global escena
    global running
    global nivel

    dificultad_4 = screen.blit(cuatro_imagen,(300, 50))
    dificultad_5 = screen.blit(cinco_imagen,(300, 200))
    dificultad_6 = screen.blit(seis_imagen,(300, 350))
    dificultad_7 = screen.blit(siete_imagen,(300, 500))
    dificultad_8 = screen.blit(ocho_imagen,(300, 650))
    volver = screen.blit(exit_imagen,(40, 650))
    
    # Gestion de eventos (menu dificultades):
    for event in pygame.event.get():
        # 1.Salida con la x superior izquierda
        if event.type == pygame.QUIT:
            running = False
        # 2. Botones del menu de dificultades
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if volver.collidepoint(event.pos):
                escena = Escena.MENU_PRINCIPAL
            elif dificultad_4.collidepoint(event.pos):
                escena = Escena.JUEGO
                nivel = 4
            elif dificultad_5.collidepoint(event.pos):
                escena = Escena.JUEGO
                nivel = 5
            elif dificultad_6.collidepoint(event.pos):
                escena = Escena.JUEGO
                nivel = 6
            elif dificultad_7.collidepoint(event.pos):
                escena = Escena.JUEGO
                nivel = 7
            elif dificultad_8.collidepoint(event.pos):
                escena = Escena.JUEGO
                nivel = 8
            
        
def juego():
    global running
    global escena
    global nivel

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                escena = Escena.MENU_PRINCIPAL
                return

        game = Game(nivel)   
        game.nuevo()
        game.run()
        print(nivel)
        pygame.display.flip()


# Bucle principal del juego:
running = True
# Variable que me facilita el primer menu y el segundo menu
escena = Escena.MENU_PRINCIPAL
while running:
    
    # Gestion de eventos(menu):
    for event in pygame.event.get():
        # 1.Salida con la x superior izquierda
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)

    if escena == Escena.MENU_PRINCIPAL:
        # Detectar clic en el botón Jugar y salir
        menu_principal()
    elif escena == Escena.MENU_JUGAR:
        #Botones de niveles
        menu_jugar()

    elif escena == Escena.JUEGO:
        #Juego y logica
        juego()

    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar instancias de pygame, y procesos forzosamente:
pygame.quit()
sys.exit()