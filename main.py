import random

import pygame
from settings import *
from sprites import *

def diccionary(diccionario,palabra_oculta,nivel):
    for i in range(nivel):
        diccionario[palabra_oculta[i]] = 0
        
    for i in range(nivel):
        if palabra_oculta[i] in diccionario:
            diccionario[palabra_oculta[i]] +=1
        else:
            diccionario[palabra_oculta[i]] = 1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.lemario = {longitud: set() for longitud in range(4,9)} # Creamos un diccionario con la longitud de cada palabra, su valor
        self.create_word_list()
        self.letters_text = UIElement(100, 70, "Not Enough Letters", WHITE)
                
        
    def create_word_list(self):
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

    def new(self,nivel):
        # Filtramos de acuerdo a la Clave de cada diccionario(Clave = len(palabra))
        # lemario_dif_4 = self.lemario.get(4)
        # lemario_dif_5 = self.lemario.get(5)
        # lemario_dif_6 = self.lemario.get(6)
        # lemario_dif_7 = self.lemario.get(7)
        # lemario_dif_8 = self.lemario.get(8)
        # if nivel == 4:
        #   self.palabra_oculta = random.sample(self.lemario.get(nivel),1)[0].lower()
        # if nivel == 5:
        #     self.palabra_oculta = random.sample(self.lemario.get(nivel),1)[0].lower()
        # if nivel == 6:
        #     self.palabra_oculta = random.sample(self.lemario.get(nivel),1)[0].lower()
        # if nivel == 7:
        #     self.palabra_oculta = random.sample(self.lemario.get(nivel),1)[0].lower()
        # if nivel == 8:
        #     self.palabra_oculta = random.sample(self.lemario.get(nivel),1)[0].lower()
        
        self.palabra_oculta = random.sample(self.lemario.get(nivel),1)[0].lower()
        self.nivel = nivel
        self.diccionario = dict()
        diccionary(self.diccionario,self.palabra_oculta,nivel)

        # for i in self.palabra_oculta:
        #     if i in self.diccionario:
        #         self.diccionario[i] +=1
        #     else:
        #         self.diccionario[i] = 1

        #print(self.diccionario)

        #print(self.palabra_oculta)
        self.text = ""
        self.current_row = 0
        self.tiles = []
        self.create_tiles()
        self.flip = True
        self.not_enough_letters = False
        self.isgood = False
        self.timer = 0

    def create_tiles(self):
        for row in range(6):
            self.tiles.append([])
            for col in range(8):
                self.tiles[row].append(Tile((col * (TILESIZE + GAPSIZE)) + MARGIN_X, (row * (TILESIZE + GAPSIZE)) + MARGIN_Y))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            
            self.update()
            self.draw()

    def update(self):
        self.add_letter()

    def add_letter(self):
        # empty all the letter in the current row
        for tile in self.tiles[self.current_row]:
            tile.letter = ""

        # add the letters typed to the current row
        for i, letter in enumerate(self.text):
            self.tiles[self.current_row][i].letter = letter
            self.tiles[self.current_row][i].create_font()

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)

    def draw(self):
        self.screen.fill(BGCOLOUR)
        # display the not enough letters text
        if self.not_enough_letters:
            self.timer += 1
            self.letters_text.fade_in()
            if self.timer > 90:
                self.not_enough_letters = False
                self.timer = 0
        else:
            self.letters_text.fade_out()
        self.letters_text.draw(self.screen)

        self.draw_tiles()

        pygame.display.flip()

    def row_animation(self):
        # row shaking if not enough letters is inputted
        self.not_enough_letters = True
        start_pos = self.tiles[0][0].x
        amount_move = 4
        move = 3
        screen_copy = self.screen.copy()
        screen_copy.fill(BGCOLOUR)
        for row in self.tiles:
            for tile in row:
                if row != self.tiles[self.current_row]:
                    tile.draw(screen_copy)

    def rowbad_animation(self):
        # row shaking if not enough letters is inputted
        self.not_enough_letters = True
        start_pos = self.tiles[0][0].x
        amount_move = 4
        move = 3
        screen_copy = self.screen.copy()
        screen_copy.fill(BGCOLOUR)
        for row in self.tiles:
            for tile in row:
                if row != self.tiles[self.current_row]:
                    tile.draw(screen_copy)                

        while True:
            while self.tiles[self.current_row][0].x < start_pos + amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    #tile.x += move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            while self.tiles[self.current_row][0].x > start_pos - amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x -= move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            amount_move -= 2
            if amount_move < 0:
                break

    def box_animation(self):
        # tile scale animation for every letter inserted
        for tile in self.tiles[self.current_row]:
            if tile.letter == "":
                screen_copy = self.screen.copy()
                for start, end, step in ((0, 6, 1), (0, -6, -1)):
                    for size in range(start, end, 2*step):
                        self.screen.blit(screen_copy, (0, 0))
                        tile.x -= size
                        tile.y -= size
                        tile.width += size * 2
                        tile.height += size * 2
                        surface = pygame.Surface((tile.width, tile.height))
                        surface.fill(BGCOLOUR)
                        self.screen.blit(surface, (tile.x, tile.y))
                        tile.draw(self.screen)
                        pygame.display.flip()
                        self.clock.tick(FPS)
                    self.add_letter()
                break

    def reveal_animation(self, tile, colour):
        # reveal colours animation when user input the whole word
        screen_copy = self.screen.copy()

        while True:
            surface = pygame.Surface((tile.width + 5, tile.height + 5))
            surface.fill(BGCOLOUR)
            screen_copy.blit(surface, (tile.x, tile.y))
            self.screen.blit(screen_copy, (0, 0))
            if self.flip:
                tile.y += 6
                tile.height -= 12
                tile.font_y += 4
                tile.font_height = max(tile.font_height - 8, 0)
            else:
                tile.colour = colour
                tile.y -= 6
                tile.height += 12
                tile.font_y -= 4
                tile.font_height = min(tile.font_height + 8, tile.font_size)
            if tile.font_height == 0:
                self.flip = False

            tile.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

            if tile.font_height == tile.font_size:
                self.flip = True
                break
    

    def check_letters(self, ref_diccionario,nivel):

        for i in range(nivel):
            # print(ref_diccionario)
            ##print(self.text)
            user_letter = self.text[i] #0
            colour = LIGHTGREY
            #print(self.palabra_oculta)
        
            if (user_letter in ref_diccionario) and ref_diccionario[user_letter] > 0 :
                
                if user_letter == self.palabra_oculta[i]: #0
                    colour = GREEN
                    ref_diccionario[user_letter] -= 1
                elif (user_letter in self.palabra_oculta) and (user_letter not in self.text[i+1:]): #0
                    # print(self.text[i+1:])
                    colour = YELLOW
                    ref_diccionario[user_letter] -= 1

                
                user_letter = ""
            self.reveal_animation(self.tiles[self.current_row][i], colour)    

        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.text) == self.nivel:
                        # check all letters
                        diccionary(self.diccionario,self.palabra_oculta,self.nivel)
                        
                        if self.text not in self.lemario.get(self.nivel):
                            print("no puede")
                            self.rowbad_animation()
                            

                        else:
                            self.check_letters(self.diccionario,self.nivel)


                        # if the text is correct or the player has used all his turns
                        if self.text == self.palabra_oculta or self.current_row + 1 == 6:
                            # player lose, lose message is sent
                            if self.text != self.palabra_oculta:
                                self.end_screen_text = UIElement(100, 700, f"THE WORD WAS: {self.palabra_oculta}", WHITE)

                            # player win, send win message
                            else:
                                self.end_screen_text = UIElement(100, 700, "YOU GUESSED RIGHT", WHITE)

                            # restart the game
                            self.playing = False
                            self.end_screen()
                            break

                        self.current_row += 1
                        self.text = ""
                    else:
                        # row animation, not enough letters message
                        self.row_animation()
                        

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 5 and event.unicode.isalpha():
                        self.text += event.unicode.lower()
                        self.box_animation()
                        

    def end_screen(self):
        play_again = UIElement(85, 750, "PRESS ENTER TO PLAY AGAIN", WHITE, 30)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

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


game = Game()
while True:
    game.new(5)
    game.run()
