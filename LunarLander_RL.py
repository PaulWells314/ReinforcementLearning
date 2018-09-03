import numpy as np

NUM_POS     = 16   # 0 = ground  16 = maximum altitude
NUM_VEL     = 32   
NUM_ACTIONS = 2     # 0 = no action (gravity only)  1 = Thrust
ZERO_VEL    = 16    # V > ZERO_VEL is up
NUM_STEPS   = 128
NUM_TRIALS  = 32
DELTA       = 1

def next_state(pos, vel, action):
    next_pos = pos + (vel - ZERO_VEL) * DELTA
    if next_pos >= NUM_POS:
        return (pos, vel)
    if action == 1:
        acc = 2
    else:
        acc = -1
    next_vel = vel + acc * DELTA
    if next_vel >= NUM_VEL:
        next_vel = NUM_VEL - 1
    return (next_pos, next_vel)
    
    
def dumpV(V):
        for pos in range(NUM_POS):
            for vel in range(NUM_VEL):
                if V[pos,vel] != 0.0:
                    print("pos ", pos, " vel ", vel, " V ", V[pos,vel])
                    
def main():

    V = np.zeros( (NUM_POS, NUM_VEL) )
    VTemp = np.zeros( (NUM_POS, NUM_VEL) )
    R = np.zeros( (NUM_POS, NUM_VEL) )

    
   
    R[1:, :] =  0
   
    
    # Land as softly as possible
    for v in range(NUM_VEL):
        R[0, v] = 5 * (v - ZERO_VEL)
    
    for epoch in range(NUM_TRIALS):
        pos = NUM_POS -1
        vel = ZERO_VEL
        
        for pos in range(NUM_POS):
            for vel in range(NUM_VEL):
                best_V = -10000
                best_action = 0
                best_pos =    pos
                best_vel =    vel
                
                for j in range(NUM_ACTIONS):
                    test_pos, test_vel = next_state(pos, vel, j)
                    if V[test_pos, test_vel] > best_V:     
                        best_action = j
                        best_vel = test_vel
                        best_pos = test_pos
                        best_V = V[test_pos, test_vel]
                   
                        
                VTemp[pos, vel] = R[pos, vel] + 0.9 * best_V
        V = VTemp
        #print("iteration ", epoch) 
        #dumpV(V)
        #print("")
        
    # Best path from given position
    pos = 15
    vel = ZERO_VEL
    best_V = -10000
    while (pos > 0):
        for j in range(NUM_ACTIONS):
            test_pos, test_vel = next_state(pos, vel, j)
            if V[test_pos, test_vel] > best_V:     
                best_action = j
                best_vel = test_vel
                best_pos = test_pos
                best_V = V[test_pos, test_vel]
                        
        pos = best_pos
        vel = best_vel
        print("pos ", pos, "vel ", vel, "action ", best_action)
        

main()
