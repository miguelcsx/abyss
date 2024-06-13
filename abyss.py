# main.py

import os
import csv
import pygame
from src.gameplay.game import Game
from src.gameplay.menu import MainMenu

SCOREBOARD_FILE = 'assets/scoreboard.csv'

def update_scoreboard(name, time, enemies_killed):
    # Check if the directory exists, create if not
    os.makedirs(os.path.dirname(SCOREBOARD_FILE), exist_ok=True)
    
    # Write the data to the CSV file
    with open(SCOREBOARD_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, time, enemies_killed])

def main():
    pygame.init()

    width, height = 800, 600
    fps = 60
    menu = MainMenu(width, height)

    while menu.running:
        action = menu.run()
        if action == "play":
            game = Game(width, height, fps)
            result = game.run()
            if result:  # If the game ends, update scoreboard
                name, time, enemies_killed = result
                update_scoreboard(name, time, enemies_killed)
        elif action == "quit":
            menu.running = False

    pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()
