#Code for enemy 
import heapq
import random
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Enemy_Tree.Checks import *
from Enemy_Tree.Behaviors import *
from Enemy_Tree.Et_nodes import Selector, Sequence, Action, Check

############################### Main Enemy Class ##################################
class Enemy:
    
    def __init__(self, i, j, state):
        self.x = j
        self.y = i
        self.size_x = 84
        self.size_y = 40
        self.state = state
        self.prev = " "
        self.nearest_key = []
        self.behavior_tree = self.setup_behavior_tree()

    #sets x and y to be random values within the room
    def set_rnd_cord(self): 
        self.x = random.randint(0, self.room.size - 1)
        self.y = random.randint(0, self.room.size - 1)

    #helper function for A*
    def heuristic(self, x1, y1, x2, y2):
        
        # Manhattan distance
        return abs(x1 - x2) + abs(y1 - y2)
    
    #helper function for A*
    def get_neighbors(self, x, y, state):
        neighbors = []
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < self.size_x and 0 <= ny < self.size_y and (state.Board.board[ny][nx]!="║" and state.Board.board[ny][nx]!="X" and state.Board.board[ny][nx]!="═" and state.Board.board[ny][nx]!="┋" and state.Board.board[ny][nx]!="┉" and state.Board.board[ny][nx] !="K"):
                neighbors.append((nx, ny))  

        return neighbors
    
    #implementation of A* to make a path from enemy to Enemy
    def a_star(self, start_x, start_y, goal_x, goal_y, state):
        open_list = []
        heapq.heappush(open_list, (0, start_x, start_y, 0, None))  # (f, x, y, g, parent)
        closed_set = set()
        came_from = {}
        
        while open_list:
            f, x, y, g, parent = heapq.heappop(open_list)
            if (x, y) in closed_set:
                continue
            
            came_from[(x, y)] = parent
            closed_set.add((x, y))
            
            if (x, y) == (goal_x, goal_y):
                # Reconstruct path
                path = []
                
                while came_from[(x, y)] is not None:
                    path.append((x, y))
                    (x, y) = came_from[(x, y)]
                    
                # Return reversed path    
                return path[::-1]  
            
            for nx, ny in self.get_neighbors(x, y, state):
                if (nx, ny) in closed_set:
                    continue
                
                g_new = g + 1
                h_new = self.heuristic(nx, ny, goal_x, goal_y)
                f_new = g_new + h_new
                
                heapq.heappush(open_list, (f_new, nx, ny, g_new, (x, y)))
                
        # No path found 
        return [] 
  
######################################## Enemy Behavior Tree ##################################
    
    # moves player based on Bot inputd
    def setup_behavior_tree(self):
        # Top-down construction of behavior tree
        root = Selector(name='High Level Ordering of Strategies')
        
        # Move towards the player if near
        move_plan = Sequence(name="Move To Player If Near")
        check_distance = Check(self.distance_to_player, name="Check Distance to Player")
        move_enemy = Action(self.chase_player, name="Move to Player")
        move_plan.child_nodes = [check_distance, move_enemy]
        
        # Move towards a key if far away 
        move_key = Sequence(name="Move Towards Key If Near")
        check_key_distance = Check(self.distance_to_key, name="Check Distance to Key")
        move_to_key = Action(self.chase_player, name="Move to Player")
        move_key.child_nodes = [check_key_distance, move_to_key]
        
        # Move around randomly if the player is not near
        move_randomly = Sequence(name="Move Around Randomly")
        move_enemy_rnd = Action(self.move_enemy_randomly, name="Move Randomly")
        move_randomly.child_nodes = [move_enemy_rnd]
        
        # Construct tree
        root.child_nodes = [move_plan, move_key, move_randomly]

        logging.info('\n' + root.tree_to_string())
        return root
    
    # update the behavdior tree
    def update(self, game_state):
        # Execute the behavior tree for this enemy
        self.behavior_tree.execute(game_state)
        
################################# Behavior Tree Check Functions ##################################   
    # Finds distance to player, return True if witihin x blocks 
    def distance_to_player(self, state): 

        # Get current player and enemy cordinates
        Player_x = state.Player.x 
        Player_y = state.Player.y 
        Enemy_x = self.x 
        Enemy_y = self.y
        
        # Close to Enemy
        close_to_enemy = 3.5
        
        # Get distance between player and enemy 
        dist = math.sqrt((Player_x - Enemy_x) ** 2 + (Player_y - Enemy_y) ** 2)
        
        # returns True if the player is close to the enemy
        if dist < close_to_enemy: 
            return True

        else: 
            return False

    # Find distance 
    def distance_to_key(self, state): 
        # Get the current room 
        Room = state.Board
        
        # Player Variables 
        Player_x = state.Player.x 
        Player_y = state.Player.y 

        # Get cordinates of key
        for key in Room.keys: 
            dist = math.sqrt((key[0] - Player_x) ** 2 + (key[1] - Player_y) ** 2)
            
            #  if key is far away from the key then move towards it 
            if dist > 3.0 and dist < 5.0 : 
                self.nearest_key = key
                return True 
            
        return False
        
    
###################################### Behavior Tree Behavior Functions ##################################

    #function to call to make the enemy travel directly towards the player
    def chase_player(self, state): 
        
        Player_x = state.Player.x
        Player_y = state.Player.y
         
        path = self.a_star(self.x, self.y, Player_x, Player_y, state)
        
        #return false if there isnt a path from enemy to player
        if not path:
            return False
        
        if path and len(path) > 1:
            state.Board.board[self.y][self.x]=" "
            self.x, self.y = path[0]  # Move to the next step in the path
            state.Board.board[self.y][self.x]="E"
            return True
        
    def chase_key(self, state): 
        Key_x = state.Player.x
        Key_y = state.Player.y
         
        path = self.a_star(self.x, self.y, Key_x, Key_y, state)
        
        #return false if there isnt a path from key to player
        if not path:
            return False
        
        if path and len(path) > 1:
            state.Board.board[self.y][self.x]=" "
            self.x, self.y = path[0]  # Move to the next step in the path
            state.Board.board[self.y][self.x]="E"
            return True
        

    def move_enemy_randomly(self, state):
        # Choose random input
        random_letter = random.choice(['W', 'A', 'S', 'D'])
        
        Board = state.Board.board
        
    
        # Enemy movement 
        if random_letter == 'w' or random_letter == 'W':
            if Board[self.y - 1][self.x] != ' ':
                print("Cannot Move Up")
            
            else: 
                # Replace current Enemy position with a space
                Board[self.y][self.x] = self.prev
                
                # Place Enemy at new position
                self.prev =  Board[self.y - 1][self.x]
                Board[self.y - 1][self.x] = 'E'
                
                # Update Enemy cordinates 
                self.y -= 1
            
        # moves Enemy down
        elif random_letter == 's' or random_letter == 'S': 
            if Board[self.y + 1][self.x] != ' ':
                print("Cannot Move Down")
            
            else:
                
                # Replace current Enemy position with a space
                Board[self.y][self.x] = self.prev
                
                # Place Enemy at new position 
                self.prev =  Board[self.y + 1][self.x]
                Board[self.y + 1][self.x] = 'E'
                
                # Update Enemy cordinates 
                self.y += 1
        
        # move Enemy to the right
        elif random_letter == 'd' or random_letter == 'D':
            if Board[self.y][self.x + 1] != ' ' :
                print("Cannot Move Right")
            
            else: 
                    
                # Replace current Enemy position with a space
                Board[self.y][self.x] = self.prev
                
                # Place Enemy at new position 
                self.prev =  Board[self.y][self.x + 1]
                Board[self.y][self.x + 1] = 'E'
                
                # Update Enemy cordinates 
                self.x += 1
                
        elif random_letter == 'a' or random_letter == 'A': 
            if Board[self.y][self.x - 1] != ' ':
                print("Cannot Move Left")
            
            else: 
                # Replace current Enemy position with a space
                Board[self.y][self.x] = self.prev
                
                # Place Enemy at new position 
                self.prev =  Board[self.y][self.x-1]
                Board[self.y][self.x - 1] = 'E'
                
                # Update  cordinates 
                self.x -= 1
            
        else: 
            print("Please enter a valid character")
        
        return True