import os
import random
import json
from pathlib import Path
from colorama import Fore, Style, init

init()

class Game:
    def __init__(self):
        self.grid_size = 20
        self.player_pos = [10, 10]
        self.health = 100
        self.max_health = 100
        self.enemies = []
        self.goal = (19, 19)
        self.score = 0
        self.difficulty = "Easy"
        self.difficulty_level = 1
        self.debug_mode = False
        self.move_health_loss = 1
        self.enemy_damage = 5
        self.enemy_count = 2
        self.high_score_file = "highscore.json"
        self.moves = 0
    
    def load_high_score(self):
        try:
            if Path(self.high_score_file).exists():
                with open(self.high_score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            return 0
        return 0
    
    def save_high_score(self, score):
        high_score = self.load_high_score()
        if score > high_score:
            with open(self.high_score_file, 'w') as f:
                json.dump({'high_score': score}, f)
            return True
        return False
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def main_menu(self):
        while True:
            self.clear_screen()
            print(Fore.CYAN + "=" * 40)
            print("PYTHON GRID SURVIVAL GAME")
            print("=" * 40 + Style.RESET_ALL)
            print("1. Start Game")
            print("2. View Instructions")
            print("3. View High Score")
            print("4. Exit")
            print()
            
            choice = input("Choose an option (1-4): ").strip()
            
            if choice == "1":
                return "start"
            elif choice == "2":
                self.show_instructions()
            elif choice == "3":
                self.show_high_score()
            elif choice == "4":
                self.clear_screen()
                print("Thank you for playing!")
                exit()
            else:
                print("Invalid option. Please try again.")
                input("Press Enter to continue...")
    
    def show_instructions(self):
        self.clear_screen()
        print(Fore.CYAN + "INSTRUCTIONS" + Style.RESET_ALL)
        print("-" * 40)
        print("Objective: Reach the goal (G) to win")
        print()
        print("Controls:")
        print("  W - Move Up")
        print("  A - Move Left")
        print("  S - Move Down")
        print("  D - Move Right")
        print()
        print("Game Elements:")
        print(f"  {Fore.GREEN}P{Style.RESET_ALL} = Player")
        print(f"  {Fore.YELLOW}G{Style.RESET_ALL} = Goal")
        print(f"  {Fore.RED}E{Style.RESET_ALL} = Enemy")
        print()
        print("Mechanics:")
        print("  - Each move costs 1 health (or more based on difficulty)")
        print("  - Hitting an enemy costs additional health")
        print("  - Health reaches 0 = Game Over")
        print("  - Reach the goal to win!")
        print()
        input("Press Enter to return to menu...")
    
    def show_high_score(self):
        self.clear_screen()
        high_score = self.load_high_score()
        print(Fore.CYAN + "HIGH SCORE" + Style.RESET_ALL)
        print("-" * 40)
        print(f"Current High Score: {Fore.YELLOW}{high_score}{Style.RESET_ALL}")
        print()
        input("Press Enter to return to menu...")
    
    def choose_difficulty(self):
        self.clear_screen()
        print(Fore.CYAN + "CHOOSE DIFFICULTY" + Style.RESET_ALL)
        print("-" * 40)
        print("1. Easy   (2 enemies, -1 health/move, -5 health/enemy)")
        print("2. Medium (5 enemies, -2 health/move, -10 health/enemy)")
        print("3. Hard   (8 enemies, -3 health/move, -15 health/enemy)")
        print()
        
        choice = input("Choose difficulty (1-3): ").strip()
        
        if choice == "1":
            self.difficulty = "Easy"
            self.difficulty_level = 1
            self.enemy_count = 2
            self.move_health_loss = 1
            self.enemy_damage = 5
        elif choice == "2":
            self.difficulty = "Medium"
            self.difficulty_level = 2
            self.enemy_count = 5
            self.move_health_loss = 2
            self.enemy_damage = 10
        elif choice == "3":
            self.difficulty = "Hard"
            self.difficulty_level = 3
            self.enemy_count = 8
            self.move_health_loss = 3
            self.enemy_damage = 15
        else:
            print("Invalid choice. Defaulting to Easy.")
            self.difficulty = "Easy"
            self.difficulty_level = 1
            self.enemy_count = 2
            self.move_health_loss = 1
            self.enemy_damage = 5
            input("Press Enter to continue...")
    
    def ask_debug_mode(self):
        self.clear_screen()
        print(Fore.CYAN + "DEBUG MODE" + Style.RESET_ALL)
        print("-" * 40)
        print("Debug mode shows enemy positions and additional info.")
        print()
        choice = input("Enable debug mode? (y/n): ").lower().strip()
        self.debug_mode = choice == "y"
    
    def create_enemies(self):
        self.enemies = []
        for _ in range(self.enemy_count):
            enemy_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            while enemy_pos == self.player_pos or enemy_pos in self.enemies or tuple(enemy_pos) == self.goal:
                enemy_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            self.enemies.append(enemy_pos)
    
    def display_grid(self):
        self.clear_screen()
        
        # Display grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if [i, j] == self.player_pos:
                    print(Fore.GREEN + 'P' + Style.RESET_ALL, end=' ')
                elif [i, j] in self.enemies:
                    print(Fore.RED + 'E' + Style.RESET_ALL, end=' ')
                elif (i, j) == self.goal:
                    print(Fore.YELLOW + 'G' + Style.RESET_ALL, end=' ')
                else:
                    print('.', end=' ')
            print()
        
        # Display stats
        print()
        print("-" * 40)
        print(f"Difficulty: {self.difficulty}")
        print(f"Health: {Fore.YELLOW}{self.health}/{self.max_health}{Style.RESET_ALL}")
        print(f"Score: {self.score}")
        print(f"Moves: {self.moves}")
        
        if self.debug_mode:
            print(f"{Fore.CYAN}[DEBUG] Player: {self.player_pos}, Goal: {self.goal}, Enemies: {len(self.enemies)}{Style.RESET_ALL}")
        
        print("-" * 40)
    
    def move_player(self, direction):
        if direction == 'w':
            self.player_pos[0] = max(0, self.player_pos[0] - 1)
        elif direction == 's':
            self.player_pos[0] = min(self.grid_size - 1, self.player_pos[0] + 1)
        elif direction == 'a':
            self.player_pos[1] = max(0, self.player_pos[1] - 1)
        elif direction == 'd':
            self.player_pos[1] = min(self.grid_size - 1, self.player_pos[1] + 1)
        else:
            return False
        
        # Deduct health for movement
        self.health -= self.move_health_loss
        self.moves += 1
        self.score += 10
        
        self.check_collisions()
        return True
    
    def check_collisions(self):
        # Check enemy collision
        if self.player_pos in self.enemies:
            self.health -= self.enemy_damage
            self.score -= 5
            if self.debug_mode:
                print(f"{Fore.RED}Hit by enemy! Lost {self.enemy_damage} health.{Style.RESET_ALL}")
            input("Press Enter to continue...")
        
        # Check goal collision
        if tuple(self.player_pos) == self.goal:
            self.clear_screen()
            print(Fore.GREEN + "=" * 40)
            print("CONGRATULATIONS! YOU REACHED THE GOAL!")
            print("=" * 40 + Style.RESET_ALL)
            print(f"Final Score: {self.score}")
            print(f"Moves Taken: {self.moves}")
            print(f"Health Remaining: {self.health}")
            
            if self.save_high_score(self.score):
                print(Fore.YELLOW + "NEW HIGH SCORE!" + Style.RESET_ALL)
            
            input("\nPress Enter to return to menu...")
            return True
        
        # Check game over
        if self.health <= 0:
            self.clear_screen()
            print(Fore.RED + "=" * 40)
            print("GAME OVER!")
            print("=" * 40 + Style.RESET_ALL)
            print(f"Final Score: {self.score}")
            print(f"Moves Taken: {self.moves}")
            
            input("\nPress Enter to return to menu...")
            return True
        
        return False
    
    def play_game(self):
        self.choose_difficulty()
        self.ask_debug_mode()
        
        # Reset game state
        self.player_pos = [10, 10]
        self.health = self.max_health
        self.score = 0
        self.moves = 0
        self.goal = (19, 19)
        
        self.create_enemies()
        
        game_over = False
        while not game_over:
            self.display_grid()
            move = input("Move (W/A/S/D) or Q to quit: ").lower().strip()
            
            if move == 'q':
                print("Game exited.")
                input("Press Enter to return to menu...")
                break
            elif move in ['w', 'a', 's', 'd']:
                game_over = self.move_player(move)
            else:
                print("Invalid input. Use W, A, S, or D to move.")
                input("Press Enter to continue...")
    
    def run(self):
        while True:
            menu_choice = self.main_menu()
            if menu_choice == "start":
                self.play_game()

if __name__ == '__main__':
    game = Game()
    game.run()