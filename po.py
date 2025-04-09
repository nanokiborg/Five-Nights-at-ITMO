import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

# Настройка экрана
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("FNaITMO")
pygame.display.set_icon(pygame.image.load('images/icon.png'))

# Цвет и размеры экрана
WHITE = (255, 255, 255)
WHIGHT = 800
LENGHT = 600

# Константы пресонажа
PLAYER_IMAGE_1 = pygame.image.load('images/player_1.png')
PLAYER_IMAGE_2 = pygame.image.load('images/player_2.png')
PLAYER_POSITION_X = 600
PLAYER_POSITION_Y = 300
PLAYER = PLAYER_IMAGE_1.get_rect(center=(PLAYER_POSITION_X, PLAYER_POSITION_Y))
size = 50
speed = 4

# Константы для анимации
current_frame = PLAYER_IMAGE_1  
animation_timer = 0     
animation_speed = 30 # Скорость смены кадров (в кадрах в секунду)

# Создание и задание параметров стены
BLACK = (0, 0, 0)
wall = pygame.Rect(390, 100, 20, 400) 

while True:
    # Определение угла поворота
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    dx = mouse_pos_x - PLAYER.centerx
    dy = mouse_pos_y - PLAYER.centery
    angle = math.degrees(math.atan2(-dy, dx))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if wall.collidepoint(mouse_pos_x, mouse_pos_y):
                wall = None  # Стена уничтожена

    # Изменение позиции игрока в зависимости от нажатых клавиш
    keys = pygame.key.get_pressed()
    prev_x, prev_y = PLAYER.x, PLAYER.y # Сохраняем текущую позицию
    moving_trig = False

    if keys[pygame.K_a]:  # Клавиша "Влево
        PLAYER.x -= speed
        moving_trig = True
    if keys[pygame.K_d]:  # Клавиша "Вправо"
        PLAYER.x += speed
        moving_trig = True
    if keys[pygame.K_w]:  # Клавиша "Вверх"
        PLAYER.y -= speed
        moving_trig = True
    if keys[pygame.K_s]:  # Клавиша "Вниз"
        PLAYER.y += speed
        moving_trig = True
      
    # Проверка коллизии со стеной
    if wall and PLAYER.colliderect(wall):
        PLAYER.x, PLAYER.y = prev_x, prev_y

    # Ограничение перемещения объекта в пределах экрана
    PLAYER.x = max(0, min(PLAYER.x, 800 - size)) 
    PLAYER.y = max(0, min(PLAYER.y, 600 - size))

    # Анимация
    if moving_trig:
        animation_timer += 1
        if animation_timer >= animation_speed:
            animation_timer = 0
            if current_frame == PLAYER_IMAGE_1:
                current_frame = PLAYER_IMAGE_2
            else:
                current_frame = PLAYER_IMAGE_1
    else:
        current_frame = PLAYER_IMAGE_1

    # Изменение поворота объекта в зависимости от направления курсора
    rotated_image = pygame.transform.rotate(current_frame, angle)
    rotated_player = rotated_image.get_rect(center=PLAYER.center)

    # Отрисовка
    screen.fill(WHITE)
    if wall:
        pygame.draw.rect(screen, BLACK, wall)
    screen.blit(rotated_image, rotated_player)
    pygame.display.flip()

    # Задержка для правильного отображение(равна частоте кадров) 
    pygame.time.Clock().tick(60)