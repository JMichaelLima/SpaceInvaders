# game_init.py
import pygame
from constants import WIDTH, HEIGHT, FPS

# Initialize Pygame
pygame.init()

# Game window title
WINDOW_TITLE = 'Space Invaders'

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Set up the clock for frame rate control
clock = pygame.time.Clock()
