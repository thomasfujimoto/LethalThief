import time
import sys
import threading
import logging
import os

# Imports (assuming these are available)
from Room import Room
from Player import Player 
from Enemy_Tree.Enemy import Enemy
from Enemy_Tree.Et_bot import *

title_screen = r""" 
         /$$                   /$$     /$$                 /$$       /$$$$$$$$ /$$       /$$            /$$$$$$ 
        | $$                  | $$    | $$                | $$      |__  $$__/| $$      |__/           /$$__  $$
        | $$        /$$$$$$  /$$$$$$  | $$$$$$$   /$$$$$$ | $$         | $$   | $$$$$$$  /$$  /$$$$$$ | $$  \__/
        | $$       /$$__  $$|_  $$_/  | $$__  $$ |____  $$| $$         | $$   | $$__  $$| $$ /$$__  $$| $$$$    
        | $$      | $$$$$$$$  | $$    | $$  \ $$  /$$$$$$$| $$         | $$   | $$  \ $$| $$| $$$$$$$$| $$_/    
        | $$      | $$_____/  | $$ /$$| $$  | $$ /$$__  $$| $$         | $$   | $$  | $$| $$| $$_____/| $$      
        | $$$$$$$$|  $$$$$$$  |  $$$$/| $$  | $$|  $$$$$$$| $$         | $$   | $$  | $$| $$|  $$$$$$$| $$      
        |________/ \_______/   \___/  |__/  |__/ \_______/|__/         |__/   |__/  |__/|__/ \_______/|__/      
                                                                                                        
                                                                                                        
    """ 

Game_over = r"""
        /$$$$$$                                           /$$$$$$                                            /$$$
       /$$__  $$                                         /$$__  $$                                          /$$_/
      | $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$       | $$  \ $$ /$$    /$$ /$$$$$$   /$$$$$$        /$$ /$$/  
      | $$ /$$$$ |____  $$| $$_  $$_  $$ /$$__  $$      | $$  | $$|  $$  /$$//$$__  $$ /$$__  $$      |__/| $$   
      | $$|_  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$      | $$  | $$ \  $$/$$/| $$$$$$$$| $$  \__/          | $$   
      | $$  \ $$ /$$__  $$| $$ | $$ | $$| $$_____/      | $$  | $$  \  $$$/ | $$_____/| $$             /$$|  $$  
      |  $$$$$$/|  $$$$$$$| $$ | $$ | $$|  $$$$$$$      |  $$$$$$/   \  $/  |  $$$$$$$| $$            |__/ \  $$$
       \______/  \_______/|__/ |__/ |__/ \_______/       \______/     \_/    \_______/|__/                  \___/
                                                                                                           
                                                                                                           
                                                                                                           
"""

Escaped = r"""
    /$$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$           /$$$  
    | $$_____/ /$$__  $$ /$$__  $$ /$$__  $$| $$__  $$| $$_____/| $$__  $$         |_  $$ 
    | $$      | $$  \__/| $$  \__/| $$  \ $$| $$  \ $$| $$      | $$  \ $$       /$$ \  $$
    | $$$$$   |  $$$$$$ | $$      | $$$$$$$$| $$$$$$$/| $$$$$   | $$  | $$      |__/  | $$
    | $$__/    \____  $$| $$      | $$__  $$| $$____/ | $$__/   | $$  | $$            | $$
    | $$       /$$  \ $$| $$    $$| $$  | $$| $$      | $$      | $$  | $$       /$$  /$$/
    | $$$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$| $$      | $$$$$$$$| $$$$$$$/      |__//$$$/ 
    |________/ \______/  \______/ |__/  |__/|__/      |________/|_______/          |___/  
                                                                                        
"""

# Stores the overall Game State 
class Game: 
    def __init__(self):
        self.Enemies = []
        self.Player = None 
        self.Board = None
        
        # Player Status
        self.Alive = True
        self.score = 0
        self.numKeys = 0
        self.timer_display = ""  # Variable to store the timer display
        self.stop_timer_event = threading.Event()  # Event to signal the timer thread to stop

    # Returns True if the game should end, False Otherwise
    def End_Game(self): 
        for enemy in self.Enemies:
            # Check if the enemy can kill the player
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = self.Player.x + dx, self.Player.y + dy
                
                # If the enemy is within range, the player dies
                if nx == enemy.x and ny == enemy.y or self.Player.x == enemy.x and self.Player.y == enemy.y:
                    self.Board.display()
                    print("You were caught!!")
                    self.Alive = False
                    return True
        return False
    
    # Returns True if player can excape, False Otherwise
    def escape(self): 
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = self.Player.x + dx, self.Player.y + dy
            if self.Board.board[ny][nx]=="X":
                self.Board.display()
                print("You Escaped!!!")
                print("Total number of treasures collected: ", self.score)
                self.Alive = False
                return True
        return False

# Main function (run to play)
if __name__ == "__main__":
    print("\n")

    
    # Display title screen 
    print(title_screen)
    start_text = "                                                Press Enter to START\n \n"
    input(start_text)

    # Display menu screen
    input("\n    Welcome to Lethal Thief! The object of the game to collect as many treasures ('T') as possible.\n\
    Use keys ('K') to open doors ('┋' or '┉') and avoid getting caught by the enemies ('E').\n\
    To move enter either w (UP), a (Left), s (Down), or d (Right) and push enter when finished.\n\
    Press the Enter Key to start the game!!\n")
        
    # Create class for game board 
    Game_State = Game()
    Game_State.Board = Room()
    Game_State.Player = Player()

    Board = Game_State.Board
    User = Game_State.Player
    
    # Print start message 
    print("Starting the Game")
    
    # Get Board Contents from txt file 
    Board.read_board(Game_State)
    
    # Display the board 
    Board.display() 
    
    # Display the player's score
    print("Treasures collected: ", Game_State.score)
    print("Number of keys in inventory: ", Game_State.numKeys)
    
    # Play Game
    try:
        # Debugging information for behavior tree
        logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
        
        # Continue while player is alive
        while Game_State.Alive:
            # Clear the terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            
            
            # Display the board 
            print(title_screen)
            
            Board.display() 

            # Display the player's score
            print("Treasures collected: ", Game_State.score)
            print("Number of keys in inventory: ", Game_State.numKeys)
            print('\n')
            
            player_input = input("Enter either w (UP), a (Left), s (Down), or d (Right) and push enter when finished : \n")
        
            # Update player position
            User.move_player(Game_State, player_input)

            # Update enemy positions
            for enemy in Game_State.Enemies:
                enemy.update(Game_State)
                
            # Check if the end of the game has been reached 
            if Game_State.End_Game(): 
                print(Game_over) 

            if Game_State.escape():
                print(Escaped)
            
            User.check_for_keys(Game_State)
            User.check_for_treasure(Game_State)
            
    except KeyboardInterrupt: 
        print(Game_over)