import random

def move_enemy_randomly(state, Bot):
    # Board_size = state.Board.size 
    
    # move = random.choice(['W', 'A', 'S', 'D'])
    # if move == 'W' and Bot.y > 0:
    #     Bot.y -= 1
    # elif move == 'S' and Bot.y < Board_size- 1: # have to give it board state later
    #     Bot.y += 1
    # elif move == 'A' and Bot.x > 0:
    #     Bot.x -= 1
    # elif move == 'D' and Bot.x < Board_size - 1: # have to give it board state later
    #     Bot.x += 1
    return True 

def move_to_player(state, Bot):
    User = state.Player
    
    return Bot.chase_player(User.x, User.y, state)