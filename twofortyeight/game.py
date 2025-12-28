import asyncio
import pygame
import random


def clear_screen():
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

border_color = (255, 255, 255)
border_width = 5

clear_screen()

clock = pygame.time.Clock()
running = True

# player_pos must be one of the empty tiles, chosen at random
rx, ry = random.randint(0, 4), random.randint(0, 4)
player_pos = pygame.Vector2(rx * screen.get_width() / 5, ry * screen.get_height() / 5)

tiles = {
    "two": "00002.png",
    "four": "00004.png",
    "eight": "00008.png",
    "sixteen": "00016.png",
    # "thirty_two": "00032.png",
    # "sixty_four": "00064.png",
    # "one_twenty_eight": "00128.png",
    # "two_fifty_six": "00256.png",
    # "five_twelve": "00512.png",
    # "one_zero_two_four": "01024.png",
    # "two_zero_four_eight": "02048.png",
}

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    clear_screen()

    # spawn a new tile at a random position in the grid
    spawn = pygame.image.load(tiles["two"])
    screen.blit(spawn, (player_pos.x, player_pos.y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos.y -= 10
    if keys[pygame.K_DOWN]:
        player_pos.y += 10
    if keys[pygame.K_LEFT]:
        player_pos.x -= 10
    if keys[pygame.K_RIGHT]:
        player_pos.x += 10

    # flip() the display to put your work on screen
    pygame.display.flip()

    # This is for PyScript compatibility
    await asyncio.sleep(1 / 60)
