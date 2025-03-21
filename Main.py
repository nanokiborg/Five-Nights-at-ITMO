import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FNaITMO")
pygame.display.set_icon(pygame.image.load('images/icon.png'))

running = True
while running:

    screen.blit(pygame.image.load('images/icon.png'), (144, 44))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_u:
                screen.fill((0, 255, 0))

        elif event.type == pygame.KEYUP:
            screen.fill((255, 0, 0))