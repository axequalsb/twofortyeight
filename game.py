import asyncio
import pygame


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

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    clear_screen()

    pygame.draw.circle(screen, "red", player_pos, 40)

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

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    #dt = clock.tick(60) / 1000
    await asyncio.sleep(1 / 60)
