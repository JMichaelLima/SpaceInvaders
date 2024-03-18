# sprite_renderer.py
import pygame
from constants import WHITE, SCALE_FACTOR, BLACK, HEIGHT

def render_sprite(screen, sprite, x, y, scale=SCALE_FACTOR):
    """Render a sprite at the specified location."""
    for i, row in enumerate(sprite):
        for j, pixel in enumerate(row):
            if pixel:
                pygame.draw.rect(screen, WHITE, (x + j * scale, y + i * scale, scale, scale))

# sprite_renderer.py
def render_shield(screen, shield):
    for i, row in enumerate(shield.layout):
        for j, segment in enumerate(row):
            if segment == 1:
                pygame.draw.rect(screen, WHITE, (shield.x + j * SCALE_FACTOR, shield.y + i * SCALE_FACTOR, SCALE_FACTOR, SCALE_FACTOR))

def render_sprite_to_surface(sprite, scale=SCALE_FACTOR*.8):
    """Convert sprite data to a pygame.Surface."""
    sprite_height = len(sprite)
    sprite_width = len(sprite[0])
    surface = pygame.Surface((sprite_width * scale, sprite_height * scale), pygame.SRCALPHA)
    surface.set_colorkey(BLACK)
    for y, row in enumerate(sprite):
        for x, pixel in enumerate(row):
            if pixel:
                pygame.draw.rect(surface, WHITE, (x * scale, y * scale, scale, scale))
    return surface



