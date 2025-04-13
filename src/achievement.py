import pygame
from src.constants import *

class AchievementSystem:
    """
    Система досягнень для гри з баклажаном.
    """
    def __init__(self, language_manager):
        """
        Ініціалізація системи досягнень.
        
        Args:
            language_manager: Менеджер мови для перекладу текстів
        """
        self.language_manager = language_manager
        
        # Копіюємо список досягнень з констант
        self.achievements = []
        for achievement in ACHIEVEMENTS:
            self.achievements.append(achievement.copy())
        
        # Змінні для відображення повідомлень про досягнення
        self.achievement_text = None
        self.achievement_timer = 0
        
        # Ініціалізація шрифту
        self.font = pygame.font.Font(None, LARGE_FONT_SIZE)
    
    def check_achievements(self, total_clicks):
        """
        Перевірка досягнень на основі загальної кількості кліків.
        
        Args:
            total_clicks: Загальна кількість кліків
        """
        for i, achievement in enumerate(self.achievements):
            if total_clicks >= achievement["threshold"] and not achievement["achieved"]:
                achievement["achieved"] = True
                
                # Отримуємо перекладену назву досягнення
                achievement_name = self.language_manager.get_achievement_name(i)
                self.show_achievement(achievement_name)
    
    def show_achievement(self, name):
        """
        Показує повідомлення про отримане досягнення.
        
        Args:
            name: Назва досягнення
        """
        self.achievement_text = self.font.render(
            f"{self.language_manager.get_text('achievement_unlocked')}: {name}!", 
            True, 
            ACHIEVEMENT_COLOR
        )
        self.achievement_timer = ACHIEVEMENT_DISPLAY_TIME
    
    def update(self):
        """Оновлення стану системи досягнень."""
        if self.achievement_timer > 0:
            self.achievement_timer -= 1
    
    def render(self, screen):
        """
        Рендеринг повідомлення про досягнення.
        
        Args:
            screen: Поверхня для рендерингу
        """
        if self.achievement_timer > 0 and self.achievement_text:
            # Обчислюємо прозорість
            alpha = 255
            if self.achievement_timer < 30:  # Затухання в останню секунду
                alpha = int(255 * (self.achievement_timer / 30))
            
            # Створюємо копію тексту з потрібною прозорістю
            text_surface = self.achievement_text.copy()
            text_surface.set_alpha(alpha)
            
            # Центруємо текст на екрані
            x = screen.get_width() // 2 - text_surface.get_width() // 2
            y = 80  # Трохи нижче верхнього краю екрану
            
            # Малюємо напівпрозоре тло
            bg_rect = text_surface.get_rect()
            bg_rect.center = (screen.get_width() // 2, y + text_surface.get_height() // 2)
            bg_rect.inflate_ip(20, 10)  # Трохи більший розмір, ніж текст
            
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(min(128, alpha // 2))  # Половина прозорості тексту
            
            screen.blit(bg_surface, bg_rect)
            screen.blit(text_surface, (x, y))
            
    def get_unlocked_achievements(self):
        """
        Отримує список розблокованих досягнень.
        
        Returns:
            Список розблокованих досягнень
        """
        return [a for a in self.achievements if a["achieved"]]