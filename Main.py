import pygame
import subprocess

if __name__ == "__main__":
    # Инициализация Pygame
    pygame.init()

    # Инициализация микшера для музыки
    pygame.mixer.init()

    # Загрузка фоновой музыки для игры
    pygame.mixer.music.load("music/fnaf_8bit.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Настройка экрана
    screen = pygame.display.set_mode((720, 512))
    pygame.display.set_caption("Main Menu")

    # Загрузка фонового изображения c кнопкой
    background_image = pygame.image.load("icon/main_menu.png")  
    background_image = pygame.transform.scale(background_image, (720, 512))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Проверка нажатия мышкой на кнопку
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 258 <= mouse_x <= 462 and 356 <= mouse_y <= 434:
                    subprocess.Popen(["python", "game.py"])  # Запускаем game.py
                    subprocess.Popen(["python", "chat.py"])  # Запускаем chat.py
                    running = False  

        # Отрисовка фона с кнопки
            screen.blit(background_image, (0, 0))

        # Обновление экрана
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()