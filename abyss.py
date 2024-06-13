# main.py

from src.gameplay.game import Game

def main():
    game = Game(800, 600, 60)
    game.run()

if __name__ == "__main__":
    main()
