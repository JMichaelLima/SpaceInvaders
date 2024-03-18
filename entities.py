# entities.py
from constants import WIDTH, HEIGHT, PLAYER_SPEED, BULLET_SPEED, BULLET_WIDTH, BULLET_HEIGHT

class Player:
    def __init__(self):
        self.x = WIDTH // 2 - 20
        self.y = HEIGHT - 60
        self.speed = PLAYER_SPEED
        self.lives = 3

class Bullet:
    def __init__(self, x, y, direction, speed, shooter):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for downward (alien), -1 for upward (player)
        self.speed = speed
        self.shooter = shooter
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT

    def update(self):
        """Move the bullet in the specified direction."""
        self.y += self.speed * self.direction

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'alive'  # Possible states: 'alive', 'exploding'
        self.exploding_frame = 0
        self.exploding_timer = 0

class Shield:
    def __init__(self, x, y, layout):
        self.x = x
        self.y = y
        self.layout = layout.copy()  # Make sure to use a copy to avoid altering the original

