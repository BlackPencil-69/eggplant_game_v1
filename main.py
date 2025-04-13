#!/usr/bin/env python3

import sys
import os

# Додаємо батьківську директорію до шляху для імпорту модулів
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game

def main():
    """Точка входу в гру."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()