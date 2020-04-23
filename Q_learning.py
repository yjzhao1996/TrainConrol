import gym
import numpy as np
import math
import random
from collections import defaultdict
import time


Q=defaultdict(float)
gamma=1 #dicount factor
alpha=0.5 #soft update param
n_steps=100000000
epsilon=0.1

env=gym.make('gym_train:train-v1')

actions=[]

for b in range(1, 11):
    for a in range(0, b):
        actions.append(tuple([a,b,True]))
        actions.append(tuple([a,b,False]))

def update_Q(s, r, a, s_next, done):
    max_q_next = max([Q[s_next, a] for a in actions])
    # Do not include the next state's value if currently at the terminal state.
    Q[s, a] += alpha * (r + gamma * max_q_next * (1.0 - done) - Q[s, a])

def act(ob):
    # Pick the action with highest q value.
    qvals = {tuple(a): Q[ob, a] for a in actions}
    max_q = max(qvals.values())
    # In case multiple actions have the same maximum q value.
    actions_with_max_q = [a for a, q in qvals.items() if q == max_q]
    length=len(actions_with_max_q)
    index=random.randrange(0,length,1)
    return actions_with_max_q[index]

ob=env.reset()
#rewards=[]
#reward=0.0
#print(Q[tuple(ob),tuple([7,8,True])])

start_time = time.time()

for step in range(n_steps):
    a = act(tuple(ob))
    ob_next, r, done, end = env.step(a)
    update_Q(tuple(ob), r, a, tuple(ob_next), done)
    #reward += r
    if done:
        #rewards.append(reward)
        #reward = 0.0
        ob = env.reset()
        if end:
            print(step)
            break
    else:
        ob = ob_next

print("--- %s seconds ---" % (time.time() - start_time))
