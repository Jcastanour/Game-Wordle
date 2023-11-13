# Modulos y librerias importados:
import pygame
import sys
# Inicialización de las funcionalidades de pygame
pygame.init()

# Inicializamos la pantalla con su respectivo tamaño(px):
screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Wordle")


# Definimos los colores:
azul = (60, 100, 150)
gris = (91, 91, 91)
amarillo = (200, 200, 91)
verde = (0, 200, 100)
negro = (0,0,0)

# Definimos las fuentes(texto):
jugar_imagen = pygame.image.load("jugar.png")
exit_imagen = pygame.image.load("exit.png")
cuatro_imagen = pygame.image.load("4.png")
cinco_imagen = pygame.image.load("5.png")
seis_imagen = pygame.image.load("6.png")
siete_imagen = pygame.image.load("7.png")
ocho_imagen = pygame.image.load("8.png")

class Escena:
    MENU_PRINCIPAL = 0
    MENU_JUGAR = 1
    JUEGO = 2

def menu_principal():
    screen.fill(azul)
    screen.blit(jugar_imagen, (200, 200))
    screen.blit(exit_imagen, (200, 400))

# Definimos botones:
# Definimos botones que se inicializan al entrar en el menu de jugar
def menu_jugar():
    global escena
    global running
    global cantidad_letras

    dificultad_4 = pygame.Rect(250, 300, 200, 100)
    dificultad_5 = pygame.Rect(250, 450, 200, 100)
    dificultad_6 = pygame.Rect(250, 600, 200, 100)
    dificultad_7 = pygame.Rect(250, 750, 200, 100)
    dificultad_8 = pygame.Rect(250, 900, 200, 100)
    volver = pygame.Rect(40, 650, 200, 100)

    dificultad_4 = screen.blit(cuatro_imagen,(300, 50))
    dificultad_5 = screen.blit(cinco_imagen,(300, 200))
    dificultad_6 = screen.blit(seis_imagen,(300, 350))
    dificultad_7 = screen.blit(siete_imagen,(300, 500))
    dificultad_8 = screen.blit(ocho_imagen,(300, 650))
    volver = screen.blit(exit_imagen,(40, 650))

    
    # Gestion de eventos (meni dificultades):
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
                cantidad_letras = 4
            elif dificultad_5.collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 5
            elif dificultad_6.collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 6
            elif dificultad_7.collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 7
            elif dificultad_8.collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 8
    print(escena)
            
        
def juego():
    global running
    global escena
    global cantidad_letras

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                escena = Escena.MENU_PRINCIPAL
                return

        # Lógica de juego aquí (por ejemplo, manejo de eventos, actualizaciones, etc.)
        # En este ejemplo, simplemente dibujamos la pantalla y mostramos la cantidad de letras
        screen.fill(negro)
        pygame.draw.rect(screen, azul, (100, 100, 400, 200))
        pygame.draw.rect(screen, azul, (100, 400, 400, 200))
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render(f"Cantidad de letras: {cantidad_letras}", True, (255, 255, 255))
        screen.blit(text, (150, 250))
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

    screen.fill(azul)

    if escena == Escena.MENU_PRINCIPAL:
        menu_principal()
        # Detectar clic en el botón Jugar
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(200, 200, 200, 100).collidepoint(event.pos):
                escena = Escena.MENU_JUGAR

    elif escena == Escena.MENU_JUGAR:
        menu_jugar()
        # Aquí también, detectar clic en el botón Jugar y cambiar la escena
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(250, 300, 200, 100).collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 4
            elif pygame.Rect(250, 450, 200, 100).collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 5
            elif pygame.Rect(250, 600, 200, 100).collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 6
            elif pygame.Rect(250, 750, 200, 100).collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 7
            elif pygame.Rect(250, 900, 200, 100).collidepoint(event.pos):
                escena = Escena.JUEGO
                cantidad_letras = 8

    elif escena == Escena.JUEGO:
        juego()

    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar instancias de pygame, y procesos forzosamente:
pygame.quit()
sys.exit()