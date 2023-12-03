import pygame
import sys
import numpy as np
from copy import deepcopy
from random import randint
from tkinter import Tk, filedialog  # Import tkinter modules

def createArray(widthSquares, heightSquares):
    return [[random.randint(0, 1) for _ in range(widthSquares)] for _ in range(heightSquares)]

def countNeigbors(array, counts, x, y):
    count = 0
    for l in [y-1, y, y+1]:
        for o in [x-1, x, x+1]:
            count+=array[l][o]
    count -= array[y][x]
    counts[y][x] = count
    #print(array[y][x], count)
    #count = sum(array[y-1:y+1][x-1:x+2])
    return counts

def gameOfLifeRules(array, counts, x, y, ):
    gamed = deepcopy(array)
    count = counts[y][x]
    #print(f'Before {array[y][x]}, count {count}')
    if array[y][x] == 0 and count == 3:
        gamed[y][x] = 1
        #print("reproduction")
        #print(array[y][x], count, gamed[y][x])
    elif array[y][x] == 1 and (count == 2 or count == 3):
        gamed[y][x] = 1
        #print("next gen")
        #print(array[y][x], count, gamed[y][x])
    elif array[y][x] == 1 and count > 3:
        gamed[y][x] = 0
        #print('over-pop')
        #print(array[y][x], count, gamed[y][x])
    elif array[y][x] == 1 and count < 2:
        gamed[y][x] = 0
        #print('under-pop')
        #print(array[y][x], count, gamed[y][x])
    return gamed

def saveNpyArray(array):
    np.save("test.npy", array)

def loadNpyArray(array):
    filename = 'test.npy'
    try:
        loaded_array = np.load(filename)
        if loaded_array.shape == array.shape:  # Ensure shapes match before updating
            array[:] = loaded_array  # Update the array
    except Exception as e:
        print("Error loading file:", e)


# Initialize Pygame
pygame.init()
# Define Button class
class Button:
    def __init__(self, x, y, width, height, color, text, function=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.function = function

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

squareSize = 10
widthSquares = 60
heightSquares = 40
pannelHeight = 60
width, height = widthSquares*squareSize, heightSquares*squareSize + pannelHeight

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")


# Define colors (RGB format)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (127,127,127)
orange = (255,100,10)

# Create a pause button
button_width, button_height = 100, 50
pause_button = Button((width-button_width)//2, height-pannelHeight+(pannelHeight-button_height)//2, button_width, button_height, green, "Pause")
resume_button = Button((width-button_width)//2, height-pannelHeight+(pannelHeight-button_height)//2, button_width, button_height, blue, "resume")
save_button = Button((width//2-button_width)//2, height-pannelHeight+(pannelHeight-button_height)//2, button_width, button_height, green, "Save", saveNpyArray)
load_button = Button((3*width//2-button_width)//2, height-pannelHeight+(pannelHeight-button_height)//2, button_width, button_height, green, "load", loadNpyArray)


array = np.zeros((heightSquares, widthSquares))
# Main loop
running = True
paused = True
clock = pygame.time.Clock()
while running:
    save_button.draw(screen)
    screen.fill(gray)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            square_x = mouse_x // squareSize
            square_y = mouse_y // squareSize
            if 1 <= square_x < array.shape[1]-1 and 1 <= square_y < array.shape[0]-1:
                array[square_y][square_x] = 1 - array[square_y][square_x]
            if pause_button.is_clicked(mouse_pos):
                paused = not paused 
            elif resume_button.is_clicked(mouse_pos):
                paused = not paused
            elif save_button.is_clicked(mouse_pos):
                if save_button.function:
                    save_button.function(array)
            elif load_button.is_clicked(mouse_pos):
                if load_button.function:
                    load_button.function(array)
    if paused:
        save_button.draw(screen)
        load_button.draw(screen)
        resume_button.draw(screen)
        #print("paused")
        for y, row in enumerate(array[1:-1]):
            for x, value in enumerate(row[1:-1]):
                color = orange if value == 1 else black
                pygame.draw.rect(screen, color, ((x+1) * squareSize, (y+1) * squareSize, squareSize, squareSize))
    else:
        #print("not paused")
        save_button.draw(screen)
        load_button.draw(screen)
        pause_button.draw(screen)
        counts = np.zeros((heightSquares, widthSquares))
        for y, row in enumerate(array[1:-1]):
            for x, value in enumerate(row[1:-1]):
                counts = countNeigbors(array, counts, x, y)
        for y, row in enumerate(array[1:-1]):
            for x, value in enumerate(row[1:-1]):
                array = gameOfLifeRules(array, counts, x, y)
                color = orange if value == 1 else black
                pygame.draw.rect(screen, color, ((x+1) * squareSize, (y+1) * squareSize, squareSize, squareSize))
        #running = False
    pygame.display.flip()
    clock.tick(60)
    pygame.time.delay(100)

pygame.quit()
sys.exit()