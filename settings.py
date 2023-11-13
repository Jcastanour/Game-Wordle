# COLORS (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (200, 200, 0)
BGCOLOUR = DARKGREY

# game settings
col = 8
WIDTH = 120*col
HEIGHT = 800
FPS = 60
title = "Wordle"

TILESIZE = 80
GAPSIZE = 10

MARGIN_X = int((WIDTH - (col * (TILESIZE + GAPSIZE))) / 2)
MARGIN_Y = int((HEIGHT - (6 * (TILESIZE + GAPSIZE))) / 2)
