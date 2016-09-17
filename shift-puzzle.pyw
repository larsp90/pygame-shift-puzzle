import sys
import random
import pygame

IMAGE_FILE = "dduck800_600.jpg" 
IMAGE_SIZE = (800, 600)
TILE_WIDTH = 200
TILE_HEIGHT = 200
COLUMNS = 4
ROWS = 3

# bottom right corner contains no tile
EMPTY_TILE = (COLUMNS-1, ROWS-1)   

BLACK = (0, 0, 0)

# horizontal and vertical borders for tiles
hor_border = pygame.Surface((TILE_WIDTH, 1))
hor_border.fill(BLACK)
ver_border = pygame.Surface((1, TILE_HEIGHT))
ver_border.fill(BLACK)

# load the image and divide up in tiles
# putting borders on each tile also adds them to the full image
image = pygame.image.load(IMAGE_FILE)
tiles = {}
for c in range(COLUMNS) :
    for r in range(ROWS) :
        tile = image.subsurface (
            c*TILE_WIDTH, r*TILE_HEIGHT, 
            TILE_WIDTH, TILE_HEIGHT)
        tiles [(c, r)] = tile
        if (c, r) != EMPTY_TILE:
            tile.blit(hor_border, (0, 0))
            tile.blit(hor_border, (0, TILE_HEIGHT-1))
            tile.blit(ver_border, (0, 0))
            tile.blit(ver_border, (TILE_WIDTH-1, 0))
            # make the corners a bit rounded
            tile.set_at((1, 1), BLACK)
            tile.set_at((1, TILE_HEIGHT-2), BLACK)
            tile.set_at((TILE_WIDTH-2, 1), BLACK)
            tile.set_at((TILE_WIDTH-2, TILE_HEIGHT-2), BLACK)
tiles[EMPTY_TILE].fill(BLACK)

# keep track of which tile is in which position
state = {(col, row): (col, row) 
            for col in range(COLUMNS) for row in range(ROWS)}

# keep track of the position of the empty tyle
(emptyc, emptyr) = EMPTY_TILE

# start game and display the completed puzzle
pygame.init()
display = pygame.display.set_mode(IMAGE_SIZE)
pygame.display.set_caption("shift-puzzle")
display.blit (image, (0, 0))
pygame.display.flip()

# swap a tile (c, r) with the neighbouring (emptyc, emptyr) tile
def shift (c, r) :
    global emptyc, emptyr 
    display.blit(
        tiles[state[(c, r)]],
        (emptyc*TILE_WIDTH, emptyr*TILE_HEIGHT))
    display.blit(
        tiles[EMPTY_TILE],
        (c*TILE_WIDTH, r*TILE_HEIGHT))
    state[(emptyc, emptyr)] = state[(c, r)]
    state[(c, r)] = EMPTY_TILE
    (emptyc, emptyr) = (c, r)
    pygame.display.flip()

# shuffle the puzzle by making some random shift moves
def shuffle() :
    global emptyc, emptyr
    # keep track of last shuffling direction to avoid "undo" shuffle moves
    last_r = 0 
    for i in range(75):
        # slow down shuffling for visual effect
        pygame.time.delay(50)
        while True:
            # pick a random direction and make a shuffling move
            # if that is possible in that direction
            r = random.randint(1, 4)
            if (last_r + r == 5):
                # don't undo the last shuffling move
                continue
            if r == 1 and (emptyc > 0):
                shift(emptyc - 1, emptyr) # shift left
            elif r == 4 and (emptyc < COLUMNS - 1):
                shift(emptyc + 1, emptyr) # shift right
            elif r == 2 and (emptyr > 0):
                shift(emptyc, emptyr - 1) # shift up
            elif r == 3 and (emptyr < ROWS - 1):
                shift(emptyc, emptyr + 1) # shift down
            else:
                # the random shuffle move didn't fit in that direction  
                continue
            last_r=r
            break # a shuffling move was made

# process mouse clicks 
at_start = True
showing_solution = False
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN :
        if at_start:
            # shuffle after the first mouse click
            shuffle()
            at_start = False
        elif event.dict['button'] == 1:
            # mouse left button: move if next to the empty tile
            mouse_pos = pygame.mouse.get_pos()
            c = mouse_pos[0] / TILE_WIDTH
            r = mouse_pos[1] / TILE_HEIGHT
            if (    (abs(c-emptyc) == 1 and r == emptyr) or  
                    (abs(r-emptyr) == 1 and c == emptyc)):
                shift (c, r)
        elif event.dict['button'] == 3:
            # mouse right button: show solution image
            saved_image = display.copy()
            display.blit(image, (0, 0))
            pygame.display.flip()
            showing_solution = True
    elif showing_solution and (event.type == pygame.MOUSEBUTTONUP):
        # stop showing the solution
        display.blit (saved_image, (0, 0))
        pygame.display.flip()
        showing_solution = False

