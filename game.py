import pygame
import math
import sys
from walls.wallmanager import WallManager
from walls.first_level import generate_random_walls, create_manual_walls


if __name__=="__main__":
    # Инициализация Pygame
    pygame.init()

    # Цвет, размеры экрана и карты
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 360
    MAP_WIDTH, MAP_HEIGHT = 2000, 2000


    # Создание экрана игрока
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("FNaITMO")
    pygame.display.set_icon(pygame.image.load('textures/icon.png'))

    # Константы пресонажа
    PLAYER_IMAGE_1 = pygame.image.load('textures/player_1.png')
    PLAYER_IMAGE_2 = pygame.image.load('textures/player_2.png')
    PLAYER_POSITION_X = 300
    PLAYER_POSITION_Y = 600
    speed = 4

    # Константы для анимации
    current_frame = PLAYER_IMAGE_1  
    animation_timer = 0     
    animation_speed = 30 # Скорость смены кадров (в кадрах в секунду)

    # Задание начальной позиции и создание камеры персонажа
    PLAYER = PLAYER_IMAGE_1.get_rect(center=(PLAYER_POSITION_X, PLAYER_POSITION_Y))
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    #Создание менеджера стен
    wall_manager = WallManager()

    # Создание и задание положения стенам
    # Вариант 1: Добавление стен вручную
    manual_walls = create_manual_walls()
    wall_manager.add_walls(manual_walls)

    # Вариант 2: Добавление случайных стен
    random_walls = generate_random_walls(5, MAP_WIDTH, MAP_HEIGHT)
    wall_manager.add_walls(random_walls)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
        if wall_manager.check_collision(PLAYER):
            PLAYER.x, PLAYER.y = prev_x, prev_y
            
        # Ограничение перемещения объекта в пределах карты
        PLAYER.x = max(0, min(PLAYER.x, MAP_WIDTH - PLAYER.width))
        PLAYER.y = max(0, min(PLAYER.y, MAP_HEIGHT - PLAYER.height))

        # Обновление камеры
        camera.center = PLAYER.center  # Камера следует за объектом
        camera.x = max(0, min(camera.x, MAP_WIDTH - SCREEN_WIDTH))  # Ограничение по ширине
        camera.y = max(0, min(camera.y, MAP_HEIGHT - SCREEN_HEIGHT))  # Ограничение по высоте

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

        # Определение угла поворота и расположение курсора
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        dx = mouse_pos_x - (PLAYER.centerx - camera.x)
        dy = mouse_pos_y - (PLAYER.centery - camera.y)
        angle = math.degrees(math.atan2(-dy, dx)) 

        # Изменение поворота объекта в зависимости от направления курсора
        rotated_image = pygame.transform.rotate(current_frame, angle)
        rotated_player = rotated_image.get_rect(center=PLAYER.center)
        # Отрисовка ---------------
        screen.fill(WHITE)

        # Отрисовка карты
        map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        map_surface.fill(GRAY)

        # Рисуем сетку для визуализации карты
        for x in range(0, MAP_WIDTH, 50):
            pygame.draw.line(map_surface, BLACK, (x, 0), (x, MAP_HEIGHT))
        for y in range(0, MAP_HEIGHT, 50):
            pygame.draw.line(map_surface, BLACK, (0, y), (MAP_WIDTH, y))

        # Рисуем стены
        wall_manager.draw(map_surface, camera)

        # Отображение части карты через камеру
        screen.blit(map_surface, (0, 0), camera)

        # Финальная отрисовка персонажа
        screen.blit(rotated_image, (rotated_player.x - camera.x, rotated_player.y - camera.y))

        
        pygame.display.flip()

        # Задержка для правильного отображение(равна частоте кадров) 
        pygame.time.Clock().tick(60)