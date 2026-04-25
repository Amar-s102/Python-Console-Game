import os
import random
import colorama
from colorama import Fore, Style

colorama.init()

class Game:
    def __init__(self):
        self.grid_size = 20
        self.player_pos = [10, 10]
        self.health = 100
        self.enemies = []
        self.goal = (19, 19)
        self.score = 0
        self.difficulty = 1  # 1 = easy, 2 = medium, 3 = hard
        self.debug_mode = False
    
    def create_enemies(self):
        for _ in range(self.difficulty * 2):
            enemy_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            while enemy_pos == self.player_pos or enemy_pos in self.enemies:
                enemy_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            self.enemies.append(enemy_pos)
    
    def display_grid(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if [i, j] == self.player_pos:
                    print(Fore.GREEN + 'P', end='')  # Player
                elif [i, j] in self.enemies:
                    print(Fore.RED + 'E', end='')  # Enemies
                elif (i, j) == self.goal:
                    print(Fore.YELLOW + 'G', end='')  # Goal
                else:
                    print('.', end='')
            print(Style.RESET_ALL)
        print(f'Health: {self.health}')
        print(f'Score: {self.score}')
    
    def move_player(self, direction):
        if direction == 'w':
            self.player_pos[0] = max(0, self.player_pos[0] - 1)
        elif direction == 's':
            self.player_pos[0] = min(self.grid_size - 1, self.player_pos[0] + 1)
        elif direction == 'a':
            self.player_pos[1] = max(0, self.player_pos[1] - 1)
        elif direction == 'd':
            self.player_pos[1] = min(self.grid_size - 1, self.player_pos[1] + 1)
        self.check_collisions()
    
    def check_collisions(self):
        if self.player_pos in self.enemies:
            self.health -= 10
            if self.debug_mode:
                print('Hit by enemy! Health decreased. Current Health:', self.health)
        if self.health <= 0:
            print('Game Over!')
            exit()  
        if tuple(self.player_pos) == self.goal:
            self.score += 10
            print('Goal reached! Score:', self.score)
            self.reset_game()
    
    def reset_game(self):
        self.player_pos = [10, 10]
        self.health = 100
        self.create_enemies()

    def run(self):
        self.create_enemies()
        while True:
            self.display_grid()
            move = input('Move (W/A/S/D): ').lower()
            if move in ['w', 'a', 's', 'd']:
                self.move_player(move)
            else:
                print('Invalid move!') 

if __name__ == '__main__':
    game = Game()
    game.run()