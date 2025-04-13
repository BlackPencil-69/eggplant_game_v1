import pygame
import math
import random
from src.constants import *

class AnimationSystem:
    """
    Клас для управління всіма анімаціями в грі.
    """
    def __init__(self, screen, eggplant_image, eggplant_rect):
        """
        Ініціалізація системи анімації.
        
        Args:
            screen: Поверхня для рендерингу
            eggplant_image: Зображення баклажана
            eggplant_rect: Прямокутник із розташуванням баклажана
        """
        self.screen = screen
        self.eggplant_image = eggplant_image
        self.eggplant_rect = eggplant_rect
        
        # Змінні для анімації кліку
        self.click_animation = False
        self.click_timer = 0
        self.click_scale = 1.0
        
        # Змінні для анімації тексту
        self.floating_texts = []
        
        # Частинки
        self.particles = []
        
        # Кеш масштабованих зображень
        self.initialize_scaling_cache()
    
    def initialize_scaling_cache(self):
        """Створює кеш змасштабованих зображень для оптимізації."""
        self.scaled_images = {}
        # Передобчислюємо кілька масштабів для швидкого доступу
        scales = [0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]
        for scale in scales:
            scaled_width = int(self.eggplant_rect.width * scale)
            scaled_height = int(self.eggplant_rect.height * scale)
            self.scaled_images[scale] = pygame.transform.smoothscale(
                self.eggplant_image, (scaled_width, scaled_height))
    
    def get_scaled_image(self, scale):
        """
        Отримує передобчислене змасштабоване зображення.
        
        Args:
            scale: Потрібний масштаб
            
        Returns:
            Змасштабоване зображення
        """
        # Знаходимо найближчий доступний масштаб
        closest_scale = min(self.scaled_images.keys(), 
                          key=lambda x: abs(x - scale))
        return self.scaled_images[closest_scale]
    
    def start_click_animation(self):
        """Запускає анімацію кліку."""
        self.click_animation = True
        self.click_timer = CLICK_ANIMATION_DURATION
        
    def add_floating_text(self, text):
        """
        Додає текст, що з'являється і повільно зникає.
        
        Args:
            text: Текст для відображення
        """
        text_font = pygame.font.Font(None, FONT_SIZE)
        text_surface = text_font.render(text, True, TEXT_ANIMATION_COLOR)
        # Розміщуємо текст над баклажаном з невеликою випадковою варіацією
        x = self.eggplant_rect.centerx - text_surface.get_width() // 2 + random.randint(-20, 20)
        y = self.eggplant_rect.top - 30 + random.randint(-10, 10)
        
        self.floating_texts.append({
            "surface": text_surface,
            "pos": [x, y],
            "timer": TEXT_ANIMATION_DURATION,
            "alpha": 255
        })
    
    def spawn_particles(self, pos, count=PARTICLE_COUNT):
        """
        Створює частинки при кліку.
        
        Args:
            pos: Позиція, де створити частинки
            count: Кількість частинок
        """
        for _ in range(count):
            # Випадковий кут і швидкість
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            # Випадкова тривалість життя та колір
            lifetime = random.randint(20, 40)
            color = random.choice(PARTICLE_COLORS)
            
            self.particles.append({
                "pos": list(pos),
                "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
                "lifetime": lifetime,
                "color": color,
                "size": random.randint(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
            })
    
    def update(self):
        """Оновлення всіх анімацій."""
        # Оновлення анімації кліку
        if self.click_animation:
            # Плавна пульсація при кліку
            progress = 1 - (self.click_timer / CLICK_ANIMATION_DURATION)
            self.click_scale = 1 + (CLICK_ANIMATION_SCALE - 1) * math.sin(progress * math.pi)
            self.click_timer -= 1
            if self.click_timer <= 0:
                self.click_animation = False
                self.click_scale = 1.0
        
        # Оновлення плаваючих текстів
        for text in self.floating_texts[:]:
            text["timer"] -= 1
            text["pos"][1] -= 1  # Рух тексту вгору
            # Поступове зникнення тексту
            if text["timer"] < TEXT_FADE_SPEED:
                text["alpha"] = int(255 * (text["timer"] / TEXT_FADE_SPEED))
            # Видалення тексту, коли час вийшов
            if text["timer"] <= 0:
                self.floating_texts.remove(text)
        
        # Оновлення частинок
        self.update_particles()
    
    def update_particles(self):
        """Оновлення стану частинок."""
        for particle in self.particles[:]:
            particle["lifetime"] -= 1
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)
                continue
                
            # Рух частинок
            particle["pos"][0] += particle["vel"][0]
            particle["pos"][1] += particle["vel"][1]
            # Додавання "гравітації"
            particle["vel"][1] += PARTICLE_GRAVITY
    
    def render(self, center_pos):
        """
        Рендеринг баклажана та всіх анімаційних ефектів.
        
        Args:
            center_pos: Позиція центра баклажана
        """
        # Малювання баклажана з поточним масштабом
        scaled_image = self.get_scaled_image(self.click_scale)
        scaled_rect = scaled_image.get_rect()
        scaled_rect.center = center_pos
        self.screen.blit(scaled_image, scaled_rect)
        
        # Оновлюємо прямокутник баклажана для коректного визначення натискань
        self.eggplant_rect = scaled_rect
        
        # Малювання частинок
        self.render_particles()
        
        # Малювання плаваючих текстів
        self.render_floating_texts()
    
    def render_particles(self):
        """Рендеринг частинок."""
        for particle in self.particles:
            # Прозорість залежить від часу життя
            alpha = 255 * (particle["lifetime"] / 40)
            
            # Створюємо тимчасову поверхню для частинки
            surf = pygame.Surface((particle["size"], particle["size"]))
            surf.fill(particle["color"])
            surf.set_alpha(alpha)
            
            # Малюємо частинку
            self.screen.blit(surf, particle["pos"])
    
    def render_floating_texts(self):
        """Рендеринг плаваючих текстів."""
        for text in self.floating_texts:
            # Створюємо копію з потрібною прозорістю
            text_surface = text["surface"].copy()
            text_surface.set_alpha(text["alpha"])
            
            # Малюємо текст
            self.screen.blit(text_surface, text["pos"])