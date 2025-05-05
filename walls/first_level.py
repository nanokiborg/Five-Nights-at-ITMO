import pygame
import random

def generate_random_walls(count, map_width, map_height):
    """ Генерирует случайные стены на карте """
    walls = []
    for _ in range(count):
        x = random.randint(0, map_width - 100)
        y = random.randint(0, map_height - 100)
        width = random.randint(50, 200)
        height = random.randint(50, 200)
        walls.append(pygame.Rect(x, y, width, height))
    return walls

def create_manual_walls():
    """ Создает стены вручную """
    walls = [
        pygame.Rect(800, 500, 50, 200),
        pygame.Rect(1000, 300, 200, 50),
        pygame.Rect(1200, 700, 50, 300),
    ]
    return walls