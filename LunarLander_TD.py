"""
Lunar Lander: An example of Reinforcement Learning by solving Bellman equations.
"""

import numpy as np
from enum import Enum

class Action(Enum):
    ACTION_NONE = 1  # free-fall
    ACTION_BURN = 2  # positve accelertation (up)


NUM_POS         = 20    # 0 = ground  NUM_POS - 1 = maximum altitude
NUM_VEL         = 32  
NUM_ACTIONS     =  2 
ZERO_VEL        = 16    # vel > ZERO_VEL is up
NUM_STEPS       = 128
NUM_TRIALS      = 32
DELTA           = 1
DISCOUNT_FACTOR = 0.9

def get_action_index(action):
    if action == Action.ACTION_NONE:
        return 0
    else:
        if action == Action.ACTION_BURN:
            return 1
        
def generate_r():
    R = np.zeros( (NUM_POS, NUM_VEL) ) 
    R[1:, :] =  0
    
    # Land as softly as possible
    for v in range(NUM_VEL):
        R[0, v] =  5 * (v - ZERO_VEL)
    return R
    
def generate_q():
    q = np.zeros( (NUM_POS, NUM_VEL, NUM_ACTIONS) ) 
    for i in range(NUM_POS):
        for j in range(NUM_VEL):
            for a  in Action:
                q[i, j, get_action_index(a)] = -200
    return q
    
def update_q(s, a, r, q):
    pos = s[0]
    vel = s[1]
    print ("pos ", pos, " vel ", vel, " a ", a)
    if pos < 0 or pos >= NUM_POS:
        return (-1, -1), q
    if pos >= NUM_POS-2 and vel > ZERO_VEL :
         return (-1, -1), q
         
    if pos == 0:
         q[pos, vel, get_action_index(a)] = r[pos, vel]
       
         return (-1, -1), q
   
    next_pos, next_vel = next_state(pos, vel, a)
    if next_pos < 0:
        next_pos = 0
    if next_pos > NUM_POS-1:
        next_pos = NUM_POS-1
       
    print("next_pos ", next_pos, " next_vel ", next_vel)
    max_q = -1000
    a_max = Action.ACTION_NONE
    for a_prime in Action:
        if q[next_pos, next_vel, get_action_index(a_prime)] > max_q:
            a_max = a_prime
            max_q = q[next_pos, next_vel, get_action_index(a_prime)]
   
    q[pos, vel, get_action_index(a)] = r[pos, vel] + q[next_pos, next_vel, get_action_index(a_max) ]
    print("q ", q[s[0], s[1], get_action_index(a)])
    next_s = (next_pos, next_vel)
    return (next_s, q)
    
    
def next_state_action(s, a, q):
    i= np.random.randint(1, 3)
    if i == 1:
        a = Action.ACTION_NONE
    else:
        a = Action.ACTION_BURN
    return a 
    
def next_state(pos, vel, action):
    """ State consists of discretized position and velocity.
    This function generates the next state from the current position, velocity
    and action.
    """
    next_pos = pos + (vel - ZERO_VEL) * DELTA
   
    print("next state action ", action)
    if action == Action.ACTION_BURN:
        acc = 2
        print("Burn")
    else:
        acc = -1
        print("No Burn")
    next_vel = vel + acc * DELTA
   
    return (next_pos, next_vel)
    
def main():

    r = generate_r()
    q = generate_q()
    
    for i in range(1000):
        s = (NUM_POS - 1, ZERO_VEL)
        a = Action.ACTION_NONE
        while s[0] != -1:
            (s, q) = update_q(s, a, r, q)
            a    = next_state_action(s, a, q)
            print("next action ", a)
    for i in range(NUM_POS):
        for j in range(NUM_VEL):
            for a  in Action:
                print(i, j, get_action_index(a), q[i, j, get_action_index(a)])
         
     
main()
