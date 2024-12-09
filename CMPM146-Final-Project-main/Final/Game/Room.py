# Code for Room Generation
from Enemy_Tree.Enemy import Enemy

# Room Class
class Room:
    # initialize useful variables
    def __init__(self):
        # Room size
        self.size = 45
        self.board = [[' ' for _ in range(84)] for _ in range(self.size)]
        
        # add x y key locatoin to this list 
        self.keys = []
        # add x y treasure locatoin to this list 
        self.treasure = []
        
    # Get the Board from the txt file 
    def read_board(self, state): 
        
        with open('Final_Room.txt', 'r', encoding='utf-8') as file:
            
            # index for line in file
            i = 0
            for line in file:
                for j in range(len(line) - 1):
                    
                    # set the board
                    self.board[i][j] = line[j]
                        
                    # if Player is found mark player location 
                    if line[j] == 'P':
                        state.Player.y = i 
                        state.Player.x = j
                        
                    # elif Enemny is found create a new class and add to enemy list 
                    elif line[j] == 'E':
                        new_enemy = Enemy(i, j, state)
                        state.Enemies.append(new_enemy)
                    
                    # elif key is found 
                    elif line[j] == 'K':
                        new_key = [j, i] 
                        self.keys.append(new_key)

                    #if its a treasure item
                    elif line[j] == 'T':
                        new_treasure = [j, i] 
                        self.treasure.append(new_treasure)


                        
                # increment index
                i += 1
                   
        print('\n') 
    
    # displays the game board
    def display(self):
        
        print("Game Board:")
                    
        for i in range(len(self.board) - 1): 
            line = ''.join(self.board[i])
            print(line)
        
    
        return 
    
    
    