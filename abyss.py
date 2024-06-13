# main.py

import pygame
from src.gameplay.game import Game
from src.gameplay.menu import MainMenu

def main():
    pygame.init()

    width, height = 800, 600
    fps = 60
    menu = MainMenu(width, height)

    while menu.running:
        action = menu.run()
        if action == "play":
            game = Game(width, height, fps)
            game.run()
        elif action == "quit":
            menu.running = False

    pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()
