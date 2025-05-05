import pygame

# Класс для управления стенами
class WallManager:
    def __init__(self):
        self.walls = [] 

    def add_walls(self, walls):
        """Добавляет новую стену"""
        self.walls.extend(walls)

    def check_collision(self, obj_connect):
        """Проверяет столкновение объекта с любой из стен"""
        for wall in self.walls:
            if obj_connect.colliderect(wall):
                return True
        return False

    def draw(self, surface, camera):
        """Отрисовывает все стены"""
        for wall in self.walls:
                pygame.draw.rect(surface, (0, 0, 0), wall)