import pygame

class WallManager:
    def __init__(self):
        self.walls = []  # Список всех стен

    def add_wall(self, x, y, width, height):
        """Добавляет новую стену."""
        wall = pygame.Rect(x, y, width, height)
        self.walls.append(wall)

    def check_collision(self, rect):
        """Проверяет столкновение объекта с любой из стен."""
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        return False

    def draw(self, surface, camera):
        """Отрисовывает все стены на карте через камеру."""
        for wall in self.walls:
            # Рисуем только видимую часть стены
            visible_wall = wall.clip(camera)  # Обрезаем стену по границам камеры
            if visible_wall.width > 0 and visible_wall.height > 0:
                visible_wall.topleft = (wall.x - camera.x, wall.y - camera.y)
                pygame.draw.rect(surface, (0, 0, 0), visible_wall)