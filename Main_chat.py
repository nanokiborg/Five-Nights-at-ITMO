import pygame
from chat import show_chat_window # импорт функции из файла с ЧАТОМ

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FNaITMO")
pygame.display.set_icon(pygame.image.load('Five-Nights-at-ITMO\textures\icon.png')) 
# для более корректного поиска изображения удлиннила ссылку 
# P.s. по старому пути images\icon.png не находило вообще

running = True
while running:

    screen.blit(pygame.image.load('Five-Nights-at-ITMO\textures\icon.png'), (144, 44)) 
    # для более корректного поиска изображения удлиннила ссылку 

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_u:
                screen.fill((0, 255, 0))
            elif event.key == pygame.K_h:  # Это обозначение кнопки для открытия ЧАТА
                show_chat_window()

        elif event.type == pygame.KEYUP:
            screen.fill((255, 0, 0))