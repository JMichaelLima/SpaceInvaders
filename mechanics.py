# mechanics.py
import pygame
from constants import WIDTH, HEIGHT, BULLET_WIDTH, BULLET_HEIGHT, ALIEN_POINTS, ALIEN_SPEED_INCREASE, ALIEN_SPEED, SCALE_FACTOR


def update_player_position(player, direction):
    """Update the player's position based on the input direction."""
    player.x += direction * player.speed
    player.x = max(0, min(WIDTH - 30, player.x))


def update_bullets(bullets):
    """Update the positions of all bullets and remove off-screen bullets."""
    for bullet in bullets[:]:
        bullet.update()
        if bullet.y + BULLET_HEIGHT < 0:
            bullets.remove(bullet)


def check_bullet_alien_collisions(bullets, aliens, score):
    for bullet in bullets[:]:
        if bullet.shooter == 'player':  # Only player bullets can hit aliens
            bullet_rect = pygame.Rect(
                bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
            for alien in aliens[:]:
                alien_rect = pygame.Rect(
                    alien.x, alien.y, SCALE_FACTOR * 6, SCALE_FACTOR * 6)
                if bullet_rect.colliderect(alien_rect) and alien.state == 'alive':
                    bullets.remove(bullet)
                    alien.state = 'exploding'
                    alien.exploding_frame = 1
                    score += ALIEN_POINTS  # Update score
                    break
    return score  # Return the updated score

def update_aliens(aliens, alien_direction, alien_speed, alien_move_down, alien_move_base_delay):
    """Update the positions of the aliens, changing direction if necessary, and decrease move delay."""
    alien_edge_reached = False
    for alien in aliens:
        alien.x += alien_direction * alien_speed
        if alien.x <= 0 or alien.x >= WIDTH - SCALE_FACTOR * 6:
            alien_edge_reached = True

    if alien_edge_reached:
        alien_direction *= -1
        # Decrease the base delay to make aliens move faster after each reversal
        alien_move_base_delay = max(10, alien_move_base_delay - ALIEN_SPEED_INCREASE)
        for alien in aliens:
            alien.x += alien_direction * alien_speed
            alien.y += alien_move_down
    return alien_direction, alien_move_base_delay



def check_bullet_shield_collisions(bullets, shields):
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(
            bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        for shield in shields:
            for i, row in enumerate(shield.layout):
                for j, segment in enumerate(row):
                    if segment == 1:
                        segment_rect = pygame.Rect(
                            shield.x + j * SCALE_FACTOR, shield.y + i * SCALE_FACTOR, SCALE_FACTOR, SCALE_FACTOR)
                        if bullet_rect.colliderect(segment_rect):
                            bullets.remove(bullet)
                            # Mark the segment as destroyed
                            shield.layout[i][j] = 0
                            return  # Exit after the first collision to avoid multiple hits per shot


def reset_player(player):
    """
    Reset the player's position and any other necessary state.

    :param player: The player object to reset.
    """
    # Reset player position to the middle bottom of the screen
    player.x = WIDTH // 2 - 20
    player.y = HEIGHT - 60

    # Add any additional state resets here. For example:
    # player.is_invulnerable = True  # If implementing invulnerability after being hit


def check_player_collisions(player, bullets):
    # 8 units wide in the sprite multiplied by the scale factor
    player_width = 8 * SCALE_FACTOR
    # 5 units tall in the sprite multiplied by the scale factor
    player_height = 5 * SCALE_FACTOR

    # Adjust these dimensions to match your player sprite's actual size.
    player_rect = pygame.Rect(player.x, player.y, player_width, player_height)
    for bullet in bullets[:]:
        if bullet.shooter == 'alien':
            bullet_rect = pygame.Rect(
                bullet.x, bullet.y, bullet.width, bullet.height)
            if player_rect.colliderect(bullet_rect):
                bullets.remove(bullet)
                player.lives -= 1
                reset_player(player)
                break
