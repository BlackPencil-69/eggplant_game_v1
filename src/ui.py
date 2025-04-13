import pygame
from src.constants import *

class UI:
    """
    Клас для відображення всіх елементів інтерфейсу користувача.
    """
    def __init__(self, screen, width, height, language_manager):
        """
        Ініціалізація інтерфейсу користувача.
        
        Args:
            screen: Поверхня для рендерингу
            width: Ширина екрану
            height: Висота екрану
            language_manager: Менеджер мови
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.language_manager = language_manager
        
        # Ініціалізація шрифтів
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)
        
        # Створення кнопок (тільки кнопка досягнень)
        self.achievements_button_rect = pygame.Rect(self.width - BUTTON_WIDTH - 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.close_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)  # Позиція буде оновлена при рендерингу панелі
    
    def update_screen_size(self, width, height):
        """
        Оновлення розмірів екрану після зміни розміру вікна.
        
        Args:
            width: Нова ширина екрану
            height: Нова висота екрану
        """
        self.width = width
        self.height = height
        
        # Оновлення позицій кнопок
        self.achievements_button_rect = pygame.Rect(self.width - BUTTON_WIDTH - 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    def render(self, left_clicks, right_clicks, total_clicks, achievements):
        """
        Рендеринг усіх елементів інтерфейсу.
        
        Args:
            left_clicks: Кількість лівих кліків
            right_clicks: Кількість правих кліків
            total_clicks: Загальна кількість кліків
            achievements: Об'єкт системи досягнень
        """
        self.draw_score(left_clicks, right_clicks, total_clicks)
        self.draw_progress_bar(total_clicks, achievements.achievements)
        self.draw_help_text()
        self.draw_buttons()
    
    def draw_score(self, left_clicks, right_clicks, total_clicks):
        """
        Рендеринг рахунку кліків.
        
        Args:
            left_clicks: Кількість лівих кліків
            right_clicks: Кількість правих кліків
            total_clicks: Загальна кількість кліків
        """
        # Рядок із загальною статистикою
        stats_text = self.font.render(
            f"{self.language_manager.get_text('left_clicks')}: {left_clicks} | {self.language_manager.get_text('right_clicks')}: {right_clicks} | {self.language_manager.get_text('total')}: {total_clicks}", 
            True, 
            TEXT_COLOR
        )
        self.screen.blit(stats_text, (10, 10))
    
    def draw_progress_bar(self, total_clicks, achievements):
        """
        Рендеринг прогрес-бару до наступного досягнення.
        
        Args:
            total_clicks: Загальна кількість кліків
            achievements: Список досягнень
        """
        # Знаходимо наступне досягнення
        next_milestone = 10
        next_achievement_name = ""
        for achievement in achievements:
            if not achievement["achieved"]:
                next_milestone = achievement["threshold"]
                next_achievement_name = achievement["name"]
                break
        
        # Якщо пройдено всі досягнення, показуємо прогрес до "наступних 100 кліків"
        if total_clicks >= achievements[-1]["threshold"]:
            current_hundred = (total_clicks // 100) * 100
            next_milestone = current_hundred + 100
        
        # Обчислюємо прогрес до наступного досягнення
        if next_milestone > 0:
            if total_clicks >= next_milestone:
                progress = 1.0
            else:
                # Для плавності використовуємо прогрес від останнього досягнення
                last_milestone = 0
                for achievement in achievements:
                    if achievement["threshold"] < next_milestone and achievement["threshold"] > last_milestone:
                        last_milestone = achievement["threshold"]
                
                total_range = next_milestone - last_milestone
                current_progress = total_clicks - last_milestone
                progress = current_progress / total_range
        else:
            progress = 1.0
        
        # Малюємо прогрес-бар
        pygame.draw.rect(
            self.screen, 
            PROGRESS_BAR_BG_COLOR, 
            (10, 40, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT)
        )
        
        pygame.draw.rect(
            self.screen, 
            PROGRESS_BAR_FILL_COLOR, 
            (10, 40, int(PROGRESS_BAR_WIDTH * progress), PROGRESS_BAR_HEIGHT)
        )
        
        # Текст із прогресом
        progress_text = self.font.render(
            f"{total_clicks}/{next_milestone}", 
            True, 
            TEXT_COLOR
        )
        self.screen.blit(progress_text, (PROGRESS_BAR_WIDTH + 20, 40))
        
        # Додаємо назву наступного досягнення, якщо воно є
        if next_achievement_name:
            next_achievement_text = self.small_font.render(
                next_achievement_name, 
                True, 
                TEXT_COLOR
            )
            self.screen.blit(next_achievement_text, (10, PROGRESS_BAR_HEIGHT + 45))
    
    def draw_help_text(self):
        """Рендеринг тексту з підказками."""
        help_text = self.font.render(
            self.language_manager.get_text("help_text"), 
            True, 
            TEXT_COLOR
        )
        self.screen.blit(
            help_text, 
            (self.width // 2 - help_text.get_width() // 2, self.height - 30)
        )
    
    def draw_buttons(self):
        """Рендеринг кнопок інтерфейсу."""
        # Кнопка досягнень
        pygame.draw.rect(
            self.screen,
            BUTTON_COLOR,
            self.achievements_button_rect
        )
        achievements_text = self.font.render(
            self.language_manager.get_text("achievements_button"),
            True,
            BUTTON_TEXT_COLOR
        )
        self.screen.blit(
            achievements_text,
            (self.achievements_button_rect.centerx - achievements_text.get_width() // 2,
             self.achievements_button_rect.centery - achievements_text.get_height() // 2)
        )
    
    def render_achievements_panel(self, achievements, total_clicks):
        """
        Рендеринг панелі зі списком досягнень.
        
        Args:
            achievements: Список досягнень
            total_clicks: Загальна кількість кліків
        """
        # Створюємо напівпрозору панель на весь екран
        panel_surface = pygame.Surface((self.width, self.height))
        panel_surface.fill((0, 0, 0))
        panel_surface.set_alpha(200)  # Напівпрозорість
        self.screen.blit(panel_surface, (0, 0))
        
        # Вікно досягнень
        panel_width = min(self.width - 100, 600)
        panel_height = min(self.height - 100, 400)
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height) // 2
        
        pygame.draw.rect(
            self.screen,
            ACHIEVEMENTS_BG_COLOR,
            (panel_x, panel_y, panel_width, panel_height)
        )
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),  # Світло-сірий обідок
            (panel_x, panel_y, panel_width, panel_height),
            2  # Товщина обідка
        )
        
        # Заголовок
        title_text = self.large_font.render(
            self.language_manager.get_text("achievements_title"),
            True,
            ACHIEVEMENT_COLOR
        )
        self.screen.blit(
            title_text,
            (panel_x + (panel_width - title_text.get_width()) // 2, panel_y + 20)
        )
        
        # Список досягнень
        unlocked_achievements = [a for a in achievements if a["achieved"]]
        if not unlocked_achievements:
            # Якщо немає розблокованих досягнень
            no_achievements_text = self.font.render(
                self.language_manager.get_text("no_achievements"),
                True,
                TEXT_COLOR
            )
            self.screen.blit(
                no_achievements_text,
                (panel_x + (panel_width - no_achievements_text.get_width()) // 2, 
                 panel_y + panel_height // 2 - no_achievements_text.get_height() // 2)
            )
        else:
            # Виводимо список розблокованих досягнень
            y_offset = panel_y + 70
            for achievement in unlocked_achievements:
                achievement_text = self.font.render(
                    achievement["name"],
                    True,
                    ACHIEVEMENT_COLOR
                )
                self.screen.blit(achievement_text, (panel_x + 20, y_offset))
                y_offset += 30
            
            # Виводимо заблоковані досягнення
            y_offset += 20  # Додатковий відступ
            for achievement in achievements:
                if not achievement["achieved"]:
                    # Використовуємо текст для заблокованого досягнення
                    locked_text = self.small_font.render(
                        self.language_manager.get_text("locked_achievement").format(achievement["threshold"]),
                        True,
                        (150, 150, 150)  # Сірий колір для заблокованих
                    )
                    self.screen.blit(locked_text, (panel_x + 20, y_offset))
                    y_offset += 25
        
        # Кнопка "Закрити"
        self.close_button_rect = pygame.Rect(
            panel_x + panel_width - BUTTON_WIDTH - 10,
            panel_y + panel_height - BUTTON_HEIGHT - 10,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        pygame.draw.rect(
            self.screen,
            BUTTON_COLOR,
            self.close_button_rect
        )
        close_text = self.font.render(
            self.language_manager.get_text("close_button"),
            True,
            BUTTON_TEXT_COLOR
        )
        self.screen.blit(
            close_text,
            (self.close_button_rect.centerx - close_text.get_width() // 2,
             self.close_button_rect.centery - close_text.get_height() // 2)
        )