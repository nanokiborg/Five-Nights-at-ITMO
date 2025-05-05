import pygame
import sys
import os
import subprocess
from pygame.locals import *
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Скрывает лишнюю консоль
# P.s. не особо помогло кнч


class ChatWindow:
    def __init__(self):      
        pygame.init() 
        self.screen = pygame.display.set_mode((480, 720))
        pygame.display.set_caption("ЧАТ МАТАНБАЗА 2025")
        self.clock = pygame.time.Clock()

        self.bg_color = (40, 40, 40)
        self.text_color = (220, 220, 255)
        self.font = pygame.font.Font(None, 32)
        self.line_height = 36
        self.margin = 20

        self.lines = [
            "===МАТАН БАЗА 2025===",
            "",
            "Силлабус",
            "События:",
            "Преподаватели:",
            "Дедлайны:"
        ]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            self.screen.fill(self.bg_color)

            y_pos = self.margin
            for line in self.lines:
                if line: 
                    text_surface = self.font.render(line, True, self.text_color)
                    self.screen.blit(text_surface, (self.margin, y_pos))
                y_pos += self.line_height
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
        sys.exit()

def show_chat_window():
    """Запуск текстового окна в отдельном процессе"""
    script_path = os.path.join(os.path.dirname(__file__), "chat.py")
    if sys.platform == "win32":
        subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen([sys.executable, script_path])

if __name__ == "__main__":
    window = ChatWindow()
    window.run()