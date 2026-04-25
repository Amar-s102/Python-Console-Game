import os
import random
import json
import colorama


class Game:
    def __init__(self):
        colorama.init(autoreset=True)

        self.grid_size = 20
        self.health = 100
        self.score = 0
        self.moves = 0
        self.high_score = 0

        self.difficulty = "normal"
        self.debug_mode = False

        self.player_position = None
        self.goal_position = None
        self.enemies = []

        self.load_high_score()

    def load_high_score(self):
        try:
            if os.path.exists("high_score.json"):
                with open("high_score.json", "r") as file:
                    data = json.load(file)
                    self.high_score = data.get("high_score", 0)
        except (json.JSONDecodeError, OSError):
            self.high_score = 0

    def save_high_score(self):
        try:
            with open("high_score.json", "w") as file:
                json.dump({"high_score": self.high_score}, file)
        except OSError:
            print("Could not save high score.")

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("\nPress Enter to continue...")

    def main_menu(self):
        while True:
            self.clear_screen()
            print("=== PYTHON CONSOLE GRID GAME ===")
            print("1. Start Game")
            print("2. Instructions")
            print("3. Show High Score")
            print("4. Choose Difficulty")
            print("5. Toggle Debug Mode")
            print("6. Exit")
            print(f"\nCurrent difficulty: {self.difficulty.title()}")
            print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")

            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                self.play_game()
            elif choice == "2":
                self.show_instructions()
            elif choice == "3":
                self.show_high_score()
            elif choice == "4":
                self.choose_difficulty()
            elif choice == "5":
                self.toggle_debug_mode()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number from 1 to 6.")
                self.pause()

    def show_instructions(self):
        self.clear_screen()
        print("=== INSTRUCTIONS ===")
        print("Move the player P around the 20 x 20 grid.")
        print("Use W to move up, S to move down, A to move left, and D to move right.")
        print("Reach the goal G to win the game.")
        print("Avoid enemies E because touching one removes extra health.")
        print("Each valid move reduces health.")
        print("The game ends when you reach the goal or your health reaches zero.")
        print("Debug mode can hide or show enemies and the goal for testing.")
        self.pause()

    def show_high_score(self):
        self.clear_screen()
        print("=== HIGH SCORE ===")
        print(f"Current high score: {self.high_score}")
        self.pause()

    def choose_difficulty(self):
        self.clear_screen()
        print("=== CHOOSE DIFFICULTY ===")
        print("1. Easy   - 5 enemies, 1 health lost per move, 5 enemy damage")
        print("2. Normal - 8 enemies, 1 health lost per move, 5 enemy damage")
        print("3. Hard   - 12 enemies, 2 health lost per move, 10 enemy damage")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            self.difficulty = "easy"
        elif choice == "2":
            self.difficulty = "normal"
        elif choice == "3":
            self.difficulty = "hard"
        else:
            print("Invalid choice. Difficulty remains unchanged.")
            self.pause()
            return

        print(f"Difficulty set to {self.difficulty.title()}.")
        self.pause()

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        print(f"Debug mode is now {'ON' if self.debug_mode else 'OFF'}.")
        self.pause()

    def get_difficulty_settings(self):
        if self.difficulty == "easy":
            return 5, 1, 5
        if self.difficulty == "hard":
            return 12, 2, 10
        return 8, 1, 5

    def generate_random_position(self, used_positions):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            position = [row, col]

            if position not in used_positions:
                return position

    def setup_game(self):
        self.health = 100
        self.score = 0
        self.moves = 0
        self.enemies = []

        enemy_count, _, _ = self.get_difficulty_settings()
        used_positions = []

        self.player_position = self.generate_random_position(used_positions)
        used_positions.append(self.player_position)

        self.goal_position = self.generate_random_position(used_positions)
        used_positions.append(self.goal_position)

        for _ in range(enemy_count):
            enemy_position = self.generate_random_position(used_positions)
            self.enemies.append(enemy_position)
            used_positions.append(enemy_position)

    def create_grid(self):
        return [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def display_grid(self):
        grid = self.create_grid()

        player_row, player_col = self.player_position
        goal_row, goal_col = self.goal_position

    
        if self.debug_mode:
            grid[goal_row][goal_col] = colorama.Fore.GREEN + "G" + colorama.Style.RESET_ALL

            for enemy in self.enemies:
                enemy_row, enemy_col = enemy
                grid[enemy_row][enemy_col] = colorama.Fore.RED + "E" + colorama.Style.RESET_ALL
        else:
            grid[goal_row][goal_col] = colorama.Fore.GREEN + "G" + colorama.Style.RESET_ALL
            for enemy in self.enemies:
                enemy_row, enemy_col = enemy
                grid[enemy_row][enemy_col] = colorama.Fore.RED + "E" + colorama.Style.RESET_ALL

        grid[player_row][player_col] = colorama.Fore.CYAN + "P" + colorama.Style.RESET_ALL

        print("=== GAME SCREEN ===")
        print(f"Difficulty: {self.difficulty.title()}")
        print(f"Health: {self.health}")
        print(f"Score: {self.score}")
        print(f"Moves: {self.moves}")
        print(f"High Score: {self.high_score}")
        print()

        for row in grid:
            print(" ".join(row))

    def get_new_position(self, move):
        row, col = self.player_position

        if move == "w":
            row -= 1
        elif move == "s":
            row += 1
        elif move == "a":
            col -= 1
        elif move == "d":
            col += 1

        return [row, col]

    def is_inside_grid(self, position):
        row, col = position
        return 0 <= row < self.grid_size and 0 <= col < self.grid_size

    def handle_move(self, move):
        _, move_health_loss, enemy_damage = self.get_difficulty_settings()

        if move not in ["w", "a", "s", "d"]:
            return "Invalid input. Use W, A, S, or D."

        new_position = self.get_new_position(move)

        if not self.is_inside_grid(new_position):
            return "You cannot move outside the grid."

        self.player_position = new_position
        self.health -= move_health_loss
        self.moves += 1
        self.score += 10

        if self.player_position in self.enemies:
            self.health -= enemy_damage
            self.score -= 5
            return f"You hit an enemy and lost {enemy_damage} extra health."

        return ""

    def check_win(self):
        return self.player_position == self.goal_position

    def check_loss(self):
        return self.health <= 0

    def finish_game(self, won):
        self.clear_screen()

        if won:
            bonus = self.health * 2
            self.score += bonus
            print(colorama.Fore.GREEN + "You reached the goal. You win!" + colorama.Style.RESET_ALL)
            print(f"Health bonus added: {bonus}")
        else:
            print(colorama.Fore.RED + "Game Over. Your health reached zero." + colorama.Style.RESET_ALL)

        print(f"Final score: {self.score}")
        print(f"Total moves: {self.moves}")

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            print("New high score saved.")
        else:
            self.save_high_score()

        self.pause()

    def play_game(self):
        self.setup_game()
        message = ""

        while True:
            self.clear_screen()
            self.display_grid()

            if message:
                print("\n" + message)

            move = input("\nMove (W/A/S/D) or Q to quit: ").strip().lower()

            if move == "q":
                print("Game exited.")
                self.pause()
                return

            message = self.handle_move(move)

            if self.check_win():
                self.finish_game(won=True)
                return

            if self.check_loss():
                self.finish_game(won=False)
                return

    def run(self):
        self.main_menu()


if __name__ == "__main__":
    game = Game()
    game.run()
