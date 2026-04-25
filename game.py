    def move_player(self, direction):
        if direction == 'w':
            self.player_pos[0] = max(0, self.player_pos[0] - 1)
        elif direction == 's':
            self.player_pos[0] = min(self.grid_size - 1, self.player_pos[0] + 1)
        elif direction == 'a':
            self.player_pos[1] = max(0, self.player_pos[1] - 1)
        elif direction == 'd':
            self.player_pos[1] = min(self.grid_size - 1, self.player_pos[1] + 1)
        
        # Deduct health for movement
        self.health -= self.move_health_loss
        self.moves += 1
        self.score += 10

    def check_collisions(self):
        # Check enemy collision
        if self.player_pos in self.enemies:
            self.health -= self.enemy_damage
            self.score -= 5
            if self.debug_mode:
                print(f"{Fore.RED}Hit by enemy! Lost {self.enemy_damage} health.{Style.RESET_ALL}")
            input("Press Enter to continue...")
        
        # Check goal collision - WIN
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
        
        # Check game over - LOSE
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
