import asyncio
import pygame
import random
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Grid(pygame.sprite.Group):
    """The grid in the 2048 game.

    It is a nxn grid of Tile sprites."""
    def __init__(self, n=5):
        self.grid = [[None for _ in range(n)] for _ in range(n)]
        self.tiles = []
        self.n = n
        super().__init__()

    def get_empty_pos(self):
        """Get a random empty position in the grid."""
        empty_positions = [(x, y) for y in range(self.n) for x in range(self.n) if self.grid[x][y] is None]
        logger.debug(f"Empty positions: {len(empty_positions)}")
        if not empty_positions:
            return None
        return random.choice(empty_positions)

    def add(self, tile=None):
        """Add a tile to the grid."""
        # The Group __init__ calls add, so we add tile=None to our add method
        if tile is not None:
            super().add(tile)
            row, col = tile.coords
            self.grid[row][col] = tile.value


class Tile(pygame.sprite.Sprite):
    """A tile in the 2048 game."""
    def __init__(self, value, position=None, rect_size=0):
        super().__init__()
        self.value = value
        self.image = pygame.image.load(f"./0000{value}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect_size = rect_size

        # position is a grid coordinate (col, row)
        row, col = (0, 0) if position is None else position
        self.rect.topleft = (col * rect_size, row * rect_size)
        self.coords = (row, col)

    def _new_coords(self, axis, index, current):
        """Calculate new coordinates for the tile based on movement direction.

        Returns the minimum empty index of this axis.
        If there's no empty space, stay in the same position
        """
        logger.debug(f"Axis: {axis}")
        logger.debug(f"Index: {index}")
        move = False
        for i in index:
            if axis[i] is None:
                move = True
                break
        if move:
            logger.debug(f"Moving from {current} to {i}")
            return i, self.value
        logger.debug(f"Staying at {current}")
        return current, self.value

    def update(self, position=None):
        """Update the tile's position on the screen."""
        if position is None:
            return
        else:
            # Clear out current tile's position
            logger.debug(f"Updating tile {self.value} at {self.coords} moving {position}")
            game = self.groups()[0]
            if position == "up":
                col = self.coords[1]
                row, value = self._new_coords([game.grid[i][col] for i in range(game.n)], range(self.coords[0]), self.coords[0])
            elif position == "down":
                col = self.coords[1]
                row, value = self._new_coords([game.grid[i][col] for i in range(game.n)], range(game.n-1, self.coords[0], -1), self.coords[0])
            elif position == "left":
                row = self.coords[0]
                col, value = self._new_coords(game.grid[row][:], range(self.coords[1]), self.coords[1])
            elif position == "right":
                row = self.coords[0]
                col, value = self._new_coords(game.grid[row][:], range(game.n-1, self.coords[1], -1), self.coords[1])
            # Set new position
            game.grid[self.coords[0]][self.coords[1]] = None
            game.grid[row][col] = self.value
            self.rect.topleft = (col * self.rect_size, row * self.rect_size)
            self.coords = (row, col)
            self.value = value


def clear_screen(screen, n=5):
    """Clear the screen and draw the grid lines."""

    border_color = (255, 255, 255)
    border_width = 5
    screen_background = "#414558"
    screen.fill(screen_background)

    width, height = screen.get_size()
    rect_size = width // n

    pygame.draw.rect(screen, border_color, (0, 0, width, height), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, rect_size, height), border_width)
    pygame.draw.rect(screen, border_color, (0, 0, width, rect_size), border_width)
    for i in range(1, n):
        pygame.draw.rect(screen, border_color, (0, 0, i * rect_size, height), border_width)
        pygame.draw.rect(screen, border_color, (0, 0, width, i * rect_size), border_width)

    return rect_size


async def main(n=5):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("2048 Game")

    clock = pygame.time.Clock()
    running = True

    default_tiles = {
        "2": "./00002.png",
        "4": "./00004.png",
        # "8": "./twofortyeight/assets/00008.png",
        # "16": "./twofortyeight/assets/00016.png",
        # "32": "./twofortyeight/assets/00032.png",
        # "64": "./twofortyeight/assets/00064.png",
        # "128": "./twofortyeight/assets/00128.png",
        # "256": "./twofortyeight/assets/00256.png",
        # "512": "./twofortyeight/assets/00512.png",
        # "1024": "./twofortyeight/assets/01024.png",
        # "2048": "./twofortyeight/assets/02048.png",
    }

    grid = Grid(n)
    rect_size = clear_screen(screen, n)
    grid.draw(screen)
    new_pos = grid.get_empty_pos()
    grid.add(Tile(2, new_pos, rect_size))
    logger.debug(f"Added tile at position {new_pos}")
    grid.tiles.append(grid.sprites()[-1])
    screen.blit(grid.tiles[-1].image, (grid.tiles[-1].rect.x, grid.tiles[-1].rect.y))
    logger.debug(grid.grid)
    while running:
        # fill the screen with a color to wipe away anything from last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                logger.debug("MOVEMENT")
                if event.key == pygame.K_UP:
                    grid.update(position="up")
                elif event.key == pygame.K_DOWN:
                    grid.update(position="down")
                elif event.key == pygame.K_LEFT:
                    grid.update(position="left")
                elif event.key == pygame.K_RIGHT:
                    grid.update(position="right")
                logger.debug("After update:")
                logger.debug(grid.grid)
                # Spawn a new tile at a random position in the grid
                # If no empty positions are available, the game is over
                new_pos = grid.get_empty_pos()
                logger.debug(f"New position for tile: {new_pos}")
                if new_pos is None:
                    logger.debug("Game Over!")
                    running = False
                else:
                    grid.add(Tile(2, new_pos, rect_size))
                    logger.debug(f"Added tile at position {new_pos}")
                    grid.tiles.append(grid.sprites()[-1])
                rect_size = clear_screen(screen, n)
                grid.draw(screen)
                screen.blit(
                    grid.tiles[-1].image, (grid.tiles[-1].rect.x, grid.tiles[-1].rect.y)
                )
                logger.debug(grid.grid)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # This is for PyScript compatibility
        await asyncio.sleep(1 / 60)
        #clock.tick(60)

    pygame.quit()

try:
    asyncio.get_running_loop()
    asyncio.create_task(main(5))
except RuntimeError:
    asyncio.run(main(5))
