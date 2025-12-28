import asyncio
import pygame
import random


class Grid(pygame.sprite.Group):
    """The grid in the 2048 game.

    It is a 5x5 grid of Tile sprites."""
    def __init__(self):
        self.grid = [[None for _ in range(5)] for _ in range(5)]
        self.tiles = []
        super().__init__()

    def get_empty_pos(self):
        empty_positions = [(x, y) for y in range(5) for x in range(5) if self.grid[y][x] is None]
        if not empty_positions:
            return None
        return random.choice(empty_positions)


class Tile(pygame.sprite.Sprite):
    """A tile in the 2048 game."""
    def __init__(self, value, position=None):
        super().__init__()
        self.value = value
        self.image = pygame.image.load("./00002.png").convert_alpha()
        self.rect = self.image.get_rect()

        # position is a grid coordinate (col, row)
        col, row = (0, 0) if position is None else position
        self.rect.topleft = (col * RECT_SIZE, row * RECT_SIZE)


    def update(self, position=None):
        """Update the tile's position on the screen."""
        if position is None:
            return
        else:
            if position == "up":
                col, row = (self.rect.x // RECT_SIZE, max(0, self.rect.y // RECT_SIZE - 1))
            elif position == "down":
                col, row = (self.rect.x // RECT_SIZE, min(4, self.rect.y // RECT_SIZE + 1))
            elif position == "left":
                col, row = (max(0, self.rect.x // RECT_SIZE - 1), self.rect.y // RECT_SIZE)
            elif position == "right":
                col, row = (min(4, self.rect.x // RECT_SIZE + 1), self.rect.y // RECT_SIZE)
            self.rect.topleft = (col * RECT_SIZE, row * RECT_SIZE)


def clear_screen():
    """Clear the screen and draw the grid lines."""
    screen.fill("#414558")
    pygame.draw.rect(screen, border_color, (0, 0, WIDTH, HEIGHT), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, RECT_SIZE, HEIGHT), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, 2 * RECT_SIZE, HEIGHT), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, 3 * RECT_SIZE, HEIGHT), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, 4 * RECT_SIZE, HEIGHT), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, WIDTH, RECT_SIZE), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, WIDTH, 2 * RECT_SIZE), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, WIDTH, 3 * RECT_SIZE), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, WIDTH, 4 * RECT_SIZE), border_width)

# pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 600
RECT_SIZE = 600 / 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

border_color = (255, 255, 255)
border_width = 5

clock = pygame.time.Clock()
running = True

default_tiles = {
    "two": "./00002.png",
    "four": "./twofortyeight/assets/00004.png",
    "eight": "./twofortyeight/assets/00008.png",
    "sixteen": "./twofortyeight/assets/00016.png",
    # "thirty_two": "./twofortyeight/assets/00032.png",
    # "sixty_four": "./twofortyeight/assets/00064.png",
    # "one_twenty_eight": "./twofortyeight/assets/00128.png",
    # "two_fifty_six": "./twofortyeight/assets/00256.png",
    # "five_twelve": "./twofortyeight/assets/00512.png",
    # "one_zero_two_four": "./twofortyeight/assets/01024.png",
    # "two_zero_four_eight": "./twofortyeight/assets/02048.png",
}

grid = Grid()
while running:
    # fill the screen with a color to wipe away anything from last frame
    clear_screen()
    grid.draw(screen)
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Spawn a new tile at a random position in the grid
            # If no empty positions are available, the game is over
            new_pos = grid.get_empty_pos()
            if new_pos is None:
                print("Game Over!")
                running = False
            else:
                grid.add(Tile("two", new_pos))
                grid.tiles.append(grid.sprites()[-1])
            screen.blit(grid.tiles[-1].image, (grid.tiles[-1].rect.x, grid.tiles[-1].rect.y))
            if event.key == pygame.K_UP:
                grid.update(position="up")
            elif event.key == pygame.K_DOWN:
                grid.update(position="down")
            elif event.key == pygame.K_LEFT:
                grid.update(position="left")
            elif event.key == pygame.K_RIGHT:
                grid.update(position="right")

    # flip() the display to put your work on screen
    pygame.display.flip()

    # This is for PyScript compatibility
    await asyncio.sleep(1 / 60)
    #clock.tick(60)

pygame.quit()
