import pygame
import sys
import random
import time
import sprites
from sprite_renderer import render_sprite, render_shield, render_sprite_to_surface
from copy import deepcopy
from sprites import shield as shield_layout
from game_init import window, clock, FPS
from constants import (WIDTH, HEIGHT, BLACK, WHITE, SCALE_FACTOR, ALIEN_BULLET_SPEED, 
                       BULLET_HEIGHT, BULLET_WIDTH, ALIEN_HORIZONTAL_SPACING, 
                       ALIEN_VERTICAL_SPACING, ALIEN_SPEED, ALIEN_MOVE_DOWN, TOP_MARGIN, 
                       LEFT_MARGIN, NUM_ROWS, NUM_COLS, BULLET_SPEED, NUM_SHIELDS)
from entities import Player, Bullet, Alien, Shield
from mechanics import update_player_position, update_bullets, check_bullet_alien_collisions, update_aliens, check_bullet_shield_collisions, check_player_collisions

def render_lives(screen, player, player_sprite_data, margin=10):
    player_sprite_surface = render_sprite_to_surface(player_sprite_data)
    ship_width = player_sprite_surface.get_width()  # Get the width of the ship

    # Render each life with a margin
    for i in range(player.lives - 1):  # Subtract one to not count the active life
        x_position = 10 + i * (ship_width + margin)  # Calculate x position with margin
        screen.blit(player_sprite_surface, (x_position, HEIGHT - 30))

def display_game_over(screen):
    game_over_font = pygame.font.SysFont("Arial", 48)
    game_over_surface = game_over_font.render("Game Over! Press Space to Restart", True, WHITE)
    screen.blit(game_over_surface, ((WIDTH - game_over_surface.get_width()) // 2, (HEIGHT - game_over_surface.get_height()) // 2))
    pygame.display.flip()

def wait_for_spacebar():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def render_score(screen, score, x, y, scale=SCALE_FACTOR):
    score_str = str(score)
    digit_sprites = [sprites.digit_0, sprites.digit_1, sprites.digit_2, sprites.digit_3, 
                     sprites.digit_4, sprites.digit_5, sprites.digit_6, sprites.digit_7, 
                     sprites.digit_8, sprites.digit_9]
    for i, digit in enumerate(score_str):
        digit_sprite = digit_sprites[int(digit)]
        render_sprite(screen, digit_sprite, x + (i * 8 * scale), y, scale)

# Initialize game entities and settings
score = 0
player = Player()
bullets = []
aliens = [Alien(LEFT_MARGIN + x * ALIEN_HORIZONTAL_SPACING, TOP_MARGIN + y * ALIEN_VERTICAL_SPACING) 
          for y in range(NUM_ROWS) for x in range(NUM_COLS)]
shields = [Shield(x, HEIGHT - 150, deepcopy(shield_layout)) 
           for x in [(i + 1) * WIDTH // (NUM_SHIELDS + 1) - SCALE_FACTOR * len(shield_layout[0]) // 2 
                     for i in range(NUM_SHIELDS)]]
alien_move_base_delay = FPS
alien_move_timer = 0
alien_direction = 1

# Initialize alien firing variables
last_alien_fire_time = time.time()
alien_fire_delay = random.randint(1, 3)

# Define alien animation states and toggle delay
states = [sprites.invader_state_1, sprites.invader_state_2, sprites.invader_state_3, sprites.invader_state_4]
state_index = 0
toggle_delay = 30  # Speed of state changes for alien animation
frame_counter = 0

# Main game loop
running = True
while running:
    if player.lives > 0:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x + 20, player.y, -1, BULLET_SPEED, 'player'))

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            update_player_position(player, -1)
        if keys[pygame.K_RIGHT]:
            update_player_position(player, 1)

        if aliens:  # Check if there are any aliens left
            max_alien_y = max(alien.y for alien in aliens)
            descent_factor = (max_alien_y - TOP_MARGIN) / (HEIGHT - TOP_MARGIN - ALIEN_MOVE_DOWN)
            alien_move_delay = max(1, alien_move_base_delay * (1 - descent_factor) * len(aliens) / (NUM_ROWS * NUM_COLS))
        else:
            alien_move_delay = float('inf')  # Set delay to infinity if no aliens left

        # Alien movement and behavior
        alien_move_timer += 1
        if alien_move_timer >= alien_move_delay:
            alien_move_timer = 0
            alien_direction, alien_move_base_delay = update_aliens(aliens, alien_direction, ALIEN_SPEED, ALIEN_MOVE_DOWN, alien_move_base_delay)

        # Alien firing mechanism
        current_time = time.time()
        if current_time - last_alien_fire_time > alien_fire_delay and aliens:
            firing_alien = random.choice(aliens)
            if firing_alien.state == 'alive':
                bullets.append(Bullet(firing_alien.x + SCALE_FACTOR * 3, firing_alien.y, 1, ALIEN_BULLET_SPEED, 'alien'))
                last_alien_fire_time = current_time
                alien_fire_delay = random.randint(1, 3)

        # Update and check collisions
        update_bullets(bullets)
        score = check_bullet_alien_collisions(bullets, aliens, score)
        check_bullet_shield_collisions(bullets, shields)
        check_player_collisions(player, bullets)

        # Render game state
        window.fill(BLACK)
        render_sprite(window, sprites.player_ship, player.x, player.y, SCALE_FACTOR)
        for bullet in bullets:
            pygame.draw.rect(window, WHITE, (bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT))

        # Alien animation and rendering
        frame_counter += 1
        if frame_counter >= toggle_delay:
            state_index = (state_index + 1) % len(states)
            frame_counter = 0

        for alien in aliens:
            if alien.state == 'alive':
                render_sprite(window, states[state_index], alien.x, alien.y, SCALE_FACTOR)
            elif alien.state == 'exploding':
                # Select and render exploding sprite
                exploding_sprite = getattr(sprites, f'invader_exploding_{alien.exploding_frame}')
                render_sprite(window, exploding_sprite, alien.x, alien.y, SCALE_FACTOR)
                alien.exploding_timer += 1
                if alien.exploding_timer % 10 == 0:
                    alien.exploding_frame += 1
                if alien.exploding_frame > 3:
                    aliens.remove(alien)

        for shield in shields:
            render_shield(window, shield)

        render_lives(window, player, sprites.player_ship, 15)
        render_score(window, score, WIDTH - 250, 10)

    else:
        # Game Over Logic
        display_game_over(window)
        wait_for_spacebar()

        # Reset Game State
        player.lives = 3
        player.x = WIDTH // 2 - 20
        bullets.clear()
        aliens.clear()
        aliens = [Alien(LEFT_MARGIN + x * ALIEN_HORIZONTAL_SPACING, TOP_MARGIN + y * ALIEN_VERTICAL_SPACING)
                  for y in range(NUM_ROWS) for x in range(NUM_COLS)]
        shields = [Shield(x, HEIGHT - 150, deepcopy(shield_layout))
                   for x in [(i + 1) * WIDTH // (NUM_SHIELDS + 1) - SCALE_FACTOR * len(shield_layout[0]) // 2 
                             for i in range(NUM_SHIELDS)]]
        last_alien_fire_time = time.time()
        alien_move_base_delay = FPS
        score = 0

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

       
