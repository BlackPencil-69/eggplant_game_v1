from src.constants import TRANSLATIONS

class LanguageManager:
    """
    Клас для управління мовою гри.
    Забезпечує доступ до перекладів всіх текстів.
    """
    def __init__(self):
        """Ініціалізація менеджера з українською мовою."""
        self.current_language = "uk"
        self.translations = TRANSLATIONS
    
    def get_text(self, key):
        """
        Отримує переклад за ключем для української мови.
        
        Args:
            key: Ключ тексту для перекладу
            
        Returns:
            Перекладений текст
        """
        if key in self.translations[self.current_language]:
            return self.translations[self.current_language][key]
        # Якщо ключ не знайдено, повертаємо сам ключ як текст
        return key
    
    def get_achievement_name(self, index):
        """
        Отримує переклад назви досягнення за індексом.
        
        Args:
            index: Індекс досягнення
            
        Returns:
            Перекладена назва досягнення
        """
        if index < len(self.translations[self.current_language]["achievements"]):
            return self.translations[self.current_language]["achievements"][index]["name"]
        return f"Achievement {index}"