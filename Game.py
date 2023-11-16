import random
import pygame
from settings import *
import sys
from collections import deque

ganadas = 0
perdidas = 0

# JUEGO - GAME
def diccionary(diccionario,palabra_oculta,nivel): #o(1)
    for i in range(nivel):
        diccionario[palabra_oculta[i]] = 0
        
    for i in range(nivel):
        if palabra_oculta[i] in diccionario:
            diccionario[palabra_oculta[i]] +=1
        else:
            diccionario[palabra_oculta[i]] = 1

class Game:
    def __init__(self,nivel):
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
        self.lemario = {longitud: set() for longitud in range(4,9)} # Creamos un diccionario con la longitud de cada palabra, su valor
        self.crea_lista_palabras()
        self.letters_text = UIElement(self.MARGIN_X, 70, "pai te faltan letras", WHITE)
        self.letters_text_noesta = UIElement(self.MARGIN_X, 70, "No esta en el lemario", WHITE)
        self.ganadas = 0
                
        
    def crea_lista_palabras(self):
        #Abrimos el txt y añadimos a cada clave en el diccionario una palabra a su valor(set)
        with open ('palabras.txt','r',encoding='utf-8') as file:
            for linea in file:
                palabra = ' '.join(linea.split()).rstrip().strip("-") 
                longitud = len(palabra)
        
                if longitud == 4:
                    self.lemario[4].add(palabra)  
                if longitud == 5:
                    self.lemario[5].add(palabra)    
                if longitud == 6:
                    self.lemario[6].add(palabra) 
                if longitud == 7:
                    self.lemario[7].add(palabra) 
                if longitud == 8:
                    self.lemario[8].add(palabra) 

    def nuevo(self):
        
        self.palabra_oculta = random.sample(self.lemario.get(self.nivel),1)[0].lower() #o(1)

        self.diccionario = dict()
        diccionary(self.diccionario,self.palabra_oculta,self.nivel) #o(1)

        print(self.palabra_oculta)
        self.text = ""
        self.fila_actual = 0
        self.casillas = deque([[],[],[],[],[],[]]) # siempre 6, 6 filas
        self.crear_casilla()
        self.flip = True
        self.faltan_letras = False
        self.noesta = False
        self.timer = 0

    def crear_casilla(self): #[[],[],[],[],[],[]]
        for row in range(6): #siempre 6 veces,6 filas
            #self.casillas.append([])
            for col in range(self.nivel): #siempre el nivel, las columnas
                self.casillas[row].append(Casilla((col * (80 + 10)) + self.MARGIN_X, (row * (80 + 10)) + self.MARGIN_Y))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()


    def update(self):
        self.add_letter()

    def add_letter(self):
        # empty all the letter in the current fila
        for casilla in self.casillas[self.fila_actual]:
            casilla.letter = ""

        # add the letters typed to the current fila
        for i, letter in enumerate(self.text):
            self.casillas[self.fila_actual][i].letter = letter
            self.casillas[self.fila_actual][i].create_font()

    def draw_tiles(self):
        for fila in self.casillas:
            for casilla in fila:
                casilla.draw(self.screen)

    def draw(self):
        self.screen.fill(BGCOLOUR)
        # display the not enough letters text
        if self.faltan_letras:
            self.timer += 1
            self.letters_text.fade_in()
            if self.timer > 90:
                self.faltan_letras = False
                self.timer = 0
        else:
            self.letters_text.fade_out()

        if self.noesta:
            self.timer += 1
            self.letters_text_noesta.fade_in()
            if self.timer > 90:
                self.noesta = False
                self.timer = 0
        else:
            pass
            self.letters_text_noesta.fade_out()

        if self.noesta:
            self.letters_text_noesta.draw(self.screen)
        else:
            self.letters_text.draw(self.screen)

        self.draw_tiles()

        pygame.display.flip()

    def row_animation(self):
        # row shaking if not enough letters is inputted
        self.faltan_letras = True
        start_pos = self.casillas[0][0].x
        amount_move = 4
        move = 3
        screen_copy = self.screen.copy()
        screen_copy.fill(BGCOLOUR)
        for fila in self.casillas:
            for casilla in fila:
                if fila != self.casillas[self.fila_actual]:
                    casilla.draw(screen_copy)
        while True:
            while self.casillas[self.fila_actual][0].x < start_pos + amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for casilla in self.casillas[self.fila_actual]:
                    casilla.x += move
                    casilla.draw(self.screen)
                self.clock.tick(60)
                pygame.display.flip()

            while self.casillas[self.fila_actual][0].x > start_pos - amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for casilla in self.casillas[self.fila_actual]:
                    casilla.x -= move
                    casilla.draw(self.screen)
                self.clock.tick(60)
                pygame.display.flip()

            amount_move -= 2
            if amount_move < 0:
                break

    def draw_isnot(self):
        self.screen.fill(BGCOLOUR)
        # La palabra no esta en el lemario
        if self.noesta:
            self.timer += 1
            self.letters_text_noesta.fade_in()
            if self.timer > 90:
                self.noesta = False
                self.timer = 0
        else:
            self.letters_text_noesta.fade_out()
        self.letters_text_noesta.draw(self.screen)
        self.draw_tiles()
        pygame.display.flip()

    def isnot_animation(self):
        # Animacion de que no esta en el lemario
        self.noesta = True
        
        start_pos = self.casillas[0][0].x
        amount_move = 4
        move = 3
        screen_copy = self.screen.copy()
        screen_copy.fill(BGCOLOUR)
        for fila in self.casillas:
            for casilla in fila:
                if fila != self.casillas[self.fila_actual]:
                    casilla.draw(screen_copy)
        while True:
            while self.casillas[self.fila_actual][0].x < start_pos + amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for casilla in self.casillas[self.fila_actual]:
                    casilla.x += move
                    casilla.draw(self.screen)
                self.clock.tick(60)
                pygame.display.flip()

            while self.casillas[self.fila_actual][0].x > start_pos - amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for casilla in self.casillas[self.fila_actual]:
                    casilla.x -= move
                    casilla.draw(self.screen)
                self.clock.tick(60)
                pygame.display.flip()

            amount_move -= 2
            if amount_move < 0:
                break

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
    

    def check_letters(self, ref_diccionario,nivel):
        for i in range(nivel):
            #print(ref_diccionario)
            #print(self.lemario.get(8))
            user_letter = self.text[i] #0 
            #print(user_letter)
            colour = LIGHTGREY
            print(self.palabra_oculta)
        
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
                            print("no puede")
                            self.text = ""
                            continue

                        # Si adivino o agoto los turnos
                        if self.text == self.palabra_oculta or self.fila_actual + 1 == 6:
                            # player lose, lose message is sent
                            if self.text != self.palabra_oculta:
                                self.end_screen_text = UIElement(self.MARGIN_X - 20, 700, f"La palabra era: {self.palabra_oculta}", WHITE)
                                self.perdidas +=1

                            # player win, send win message
                            else:
                                self.end_screen_text = UIElement(self.MARGIN_X - 20, 700, "Ganaste", WHITE)
                                self.ganadas +=1

                            # restart the game
                            self.playing = False
                            
                            self.end_screen()
                            break
                        else:       
                            self.fila_actual += 1
                            self.text = ""
                    else:
                        # animacion de no hay letras
                        self.row_animation()
                        

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < self.nivel and event.unicode.isalpha():
                        self.text += event.unicode.lower()
                        #self.box_animation()
                        

    def end_screen(self):
        play_again = UIElement(self.MARGIN_X - 20, 750, "Enter para volver a jugar", WHITE, 30)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.fill(BGCOLOUR)
            self.draw_tiles()
            self.end_screen_text.fade_in()
            self.end_screen_text.draw(self.screen)
            play_again.fade_in()
            play_again.draw(self.screen)
            pygame.display.flip()



