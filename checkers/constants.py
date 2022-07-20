import pygame
import os

WIDTH, HEIGHT = 720, 720
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

'''
My board will be green and cream with red and white 
'''
WOODEN_YELLOW = (236, 213, 167)
GREEN_LIGHT = (9, 97, 73)
WHITE_MARBLE = (240, 235, 215)
RED_RUBY = (155, 17, 30)
BLUE_GREEN = (10, 122, 149)
BLACK_SOFT = (14, 17, 17)
CROWN = pygame.transform.scale(pygame.image.load(os.path.join(
    "assets", 'crown.png')), (SQUARE_SIZE//2, SQUARE_SIZE//4))
