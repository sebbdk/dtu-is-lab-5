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
slow = False
runai = True
render = False
done = False

# Game clock
clock = pygame.time.Clock()

# INSERT YOUR CODE HERE (1/2)
# Define data structure for q-table

from collections import defaultdict

#def default_value():
#    a = [0,0,0,0]
#   return a

qmap = defaultdict(lambda : [0,0,0,0]) # listen i rækkefølge [N,S,E,W] 
qmap2 = defaultdict(lambda : [0,0,0,0])
actmap = ['up', 'down', 'right', 'left']

count = 0
succescount = 0
expcount = 0

resarr = np.array([])

# END OF YOUR CODE (1/2)
def reset():
    global count
    global succescount
    global qmap
    global qmap2

    count = 0
    succescount = 0
    qmap = defaultdict(lambda : [0,0,0,0])
    qmap2 = defaultdict(lambda : [0,0,0,0])

while not exit_program:
    count += 1
    if render:
        env.render()
    
    # Slow down rendering to 5 fps
    if slow and runai:
        clock.tick(5)
        
    # Automatic reset environment in AI mode
    if done and runai:
        env.reset()
        if done == 2:
            succescount += 1
        if done == 1:
            succescount = 0
        if succescount == 10:
            resarr = np.append(resarr,count)
            if expcount < 100:
                expcount += 1
                reset()
            else:
                print(resarr)
                print(resarr.mean())
                print(resarr.std())
                #normalized_res = (resarr - np.mean(resarr))/np.std(resarr)
                #print(np.abs(normalized_res).mean())
                exit_program = True

            
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
        g = 1
        
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

        # 1. choose an action [N,S,E,W]
        if has_key == False:
            pos = qmap[f"{x}_{y}"]
        else:
            pos = qmap2[f"{x}_{y}"]
        
        pos2 = qmap2[f"{x}_{y}"]

        act = pos.index(max(pos))
        action = actmap[act]

        # 2. step the environment
        (x, y, has_key), reward, done = env.step(action)
        if has_key == False:
            new_pos = qmap[f"{x}_{y}"]
        else:
            new_pos = qmap2[f"{x}_{y}"]
        
        # Q-Learning st.
        Qvalue = reward + g * max(new_pos)
        pos[act] = Qvalue
        if Qvalue == -100:
            pos2[act] = Qvalue

        # 3. update q table

        # END OF YOUR CODE (2/2)
    
    # Human controller        
    else:
        if action_taken:
            (x, y, has_key), reward, done = env.step(action)
            action_taken = False
env.close()
