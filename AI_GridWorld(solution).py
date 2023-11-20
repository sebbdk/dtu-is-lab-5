# Grid World: AI-controlled play

# Instructions:
#   Move up, down, left, or right to move the character. The 
#   objective is to find the key and get to the door
#
# Control:
#    arrows  : Merge up, down, left, or right
#    s       : Toggle slow play
#    a       : Toggle AI player
#    d       : Toggle rendering 
#    r       : Restart game
#    q / ESC : Quit

from GridWorld import GridWorld
import numpy as np
import pygame
from collections import defaultdict 

# Initialize the environment
env = GridWorld()
env.reset()
x, y, has_key = env.get_state()

# Definitions and default settings
actions = ['left', 'right', 'up', 'down']
exit_program = False
action_taken = False
slow = True
runai = True
render = True
done = False

# Game clock
clock = pygame.time.Clock()

# INSERT YOUR CODE HERE (1/2)
# Define data structure for q-table
# Here, we will use optimistic initialization and assume all state-actions 
#   have quality 0. This is optimistic, because each step yields reward -1 and 
#   only the key and door give positive rewards (50 and 100)
Q = defaultdict(lambda: [0., 0., 0., 0.])
# END OF YOUR CODE (1/2)
succescount = 0

while not exit_program:
    if render:
        env.render()
    
    # Slow down rendering to 5 fps
    if slow and runai:
        clock.tick(5)
        
    # Automatic reset environment in AI mode
    if done and runai:
        env.reset()
        x, y, has_key = env.get_state()
        
    # Process game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                exit_program = True
            if event.key == pygame.K_UP:
                action, action_taken = 'up', True
            if event.key == pygame.K_DOWN:
                action, action_taken  = 'down', True
            if event.key == pygame.K_RIGHT:
                action, action_taken  = 'right', True
            if event.key == pygame.K_LEFT:
                action, action_taken  = 'left', True
            if event.key == pygame.K_r:
                env.reset()   
            if event.key == pygame.K_d:
                render = not render
            if event.key == pygame.K_s:
                slow = not slow
            if event.key == pygame.K_a:
                runai = not runai
                clock.tick(5)
    
    # AI controller (enable/disable by pressing 'a')
    if runai:
        # INSERT YOUR CODE HERE (2/2)
        #
        # Implement a Grid World AI (q-learning): Control the person by 
        # learning the optimal actions through trial and error
        #
        # The state of the environment is available in the variables
        #    x, y     : Coordinates of the person (integers 0-9)
        #    has_key  : Has key or not (boolean)
        #
        # To take an action in the environment, use the call
        #    (x, y, has_key), reward, done = env.step(action)
        #
        #    This gives you an updated state and reward as well as a Boolean 
        #    done indicating if the game is finished. When the AI is running, 
        #    the game restarts if done=True

        # 1. choose an action
        q_current = Q[(x,y,has_key)]    
        action_num =  np.argmax(q_current)
        action = actions[action_num]  
        # 2. step the environment
        (x, y, has_key), reward, done = env.step(action)
        # 3. update q table
        q_next = Q[(x, y, has_key)]
        q_current[action_num] = reward + np.max(q_next)

        # END OF YOUR CODE (2/2)
    
    # Human controller        
    else:
        if action_taken:
            (x, y, has_key), reward, done = env.step(action)
            action_taken = False


env.close()
