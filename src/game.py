import pygame
import sys
import os
import json
from src.ui import UI
from src.animation import AnimationSystem
from src.constants import *
from src.achievement import AchievementSystem
from src.language import LanguageManager

class Game:
    """
    Головний клас гри з баклажаном.
    Керує станом гри, взаємодією користувача та відображенням.
    """
    def __init__(self):
        """Ініціалізація гри, налаштування вікна та завантаження ресурсів."""
        pygame.init()
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        
        # Створення вікна з можливістю зміни розміру
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Гра з Баклажаном")
        
        # Ініціалізація менеджера мови
        self.language_manager = LanguageManager()
        
        # Ініціалізація ігрового стану
        self.left_clicks = 0
        self.right_clicks = 0
        self.particles = []
        self.running = True
        self.show_achievements_panel = False
        
        # Встановлення видимості курсору (завжди видимий для запису екрану)
        pygame.mouse.set_visible(True)
        
        # Налаштування для запису екрану
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Центрування вікна на екрані
        
        # Завантаження зображення баклажана
        self.load_resources()
        
        # Ініціалізація підсистем
        self.ui = UI(self.screen, self.width, self.height, self.language_manager)
        self.animation = AnimationSystem(self.screen, self.eggplant_image, self.eggplant_rect)
        self.achievements = AchievementSystem(self.language_manager)
        
        # Завантаження збереженого прогресу
        self.load_progress()
        
        # Створення таймера для стабільної частоти кадрів
        self.clock = pygame.time.Clock()
    
    def load_resources(self):
        """Завантаження зображень та інших ресурсів."""
        try:
            # Отримання шляху до папки з ресурсами відносно поточного файлу
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            eggplant_path = os.path.join(script_dir, "assets", "images", "eggplant.png")
            
            self.eggplant_image = pygame.image.load(eggplant_path)
            self.eggplant_rect = self.eggplant_image.get_rect()
            self.eggplant_rect.center = (self.width // 2, self.height // 2)
        except pygame.error as e:
            print(f"Не вдалося завантажити зображення баклажана: {e}")
            # Створення заглушки - фіолетовий прямокутник
            self.eggplant_image = pygame.Surface((100, 150))
            self.eggplant_image.fill(EGGPLANT_COLOR)
            self.eggplant_rect = self.eggplant_image.get_rect()
            self.eggplant_rect.center = (self.width // 2, self.height // 2)
    
    def save_progress(self):
        """Збереження прогресу гри у файл."""
        data = {
            "left_clicks": self.left_clicks,
            "right_clicks": self.right_clicks,
            "achievements": [a for a in self.achievements.achievements if a["achieved"]]
        }
        
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            save_path = os.path.join(script_dir, "save_data.json")
            
            with open(save_path, "w") as file:
                json.dump(data, file)
                print("Прогрес збережено")
        except (IOError, OSError) as e:
            print(f"Не вдалося зберегти прогрес: {e}")
    
    def load_progress(self):
        """Завантаження прогресу гри з файлу."""
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            save_path = os.path.join(script_dir, "save_data.json")
            
            with open(save_path, "r") as file:
                data = json.load(file)
                self.left_clicks = data.get("left_clicks", 0)
                self.right_clicks = data.get("right_clicks", 0)
                
                # Завантаження досягнень
                saved_achievements = data.get("achievements", [])
                for saved in saved_achievements:
                    for achievement in self.achievements.achievements:
                        if saved.get("name") == achievement["name"]:
                            achievement["achieved"] = True
                
                print("Прогрес завантажено")
        except (IOError, json.JSONDecodeError, FileNotFoundError):
            print("Не вдалося завантажити прогрес, починаємо з нуля")
    
    def handle_events(self):
        """Обробка подій введення користувача."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.save_progress()
            
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Перевіряємо, чи відкрито панель досягнень
                if self.show_achievements_panel:
                    if event.button == 1:  # Ліва кнопка миші
                        # Перевіряємо натискання на кнопку "Закрити"
                        if self.ui.close_button_rect.collidepoint(event.pos):
                            self.show_achievements_panel = False
                else:
                    # Перевіряємо кнопки інтерфейсу
                    if event.button == 1:  # Ліва кнопка миші
                        if self.ui.achievements_button_rect.collidepoint(event.pos):
                            self.show_achievements_panel = True
                        elif self.eggplant_rect.collidepoint(event.pos):
                            self.handle_eggplant_click(event.button)
                    elif event.button == 3 and self.eggplant_rect.collidepoint(event.pos):  # Права кнопка миші
                        self.handle_eggplant_click(event.button)
    
    def handle_eggplant_click(self, button):
        """
        Обробка кліку на баклажан.
        
        Args:
            button: Кнопка миші (1 - ліва, 3 - права)
        """
        if button == 1:  # Ліва кнопка миші
            self.left_clicks += 1
        elif button == 3:  # Права кнопка миші
            self.right_clicks += 1
            
        self.animation.start_click_animation()
        mouse_pos = pygame.mouse.get_pos()
        self.animation.spawn_particles(mouse_pos)
        
        # Перевірка досягнень після кліку
        total_clicks = self.left_clicks + self.right_clicks
        self.achievements.check_achievements(total_clicks)
        
        # Показуємо текст над баклажаном
        self.animation.add_floating_text(f"+1 ({self.language_manager.get_text('total')}: {total_clicks})")
    
    def handle_resize(self, width, height):
        """Обробляє зміну розміру вікна."""
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.eggplant_rect.center = (self.width // 2, self.height // 2)
        self.ui.update_screen_size(width, height)
    
    def update(self):
        """Оновлення ігрового стану."""
        self.animation.update()
        self.achievements.update()
    
    def render(self):
        """Рендеринг всіх елементів гри."""
        # Очищення екрану
        self.screen.fill(BACKGROUND_COLOR)
        
        # Малювання баклажана
        self.animation.render(self.eggplant_rect.center)
        
        # Малювання UI
        total_clicks = self.left_clicks + self.right_clicks
        self.ui.render(self.left_clicks, self.right_clicks, total_clicks, self.achievements)
        
        # Малювання досягнень
        self.achievements.render(self.screen)
        
        # Малювання панелі досягнень
        if self.show_achievements_panel:
            self.ui.render_achievements_panel(self.achievements.achievements, total_clicks)
        
        # Оновлення екрану
        pygame.display.flip()
    
    def run(self):
        """Головний цикл гри."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()