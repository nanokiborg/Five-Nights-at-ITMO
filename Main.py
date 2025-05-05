import pygame
import subprocess  


if __name__=="__main__":
    # Инициализация Pygame
    pygame.init()

    # Настройка экрана
    screen = pygame.display.set_mode((640, 360))
    pygame.display.set_caption("Главное меню")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Проверка нажатия мышкой на кнопки
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 220 <= mouse_x <= 420  and 120 <= mouse_y <= 170:
                    subprocess.Popen(["python", "game.py"])  # Запускаем game.py
                    running = False  # Закрываем окно с меню

        screen.fill(WHITE)

        # Отрисовка кнопок
        pygame.draw.rect(screen, BLACK, (210, 120, 200, 50))
        pygame.draw.rect(screen, BLACK, (210, 220, 200, 50))

        pygame.display.flip()

        # Задержка для контроля частоты кадров
        pygame.time.Clock().tick(60)