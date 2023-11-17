import random
import pygame
from settings import *
import sys
from collections import deque

# Funcion que gestiona cual es la cantidad de caracteres que hay en una palabra(la que hay que adivinar)
def diccionary(diccionario,palabra_oculta,nivel): #o(nivel) nivel entre 4 y 8 - nivel siempre es constante para todo la partida --> o(1)
    for i in range(nivel):
        diccionario[palabra_oculta[i]] = 0
        
    for i in range(nivel):
        if palabra_oculta[i] in diccionario:
            diccionario[palabra_oculta[i]] +=1
        else:
            diccionario[palabra_oculta[i]] = 1

# Funcion que convierte nuestro lemario en formato de texto, a un diccionario en base a su longitud de palabras (4 a 8)
def crea_lista_palabras(lemario):
        # Abrimos el txt y añadimos a cada clave en el diccionario una palabra a su valor(set)
        with open ('palabras.txt','r',encoding='utf-8') as file:
            for linea in file:
                palabra = ' '.join(linea.split()).rstrip().strip("-") 
                longitud = len(palabra)
        
                if longitud == 4:
                    lemario[4].add(palabra)  
                if longitud == 5:
                    lemario[5].add(palabra)    
                if longitud == 6:
                    lemario[6].add(palabra) 
                if longitud == 7:
                    lemario[7].add(palabra) 
                if longitud == 8:
                    lemario[8].add(palabra) 

# Se crea el lemario(como diccionario)(solo sucede una vez)
lemario = {longitud: set() for longitud in range(4,9)} 
crea_lista_palabras(lemario)

# Clase que tiene las funciones y parametros de cada partida
class Game:
    def __init__(self,nivel, lemario = lemario):
        self.lemario = lemario
        pygame.init()
        self.ganadas = 0
        self.perdidas = 0
        self.nivel = nivel
        self.WIDTH = 120*nivel
        self.MARGIN_X = int((self.WIDTH - (self.nivel * (80 + 10))) / 2) 
        self.MARGIN_Y = int((800 - (6 * (80 + 10))) / 2)  
        self.screen = pygame.display.set_mode((self.WIDTH, 800))
        pygame.display.set_caption("JUEGO WORDLE")
        self.clock = pygame.time.Clock()

        # Se crea el lemario que contiene todas las palabras(diccionario de sets)
        # self.lemario = {longitud: set() for longitud in range(4,9)} 
        # self.crea_lista_palabras()
        self.letters_text = UIElement(self.MARGIN_X, 70, "Pai te faltan letras", WHITE)
        self.letters_text_noesta = UIElement(self.MARGIN_X - 20, 70, "Nonas, esa no esta en el lemario", WHITE,23)
        self.menu = False


    # Funcion que: Crea palabra a adivinar y diccionario con cantidad de caracteres en cada palabra. 
    # Tambien crea la cantidad de casillas del juego
    def nuevo(self):
        
        self.palabra_oculta = random.sample(self.lemario.get(self.nivel),1)[0].lower() #o(1)
        self.diccionario = dict()

        # Si se quiere mostrar la palabra correcta en consola:
        print(self.palabra_oculta)

        diccionary(self.diccionario,self.palabra_oculta,self.nivel)

        self.text = ""
        self.fila_actual = 0
        self.casillas = [[],[],[],[],[],[]]# Siempre son 6 filas
        self.crear_casilla()
        self.flip = True
        self.faltan_letras = False
        self.noesta = False
        self.timer = 0

    # Funcion que crea el tablero(lista de listas, dentro de las listas hay casillas(Objetos de la clase Casilla, los cuales son los que se imprimen))
    def crear_casilla(self): #[[],[],[],[],[],[]]
        # Se entra a la fila
        for row in range(6): 
            # Se crean las columnas de esa fila, columnas= nivel
            for col in range(self.nivel):
                self.casillas[row].append(Casilla((col * (80 + 10)) + self.MARGIN_X, (row * (80 + 10)) + self.MARGIN_Y))

    
    # Funcion que ejecuta el juego
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    # Funcion que actualiza el contenido de las casillas
    def update(self):
        self.add_letter()

    # Funcion auxiliar de update
    def add_letter(self):
        # limpia cada casilla a vacio
        for casilla in self.casillas[self.fila_actual]:
            casilla.letter = ""

        # agrega las letras a cada casilla
        for i, letter in enumerate(self.text):
            self.casillas[self.fila_actual][i].letter = letter
            self.casillas[self.fila_actual][i].create_font()

    # Funcion que imprime las casillas(con letras incluidas)
    def draw_tiles(self):
        for fila in self.casillas:
            for casilla in fila:
                casilla.draw(self.screen)

    # Funcion que comprueba si faltan letras(se llama en eventos)
    def te_faltan_letras(self):
        #mensaje de faltan letras
            self.faltan_letras = True
            start_pos = self.casillas[0][0].x
            screen_copy = self.screen.copy()
            screen_copy.fill(BGCOLOUR)

            while self.casillas[self.fila_actual][0].x != start_pos:
                self.screen.blit(screen_copy, (0, 0))
                for casilla in self.casillas[self.fila_actual]:
                    casilla.x = start_pos
                    casilla.draw(self.screen)
                pygame.display.flip()
    
    # Funcion que imprime el tablero y tiene animacion en caso de que falten letras
    def draw(self):
        self.screen.fill(BGCOLOUR)
        # Muestra que faltan letras
        if self.faltan_letras:
            self.timer += 1
            self.letters_text.fade_in()
            if self.timer > 40:
                self.faltan_letras = False
                self.timer = 0
        else:
            self.letters_text.fade_out()
        
        # Muestra que no esta en el lemario
        if self.noesta:
            self.timer += 1
            self.letters_text_noesta.fade_in()
            if self.timer > 90:
                self.noesta = False
                self.timer = 0
        else:
            self.letters_text_noesta.fade_out()

        if self.noesta:
            self.letters_text_noesta.draw(self.screen)
        else:
            self.letters_text.draw(self.screen)

        self.draw_tiles()

        pygame.display.flip()

    

    def check_letters(self, ref_diccionario,nivel):
        #print(self.lemario.get(nivel)) # Por si queremos ver el lemario
        for i in range(nivel):
            user_letter = self.text[i] #0 
            colour = LIGHTGREY
        
            if (user_letter in ref_diccionario) and ref_diccionario[user_letter] > 0 :
                
                if user_letter == self.palabra_oculta[i]: 
                    colour = GREEN
                    ref_diccionario[user_letter] -= 1
                

                elif (user_letter in self.palabra_oculta): #and (user_letter not in self.text[i+1:]): #0
                    # print(self.text[i+1:])
                    colour = YELLOW
                    ref_diccionario[user_letter] -= 1

                user_letter = ""
            self.reveal_animation(self.casillas[self.fila_actual][i], colour)    

    
    # Funcion que gestiona los eventos en el juego(escribir o salirse)
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.text) == self.nivel:
                        #Verificar todas las letras y si estan en el lemario
                        if self.text in self.lemario.get(self.nivel):
                            diccionary(self.diccionario,self.palabra_oculta,self.nivel)
                            self.check_letters(self.diccionario,self.nivel)
                        else:
                            self.isnot_animation()
                            self.text = ""
                            continue

                        # Si adivino o agoto los turnos
                        if self.text == self.palabra_oculta or self.fila_actual + 1 == 6:
                            # player lose, lose message is sent
                            if self.text != self.palabra_oculta:
                                self.perdidas +=1
                                self.end_screen_text = UIElement(self.MARGIN_X - 35, 800 - self.MARGIN_Y + 20, f"La palabra era: {self.palabra_oculta}", WHITE)

                            # player win, send win message
                            else:
                                self.ganadas +=1
                                self.end_screen_text = UIElement(self.MARGIN_X - 35,800 - self.MARGIN_Y + 20, "Ganaste - GG", WHITE)
                                

                            # restart the game
                            self.playing = False

                            break
                        else:       
                            self.fila_actual += 1
                            self.text = ""
                    else:
                        # No lleno las letras
                        self.te_faltan_letras()
                        

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < self.nivel and event.unicode.isalpha():
                        self.text += event.unicode.lower()
                        

    # Funcion que imprime al ganar o perder la partida
    def end_screen(self,ganadas,perdidas): 
        play_again = UIElement(self.MARGIN_X - 35, 800 - self.MARGIN_Y + 50, "Enter para volver a jugar", WHITE,28)
        play_again2 = UIElement(self.MARGIN_X - 35, 800 - self.MARGIN_Y + 80, "Flecha <- para volver al menu", WHITE,28)
        contador_text = UIElement(self.MARGIN_X - 20, 50, f"Ganadas: {ganadas} Perdidas: {perdidas} ", WHITE)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_LEFT:
                        self.menu = True 
                        return
                
            self.screen.fill(BGCOLOUR)
            self.draw_tiles()
            contador_text.fade_in()
            contador_text.draw(self.screen)
            self.end_screen_text.fade_in()
            self.end_screen_text.draw(self.screen)
            play_again.fade_in()
            play_again.draw(self.screen)
            play_again2.fade_in()
            play_again2.draw(self.screen)
            pygame.display.flip()
    
    # Funcion para cambiar de menu
    def cambiarmenu(self):
        if self.menu:
            return True

    # ---Animacion
    def isnot_animation(self):
    # Mensaje de que no esta en el lemario
        self.noesta = True
        start_pos = self.casillas[0][0].x
        screen_copy = self.screen.copy()
        screen_copy.fill(BGCOLOUR)

        while self.casillas[self.fila_actual][0].x != start_pos:
            self.screen.blit(screen_copy, (0, 0))
            for casilla in self.casillas[self.fila_actual]:
                casilla.x = start_pos
                casilla.draw(self.screen)
            pygame.display.flip() 

    # ---Animacion
    def reveal_animation(self, casilla, colour):
        # revela por colores
        screen_copy = self.screen.copy()

        while True:
            surface = pygame.Surface((casilla.width + 5, casilla.height + 5))
            surface.fill(BGCOLOUR)
            screen_copy.blit(surface, (casilla.x, casilla.y))
            self.screen.blit(screen_copy, (0, 0))
            if self.flip:
                casilla.y += 6
                casilla.height -= 12
                casilla.font_y += 4
                casilla.font_height = max(casilla.font_height - 8, 0)
            else:
                casilla.colour = colour
                casilla.y -= 6
                casilla.height += 12
                casilla.font_y -= 4
                casilla.font_height = min(casilla.font_height + 8, casilla.font_size)
            if casilla.font_height == 0:
                self.flip = False

            casilla.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)

            if casilla.font_height == casilla.font_size:
                self.flip = True
                break