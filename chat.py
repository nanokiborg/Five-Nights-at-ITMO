import tkinter as tk
from tkinter import scrolledtext, font, ttk
from tkinter import PhotoImage
import keyboard  # Для обработки горячих клавиш
import threading  # Для работы в фоновом режиме

# Предопределенные ответы для разных чатов
CHAT_BOTS = {
    "МАТАН-БАЗА": {
        "name": "Правдин К.В.",  
        "Когда будет ПР1?": "Здравсвуйте! Очень своевременный вопрос)) ПР1 будет завтра утром! Советуем вам выспаться и хорошо написать проверочную работу!",
        "Будет ли проводится ПР1?": "Здравсвуйте! Конечно же, да",
        "А можно не присать ПР1 ?": "Здравствуйте! Перенос ПР1 возможен лишь по уважительной причине со стороны студента",
        "default": "Мы не понимаем ваш вопрос! Вы можете спросить: 'Когда будет ПР1?', 'Будет ли проводится ПР1?', 'А можно не присать ПР1 ?'"
    },
    "Техподдержка": {
        "name": "Технический специалист",  
        "привет": "Здравствуйте! Чем могу помочь?",
        "проблема": "Опишите вашу проблему подробнее.",
        "спасибо": "Спасибо за обращение!",
        "default": "Техподдержка: уточните ваш вопрос."
    },
    "Дружище": {
        "name": "Дружище", 
        "привет": "Привет! Как жизнь?",
        "шутка": "Русалка села на шпагат!",
        "default": "Хочешь услышать шутку? Напиши 'шутка'"
    }
}

class ChatTab(ttk.Frame):
    def __init__(self, master, chat_name, bot_responses, bg_image=None):
        super().__init__(master)
        self.chat_name = chat_name
        self.bot_name = bot_responses["name"]  # Берем имя бота из его конфигурации
        self.bot_responses = bot_responses
        self.bg_image = bg_image
        self.create_widgets()
        
    def create_widgets(self):
        # Создаем Canvas для фона
        self.canvas = tk.Canvas(self, bg='#f0f0f0', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Устанавливаем фоновое изображение если оно есть
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        # Основной фрейм для элементов чата
        self.chat_frame = tk.Frame(self.canvas, bg='white', bd=0)
        self.canvas.create_window(20, 20, window=self.chat_frame, anchor="nw", width=440, height=550)
        
        # Текстовое поле чата
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=font.Font(family="Helvetica", size=12),
            bg='white',
            bd=0,
            highlightthickness=0
        )
        self.chat_area.pack(padx=10, pady=10)
        
        # Настройка тегов для сообщений
        self.chat_area.tag_configure('user', background='#e3f2fd', lmargin1=10, lmargin2=10, rmargin=10, spacing2=5)
        self.chat_area.tag_configure('bot', background='#f5f5f5', lmargin1=10, lmargin2=10, rmargin=10, spacing2=5)
        self.chat_area.tag_configure('bold', font=('Helvetica', 12, 'bold'))
        
        # Фрейм для поля ввода и кнопки
        self.entry_frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window(20, 580, window=self.entry_frame, anchor="nw", width=440)
        
        # Поле ввода
        self.entry = tk.Entry(self.entry_frame, width=35, font=('Helvetica', 12), bd=1, relief=tk.SOLID)
        self.entry.pack(side=tk.LEFT, padx=(0, 5), pady=5)
        
        # Кнопка отправки (справа от поля ввода)
        self.send_button = tk.Button(
            self.entry_frame, 
            text="Отправить", 
            command=self.send_message,
            bg='#4CAF50',
            fg='white',
            bd=0,
            padx=15
        )
        self.send_button.pack(side=tk.LEFT, pady=5)
        
        welcome_messages = {
            "МАТАН-БАЗА": """
☀️  Проверочная работа № 1\n
\nПР 1 пройдёт на второй практике по теме "Таблица неопределённых интегралов".
\n🟣 ключевая контрольная точка
\n🔵 10 задач на табличные интегралы
\n🔵 порог 60% (6 из 10)
\n🔵 0 / 5 баллов
\n🔵 15 мин. 10 мин.
\nТаблица представлена к учебнике А.А. Бойцева, найдите её! Будут именно задачи на таблицу интегралов, а не просьба привести справочные сведения из неë. Демо-вариант ПР 1 не публикуется, вы легко справитесь без него!
""",
            "Техподдержка": "Здравствуйте! Это чат технической поддержки. Чем можем помочь?",
            "Развлечения": "Привет! Готовы к развлечениям? Здесь вас ждут шутки и игры!"
        }
    
        # Приветственное сообщение в зависимости от типа чата
        welcome_message = welcome_messages.get(self.chat_name, "Добро пожаловать в этот чат!")
        self.add_message(self.bot_name, welcome_message, 'bot')  # Используем self.bot_name
        
        # Привязка Enter к отправке
        self.entry.bind("<Return>", lambda e: self.send_message())
    
    def add_message(self, sender, message, tag):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}:\n", 'bold')
        self.chat_area.insert(tk.END, f"{message}\n\n", tag)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def send_message(self):
        user_input = self.entry.get().strip().lower()  # Приводим к нижнему регистру
        if not user_input:
                return
    
        self.add_message("Вы", user_input, 'user')
        self.entry.delete(0, tk.END)
    
        # Создаем словарь с ключами в нижнем регистре (исключая служебные ключи)
        lower_responses = {k.lower(): v for k, v in self.bot_responses.items() 
        if k != "name" and k != "default"}
    
        bot_response = lower_responses.get(user_input, self.bot_responses["default"])
        self.add_message(self.bot_name, bot_response, 'bot')

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Telegram-ITMO")
        
        # Фиксированный размер окна 480x720
        self.root.geometry("480x720")
        self.root.resizable(False, False)  # Запрет изменения размера
        
        # Загружаем фоновое изображение (если есть)
        try:
            self.bg_image = PhotoImage(file=r'textures/chat.gif')
            # Масштабируем изображение под размер окна
            self.bg_image = self.bg_image.zoom(1)  # Можно настроить под ваш размер изображения
            self.bg_image = self.bg_image.subsample(2)  # Или subsample для уменьшения
        except:
            self.bg_image = None
        
        # Создаем панель вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        
        # Создаем вкладки для каждого чата
        self.tabs = {}
        for chat_name, bot_responses in CHAT_BOTS.items():
            tab = ChatTab(self.notebook, chat_name, bot_responses, self.bg_image)
            self.notebook.add(tab, text=chat_name)
            self.tabs[chat_name] = tab

def start_chat():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

def run_in_background():
    # Назначаем горячую клавишу 'q' для открытия чата
    keyboard.add_hotkey('q', start_chat)
    
    # Сообщение в консоль
    print("Программа работает в фоновом режиме. Нажмите 'q' для открытия чата.")
    print("Для выхода нажмите 'ё' в консоли.")
    
    # Создаем событие для остановки
    stop_event = threading.Event()
    
    # Функция для остановки по 'ё'
    def stop_handler():
        print("\nЗавершение программы по нажатию 'ё'...")
        keyboard.unhook_all()
        stop_event.set()
    
    keyboard.add_hotkey('ё', stop_handler)
    
    # Ожидаем либо остановки, либо закрытия
    while not stop_event.is_set():
        stop_event.wait(0.1)  # Проверяем каждые 100 мс
    
    # Корректно завершаем все обработчики
    keyboard.unhook_all()
chat_window_open = False

def start_chat():
    global chat_window_open
    if not chat_window_open:
        chat_window_open = True
        root = tk.Tk()
        app = ChatApp(root)
        
        def on_close():
            global chat_window_open
            chat_window_open = False
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()

def main():
    keyboard.add_hotkey('q', start_chat)
    print("Нажмите 'q' для открытия чата...")
    print("Нажмите 'F12' или Fn+F12 для выхода из программы...")
    keyboard.wait('F12')  # Ожидаем 'F12'
    print("Завершение программы...")

if __name__ == "__main__":
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()
    main_thread.join()  # Ждем завершения потока