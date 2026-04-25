import os
import random
import json
import colorama

class Game:
    def __init__(self):
        self.high_score = 0
        self.health = 100
        self.difficulty = 'normal'
        self.debug_mode = False
        self.enemies = []
        self.grid_size = 5
        colorama.init()
        self.load_high_score()

    def load_high_score(self):
        if os.path.exists('high_score.json'):
            with open('high_score.json', 'r') as f:
                data = json.load(f)
                self.high_score = data.get('high_score', 0)

    def save_high_score(self):
        with open('high_score.json', 'w') as f:
            json.dump({'high_score': self.high_score}, f)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        while True:
            self.clear_screen()
            print("=== Main Menu ===")
            print("1. Start Game")
            print("2. Instructions")
            print("3. Show High Score")
            print("4. Choose Difficulty")
            print("5. Debug Mode")
            print("6. Exit")
            choice = input("Select an option: ")
            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.show_instructions()
            elif choice == '3':
                self.show_high_score()
            elif choice == '4':
                self.choose_difficulty()
            elif choice == '5':
                self.ask_debug_mode()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")

    def show_instructions(self):
        print("Instructions: Navigate the player and avoid enemies to achieve the highest score!")
        input("Press Enter to return to main menu...")

    def show_high_score(self):
        print(f"High Score: {self.high_score}")
        input("Press Enter to return to main menu...")

    def choose_difficulty(self):
        print("Choose Difficulty:")
        print("1. Easy")
        print("2. Normal")
        print("3. Hard")
        choice = input("Select an option: ")
        if choice == '1':
            self.difficulty = 'easy'
        elif choice == '2':
            self.difficulty = 'normal'
        elif choice == '3':
            self.difficulty = 'hard'
        else:
            print("Invalid choice! Defaulting to normal.")
            self.difficulty = 'normal'
        input("Press Enter to return to main menu...")

    def ask_debug_mode(self):
        choice = input("Enable debug mode? (y/n): ")
        self.debug_mode = True if choice.lower() == 'y' else False
        input("Press Enter to return to main menu...")

    def create_enemies(self):
        self.enemies = []
        number_of_enemies = {'easy': 2, 'normal': 4, 'hard': 6}[self.difficulty]
        for _ in range(number_of_enemies):
            self.enemies.append({'x': random.randint(0, self.grid_size - 1), 'y': random.randint(0, self.grid_size - 1)})

    def display_grid(self):
        print("Grid:")
        for row in range(self.grid_size):
            line = "|"
            for col in range(self.grid_size):
                if any(enemy['x'] == col and enemy['y'] == row for enemy in self.enemies):
                    line += "E|"
                else:
                    line += " |"
            print(line)
        print(f"Your Health: {self.health}")

    def move_player(self):
        move = input("Move (w/a/s/d): ")
        # Logic for moving player goes here

    def check_game_state(self):
        # Check for enemy collision or goal detection
        for enemy in self.enemies:
            if enemy['x'] == player_x and enemy['y'] == player_y:
                self.health -= 1
                if self.health <= 0:
                    print("Game Over!")
                    return False
        return True

    def play_game(self):
        self.create_enemies()
        while self.health > 0:
            self.display_grid()
            self.move_player()
            if not self.check_game_state():
                break
        self.save_high_score()

    def run(self):
        self.main_menu()

if __name__ == '__main__':
    game = Game()
    game.run()