import pygame

#INTERFACES
# COLORS (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)
BGCOLOUR = (40, 40, 40)
BLUE = (60, 100, 150)

class Casilla:
    def __init__(self, x, y, letter="", colour=None):
        self.x, self.y = x, y
        self.letter = letter
        self.colour = colour
        self.width, self.height = 80, 80
        self.font_size = int(60 * (80/100))
        self.create_font()

    def create_font(self):
        font = pygame.font.SysFont("Consolas", self.font_size) #fuente usada para cada casilla
        self.render_letter = font.render(self.letter, True, WHITE)  #se especifica que tendra un borde mas suave y color blanco
        self.font_width, self.font_height = font.size(self.letter) #alto y ancho que tendra la letra

    def draw(self, screen):
        if self.colour is None:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2) #pinta de blanco con bordes negro, 2 es el grosor del borde
        else:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

        if self.letter != "":
            self.font_x = self.x + (self.width / 2) - (self.font_width / 2) #para centrar la letra
            self.font_y = self.y + (self.height / 2) - (self.font_height / 2) #para centrar la letra
            letter = pygame.transform.scale(self.render_letter, (self.font_width, self.font_height)) #se escala la letra para que quede bien ajustada en la casilla
            screen.blit(letter, (self.font_x, self.font_y)) #se dibuja la letra en las coordenadas exactas


class UIElement: #animaciones
    def __init__(self, x, y, text, colour, font_size=30):
        self.x, self.y = x, y
        self.text = text
        self.colour = colour
        self.font_size = font_size
        self.transparencia = 0 #transparencia del elemento
        self.create_font()

    def create_font(self):
        font = pygame.font.SysFont("Consolas", self.font_size)
        self.original_surface = font.render(self.text, True, self.colour)
        self.text_surface = self.original_surface.copy() #copia de superficie original
        self.alpha_surface = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA) #superficie adicional para la transparencia

    def draw(self, screen):
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.transparencia))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(self.text_surface, (self.x, self.y))

    def fade_out(self):
        self.transparencia = max(self.transparencia - 10, 0)
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.transparencia))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def fade_in(self):
        self.transparencia = min(self.transparencia + 10, 255)
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.transparencia))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
