import pygame
import math
from walls import WallManager

# Функция для загрузки карт
def load_map(map_name):
    """Загружает карту и масштабирует её."""
    map_image = pygame.image.load(map_name)
    original_width, original_height = map_image.get_size()
    MAP_WIDTH, MAP_HEIGHT = original_width * 4, original_height * 4  # Увеличиваем размер карты в 4 раза
    map_surface = pygame.transform.scale(map_image, (MAP_WIDTH, MAP_HEIGHT))
    return map_surface, MAP_WIDTH, MAP_HEIGHT


# Функция для создания стен из изображения
def create_walls_from_image(map_surface, wall_manager):
    """Создает стены из изображения, объединяя соседние "стенные" и "объектные" пиксели."""
    walls = []
    visited = [[False for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]

    for y in range(0, MAP_HEIGHT, 5):  
        for x in range(0, MAP_WIDTH, 5):  
            if visited[x][y]:
                continue

            pixel_color = map_surface.get_at((x, y))
            if pixel_color == (WALLS_1 or WALLS_2 or SUBJECT):  
                
                width, height = 5, 5
                while x + width < MAP_WIDTH and map_surface.get_at((x + width, y)) == (WALLS_1 or WALLS_2 or SUBJECT):
                    width += 5
                while y + height < MAP_HEIGHT and all(map_surface.get_at((x + dx, y + height)) == (WALLS_1 or WALLS_2 or SUBJECT) for dx in range(width)) :
                    height += 5

                # Добавляем прямоугольник стены
                wall_rect = pygame.Rect(x, y, width, height)
                wall_manager.add_wall(wall_rect.x, wall_rect.y, wall_rect.width, wall_rect.height)

                # Помечаем пиксели как посещенные
                for dy in range(height):
                    for dx in range(width):
                        visited[x + dx][y + dy] = True

                        
# Инициализация Pygame
pygame.init()

# Настройка разрешения экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 360
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FNaITMO")

# Загрузка первой карты и определение её размеров
map_image = pygame.image.load("maps/hallway.png")
original_width, original_height = map_image.get_size()
MAP_WIDTH, MAP_HEIGHT = original_width * 4, original_height * 4  
map_surface = pygame.transform.scale(map_image, (MAP_WIDTH, MAP_HEIGHT))

# Создание менеджера для отрисовки стен и его параметров
wall_manager = WallManager()
WALLS_1 = (16, 20, 31)
WALLS_2 = (20, 31, 37)
SUBJECT = (22, 29, 40)
create_walls_from_image(map_surface, wall_manager)

# Загрузка изображений для анимации игрока
frame1 = pygame.image.load('hero/PLAYER_1.png')
frame2 = pygame.image.load('hero/PLAYER_2.png')

# Инциализация игрока и присваивание его параметров
PLAYER_x, PLAYER_y = 1200, 2400
PLAYER = frame1.get_rect(center=(PLAYER_x, PLAYER_y))
speed = 5

# Переменные для анимации игрока
current_frame = frame1
animation_timer = 0
animation_speed = 10

# Создание окна камеры и привязывание к игроку
camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
camera.center = (PLAYER_x, PLAYER_y)

# Флаг для отслеживания текущей карты
current_map = "maps/hallway.png"

# Точки перехода
transition_points = {
    "maps/hallway.png": {"to_romb": pygame.Rect(1308, 620, 25, 25), "to_hall": pygame.Rect(1624, 1838, 25, 25), "to_bath_m": pygame.Rect(412, 1858, 25, 25), "to_bath_w": pygame.Rect(600, 1858, 25, 25), "to_class1": pygame.Rect(1612, 1288, 25, 25), "to_class2": pygame.Rect(0, 0, 25, 25), "to_class3": pygame.Rect(1056, 1036, 25, 25), "to_class4": pygame.Rect(1612, 836, 25, 25)},
    "maps/romb.png": {"exit": pygame.Rect(528, 1758, 25, 25)},  
    "maps/hall.png": {"exit": pygame.Rect(928, 1260, 25, 25)}, 
    "maps/bathroom_m.png": {"exit": pygame.Rect(1051, 1004, 25, 25)},
    "maps/bathroom_w.png": {"exit": pygame.Rect(1051, 1074, 25, 25)},
    "maps/class1.png": {"exit": pygame.Rect(840, 1324, 25, 25)},
    "maps/class2.png": {"exit": pygame.Rect(0, 0, 25, 25)},
    "maps/class3.png": {"exit": pygame.Rect(1056, 1150, 25, 25)},
    "maps/class4.png": {"exit": pygame.Rect(1160, 1328, 25, 25)},
}

# бумаги для сбора
items = {
    "maps/hallway.png": [pygame.Rect(1388, 2624, 64, 64)],
    "maps/romb.png": [pygame.Rect(544, 1212, 25, 25)],  
    "maps/hall.png": [pygame.Rect(928, 660, 25, 25)],  
    "maps/bathroom_m.png": [pygame.Rect(948, 880, 25, 25)],
    "maps/bathroom_w.png": [pygame.Rect(888, 1028, 25, 25)],
    "maps/class1.png": [pygame.Rect(1064, 888, 25, 25)],
    "maps/class3.png": [pygame.Rect(776, 564, 25, 25)],
    "maps/class4.png": [pygame.Rect(828, 1260, 25, 25)]
}

# Коллекция собранных работ
collected_paper = set()

# Загрузка изображения для листочков
item_image = pygame.image.load("textures/paper.png")  # Загружаем изображение предмета
item_image = pygame.transform.scale(item_image, (64, 64))  # Масштабируем до нужного размера

# Загрузка первой карты
map_image = pygame.image.load(current_map)
map_surface = pygame.transform.scale(map_image, (MAP_WIDTH, MAP_HEIGHT))
create_walls_from_image(map_surface, wall_manager)


if __name__=="__main__":
    # Основной игровой цикл
    running = True
    while running:
        # Обработка события принудительного завершения работы
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Сохраняем предыдущую позицию персонажа
        prev_x, prev_y = PLAYER_x, PLAYER_y

        # Движение персонажа по нажатиям по кнопкам
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            PLAYER_x -= speed
        if keys[pygame.K_d]:
            PLAYER_x += speed
        if keys[pygame.K_w]:
            PLAYER_y -= speed
        if keys[pygame.K_s]:
            PLAYER_y += speed

        # Ограничение перемещения персонажа в пределах карты
        PLAYER_x = max(0, min(PLAYER_x, MAP_WIDTH - PLAYER.width))
        PLAYER_y = max(0, min(PLAYER_y, MAP_HEIGHT - PLAYER.height))

        # Обновление позиции персонажа
        PLAYER.center = (PLAYER_x, PLAYER_y)

        # Проверка коллизии со стенами
        if wall_manager.check_collision(PLAYER):
            # Если произошло столкновение, возвращаем персонажа на предыдущую позицию
            PLAYER_x, PLAYER_y = prev_x, prev_y
            PLAYER.center = (PLAYER_x, PLAYER_y)

        # Проверка для перехода между локациями
        if current_map == "maps/hallway.png":
            if PLAYER.colliderect(transition_points["maps/hallway.png"]["to_romb"]):
                current_map = "maps/romb.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear()  
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 548, 1728

            elif PLAYER.colliderect(transition_points["maps/hallway.png"]["to_hall"]):
                current_map = "maps/hall.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear()  
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 928, 1210
            
            elif PLAYER.colliderect(transition_points["maps/hallway.png"]["to_bath_m"]):
                current_map = "maps/bathroom_m.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear() 
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 1051, 964
            
            elif PLAYER.colliderect(transition_points["maps/hallway.png"]["to_bath_w"]):
                current_map = "maps/bathroom_w.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear() 
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 1051, 1014
            
            elif PLAYER.colliderect(transition_points["maps/hallway.png"]["to_class1"]):
                current_map = "maps/class1.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear() 
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 840, 1274
            
            elif PLAYER.colliderect(transition_points["maps/hallway.png"]["to_class2"]):
                current_map = "maps/class2.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear() 
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 880, 950

            elif PLAYER.colliderect(transition_points["maps/hallway.png"]["to_class3"]):
                current_map = "maps/class3.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear() 
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 1100, 1120

            elif PLAYER.colliderect(transition_points["maps/hallway.png"]["to_class4"]):
                current_map = "maps/class4.png"
                map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
                wall_manager.walls.clear() 
                create_walls_from_image(map_surface, wall_manager)
                PLAYER_x, PLAYER_y = 1160, 1278
            
        elif current_map == "maps/romb.png" and PLAYER.colliderect(transition_points["maps/romb.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 1300, 720

        elif current_map == "maps/hall.png" and PLAYER.colliderect(transition_points["maps/hall.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 1624, 1940

        elif current_map == "maps/bathroom_m.png" and PLAYER.colliderect(transition_points["maps/bathroom_m.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 412, 1940  

        elif current_map == "maps/bathroom_w.png" and PLAYER.colliderect(transition_points["maps/bathroom_w.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 600, 1940

        elif current_map == "maps/class1.png" and PLAYER.colliderect(transition_points["maps/class1.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 1612, 1388

        elif current_map == "maps/class2.png" and PLAYER.colliderect(transition_points["maps/class2.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 856, 1136

        elif current_map == "maps/class3.png" and PLAYER.colliderect(transition_points["maps/class3.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 1056, 1136 

        elif current_map == "maps/class4.png" and PLAYER.colliderect(transition_points["maps/class4.png"]["exit"]):
            current_map = "maps/hallway.png"
            map_surface, MAP_WIDTH, MAP_HEIGHT = load_map(current_map)
            wall_manager.walls.clear()  
            create_walls_from_image(map_surface, wall_manager)
            PLAYER_x, PLAYER_y = 1612, 936                   

        # Проверка сбора предметов
        for item in items[current_map][:]: 
            if PLAYER.colliderect(item):
                collected_paper.add((current_map))  # Добавляем собранный предмет в коллекцию
                items[current_map].remove(item)  # Удаляем предмет с карты
                print("Предмет собран, собери все, чтобы помочь друзьям!")

        # Проверка завершения игры если собраны все работы
        total_items = 8
        if len(collected_paper) == total_items:
            print("Поздравляем! Вы собрали все предметы, но, что-то пошло не так!")
            running = False

        # Обновление камеры
        camera.center = PLAYER.center
        camera.x = max(0, min(camera.x, MAP_WIDTH - SCREEN_WIDTH))
        camera.y = max(0, min(camera.y, MAP_HEIGHT - SCREEN_HEIGHT))


        # Анимация (работает только при движении)
        if (PLAYER_x, PLAYER_y) != (prev_x, prev_y):
            animation_timer += 1
            if animation_timer >= animation_speed:
                animation_timer = 0
                current_frame = frame1 if current_frame == frame2 else frame2
        else:
            current_frame = frame1

        # Отрисовка карты и игрока
        PLAYER_pos = pygame.transform.rotate(current_frame, 90)
        screen.blit(map_surface, (0, 0), camera)  # Отображаем видимую часть карты через камеру для оптимизации
        screen.blit(PLAYER_pos, (PLAYER.x - camera.x, PLAYER.y - camera.y))

        # Отрисовка предметов
        for item in items[current_map]:
            visible_item = item.move(-camera.x, -camera.y)  
            screen.blit(item_image, (visible_item.x, visible_item.y))

        # Обновление экрана
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()