# constants.py

# Game window dimensions
WIDTH, HEIGHT = 800, 600

# Frame rate (frames per second)
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Scaling factor for sprites
SCALE_FACTOR = 5

# Score settings
ALIEN_POINTS = 25

# Player settings
PLAYER_SPEED = 5

# Bullet settings
BULLET_SPEED = 7
BULLET_WIDTH = 3
BULLET_HEIGHT = 10

# Increase in alien speed
ALIEN_SPEED_INCREASE = 5  # Decrease the delay by 5 frames each reversal

# Alien bullet speed
ALIEN_BULLET_SPEED = 5  # You can adjust this value based on desired game difficulty

# Alien settings
ALIEN_SPEED = 15
ALIEN_MOVE_DOWN = 10

# Alien grid settings
NUM_ROWS = 4  # For four rows of aliens
NUM_COLS = 11  # Adjust if you want a different number of columns
ALIEN_HORIZONTAL_SPACING = 60
ALIEN_VERTICAL_SPACING = 50
TOP_MARGIN = 100
LEFT_MARGIN = 100

# Shield settings
NUM_SHIELDS = 4
SHIELD_INTERVAL = WIDTH // (NUM_SHIELDS + 1)
SHIELD_WIDTH = 5 * SCALE_FACTOR
SHIELD_HEIGHT = 3 * SCALE_FACTOR
