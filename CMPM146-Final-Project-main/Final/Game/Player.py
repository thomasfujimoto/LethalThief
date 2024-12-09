#Code for player 
import random

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.prev = " "    
        
    def set_rnd_cord(self, board_size): 
        self.x = random.randint(0, board_size)
        self.y = random.randint(0, board_size)
    
    # checks to see if player is moving into an open space
    def check_space(self, state, Player_x, Player_y): 
        Board = state.Board.board
        invalid_values = {' ', '┋', 'K', 'T', '┉'}
        
        # Check invalid characters
        if Board[Player_y][Player_x] not in invalid_values:
            return True
        
        elif  Board[Player_y][Player_x] == '┋' and state.numKeys < 1 or Board[Player_y][Player_x] == '┉' and state.numKeys < 1:
            print("You need a key to enter")
            return True
            
        else: 
            return False
         
    # moves player based on player input
    def move_player(self, state, player_input): 
        Board = state.Board.board
        
        # player movement 
        if player_input == 'w' or player_input == 'W':
            if self.check_space(state, self.x, self.y-1):
                print("Cannot Move Up")
            
            else: 
                print("Moving Up")
                # Replace current player position with a space
                if self.prev == 'K' or self.prev=="T":
                    Board[self.y][self.x] = " " 
                    
                elif self.prev == "┉": 
                    Board[self.y][self.x] = " " 
                    state.numKeys -= 11

                else: 
                    Board[self.y][self.x] = self.prev
                
                # Place player at new position
                self.prev =  Board[self.y - 1][self.x]
                
                Board[self.y - 1][self.x] = 'P'
                
                # Update player cordinates 
                self.y -= 1
            
        # moves player down
        elif player_input == 's' or player_input == 'S': 
            if self.check_space(state, self.x, self.y+1):
                print("Cannot Move Down")
            
            else:
                print("Moving Down") 
                
                # Replace current player position with a space
                if self.prev == 'K' or self.prev=="T":
                    Board[self.y][self.x] = " "
                    
                elif self.prev == "┉": 
                    Board[self.y][self.x] = " " 
                    state.numKeys -= 1
                    
                else: 
                    Board[self.y][self.x] = self.prev
                    
                # Place player at new position 
                self.prev =  Board[self.y + 1][self.x]
                Board[self.y + 1][self.x] = 'P'
                
                # Update player cordinates 
                self.y += 1
        
        # move player to the right
        elif player_input == 'd' or player_input == 'D':
            if self.check_space(state, self.x+1, self.y):
                print("Cannot Move Right")
            
            else: 
                print("Moving to the Right") 
                    
                # Replace current player position with a space
                if self.prev == 'K' or self.prev=="T":
                    Board[self.y][self.x] = " "
                    
                elif self.prev == "┋": 
                    Board[self.y][self.x] = " " 
                    state.numKeys -= 1
                    
                else: 
                    Board[self.y][self.x] = self.prev
                
                # Place player at new position 
                self.prev =  Board[self.y][self.x+1]
                Board[self.y][self.x + 1] = 'P'
                
                # Update player cordinates 
                self.x += 1
                
        elif player_input == 'a' or player_input == 'A': 
            if self.check_space(state, self.x-1, self.y):
                print("Cannot Move Left")
            
            else: 
                print("Moving to the left") 
                
                # Replace current player position with a space if its not a key
                if self.prev == 'K' or self.prev=="T":
                    Board[self.y][self.x] = " "
                    
                elif self.prev == "┋": 
                    Board[self.y][self.x] = " " 
                    state.numKeys -= 1
                    
                else: 
                    Board[self.y][self.x] = self.prev
                
                # Place player at new position 
                self.prev =  Board[self.y][self.x-1]
                Board[self.y][self.x - 1] = 'P'
                
                # Update player cordinates 
                self.x -= 1
            
        else: 
            print("Please enter a valid character")
        
        return 
    
    def check_for_keys(self, state): 
        #  Get current key 
        keys = state.Board.keys 
        
        # check to see if the keys and players cordinates match
        for key in keys: 
            
            # keys and player have teh same cordinates
            if key[0] == self.x and key[1] == self.y: 
                print("You Got a key!")
                
                # update the key count 
                state.numKeys += 1
                    
                # remove key from list 
                keys.remove(key)
        
        return

    def check_for_treasure(self, state): 
        #  Get current key 
        treasure = state.Board.treasure 
        
        # check to see if the treasure and players cordinates match
        for t in treasure: 
            
            # treasure and player have teh same cordinates
            if t[0] == self.x and t[1] == self.y: 
                print("You Picked Up Treasure!")
                
                # update the score
                state.score += 1
                     
                # remove treasure from list 
                treasure.remove(t)
        
        return
        
                
        
    
