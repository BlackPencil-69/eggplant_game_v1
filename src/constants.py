"""
Константи для гри з баклажаном.
Усі "магічні числа" та фіксовані значення винесені сюди.
"""

# Розміри екрану за замовчуванням
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Кольори (RGB)
BACKGROUND_COLOR = (230, 230, 250)  # Світло-лавандовий
TEXT_COLOR = (0, 0, 0)  # Чорний
TEXT_ANIMATION_COLOR = (255, 255, 255)  # Білий
EGGPLANT_COLOR = (138, 43, 226)  # Фіолетовий (для заглушки)
PROGRESS_BAR_BG_COLOR = (200, 200, 200)  # Світло-сірий
PROGRESS_BAR_FILL_COLOR = (100, 100, 255)  # Синій
ACHIEVEMENT_COLOR = (255, 215, 0)  # Золотистий
PARTICLE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Різні яскраві кольори
BUTTON_COLOR = (100, 100, 255)  # Колір кнопок
BUTTON_HOVER_COLOR = (80, 80, 200)  # Колір кнопок при наведенні
BUTTON_TEXT_COLOR = (255, 255, 255)  # Колір тексту на кнопках
ACHIEVEMENTS_BG_COLOR = (50, 50, 70, 200)  # Колір фону списку досягнень з прозорістю

# Налаштування анімації
FPS = 60  # Кадрів в секунду
CLICK_ANIMATION_SCALE = 1.2  # Максимальний масштаб при кліку
CLICK_ANIMATION_DURATION = 10  # Тривалість анімації кліку в кадрах
TEXT_ANIMATION_DURATION = 30  # Тривалість анімації тексту в кадрах
TEXT_FADE_SPEED = 15  # Швидкість зникнення тексту
PARTICLE_COUNT = 13  # Кількість частинок при кліку
PARTICLE_MAX_SIZE = 7  # Максимальний розмір частинок
PARTICLE_MIN_SIZE = 3  # Мінімальний розмір частинок
PARTICLE_GRAVITY = 0.1  # Симуляція гравітації для частинок

# Налаштування інтерфейсу
FONT_SIZE = 24  # Розмір шрифту за замовчуванням
LARGE_FONT_SIZE = 36  # Розмір великого шрифту
SMALL_FONT_SIZE = 18  # Розмір малого шрифту
ACHIEVEMENT_DISPLAY_TIME = 180  # Час відображення досягнення (в кадрах)
PROGRESS_BAR_WIDTH = 200  # Ширина прогрес-бару
PROGRESS_BAR_HEIGHT = 20  # Висота прогрес-бару
BUTTON_WIDTH = 150  # Ширина кнопок
BUTTON_HEIGHT = 40  # Висота кнопок
ACHIEVEMENT_LIST_PADDING = 10  # Відступи в списку досягнень

# Досягнення
ACHIEVEMENTS = [
    {"name": "Ласкаво просимо до гри", "threshold": 10, "achieved": False},
    {"name": "Початківець", "threshold": 50, "achieved": False},
    {"name": "Ентузіаст", "threshold": 100, "achieved": False},
    {"name": "Досвідчений", "threshold": 500, "achieved": False},
    {"name": "Баклажанний майстер", "threshold": 1000, "achieved": False},
    {"name": "Баклажанний гуру", "threshold": 2000, "achieved": False},
    {"name": "Баклажанний бог", "threshold": 5000, "achieved": False},
    {"name": "Надлюдський рефлекс", "threshold": 10000, "achieved": False},
    {"name": "Нескінченний баклажан", "threshold": 50000, "achieved": False},
    {"name": "Клік-король", "threshold": 100000, "achieved": False},
    {"name": "Легенда баклажанів", "threshold": 1000000, "achieved": False}
]

# Переклади (залишаємо тільки українську мову)
TRANSLATIONS = {
    "uk": {  # Українська
        "left_clicks": "Ліві кліки",
        "right_clicks": "Праві кліки",
        "total": "Всього",
        "help_text": "Клікай на баклажан лівою або правою кнопкою миші!",
        "achievement_unlocked": "Досягнення отримано",
        "achievements_button": "Досягнення",
        "close_button": "Закрити",
        "achievements_title": "Отримані досягнення",
        "no_achievements": "Досягнень поки немає. Продовжуйте клікати!",
        "locked_achievement": "??? (доступно на {})",
        "achievements": [
            {"name": "Ласкаво просимо до гри", "threshold": 10},
            {"name": "Початківець", "threshold": 50},
            {"name": "Ентузіаст", "threshold": 100},
            {"name": "Досвідчений", "threshold": 500},
            {"name": "Баклажанний майстер", "threshold": 1000},
            {"name": "Баклажанний гуру", "threshold": 2000},
            {"name": "Баклажанний бог", "threshold": 5000},
            {"name": "Надлюдський рефлекс", "threshold": 10000},
            {"name": "Нескінченний баклажан", "threshold": 50000},
            {"name": "Клік-король", "threshold": 100000},
            {"name": "Легенда баклажанів", "threshold": 1000000}
        ]
    }
}