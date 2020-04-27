import numpy as np
import matplotlib.pyplot as plt
import random
mass=192

Q = np.load('q_policy.npy',allow_pickle='TRUE').item()

actions=[]

for b in range(1, 11):
    for a in range(0, b):
        actions.append(tuple([a,b,True]))
        actions.append(tuple([a,b,False]))

def act(ob):
    # Pick the action with highest q value.
    qvals = {tuple(a): Q[ob, a] for a in actions}
    max_q = max(qvals.values())
    # In case multiple actions have the same maximum q value.
    actions_with_max_q = [a for a, q in qvals.items() if q == max_q]
    length=len(actions_with_max_q)
    index=random.randrange(0,length,1)
    return actions_with_max_q[index]

i=0
j=0
k=0

iterCnts=0
r=0
g=0
E=0

policy = np.load('policy.npy')
time_list=[]
v_list=[]

ob=np.zeros((3), dtype=int)
ob[0] = 0
ob[1] = 0
ob[2] = 0
F=0

while(1):

    action= act(tuple(ob))

    a = action[0]
    b = action[1]
    brake = action[2]
    v=i

    if j < 15:
        l = j * 10
    elif j < 20:
        l = (j - 15) * 50 + 150
    elif j < 30:
        l = (j - 20) * 100 + 400
    elif j < 38:
        l = (j - 30) * 50 + 1400
    else:
        l = (j - 38) * 10 + 1800

    time=k*5

    time_list.append(time)
    v_list.append(v)

    F=310
    for t in np.arange(0.1,5.1,0.1):
        if l <= 130:
            speed_limit = 53
        elif l <= 1820:
            speed_limit = 80
        else:
            speed_limit = 46

        # traction
        if v <= 36:
            T = 310
        else:
            T = 310 - (v - 36) * 5

        if v <= 60:
            B = 260
        else:
            B = 260 - (v - 60) * 5

        if l <= 470:
            g = 0
        elif l <= 520:
            g = 0.04
        elif l <= 700:
            g = 0.08
        elif l <= 750:
            g = 0
        elif l <= 850:
            g = -0.07
        elif l <= 1020:
            g = -0.12
        elif l <= 1120:
            g = 0
        elif l <= 1400:
            g = 0.02
        elif l <= 1780:
            g = 0.03
        elif l <= 1800:
            g = 0.02
        elif l <= 1820:
            g = 0.01
        else:
            g = 0

        fric = 3.858 * 0.0001 * v * v - 0.064 * v + 2.965

        # v_target-b
        v1 = speed_limit - b
        # v_target-a
        v2 = speed_limit - a

        if v >= v2:
            F = 0
        elif v <= v1:
            F = T

        if brake and (v > 0):
            F = -B

        F_ab=abs(F)
        F_all = F - fric
        ad = F_all / mass + g
        d_l = v / 3.6 * 0.1 + 0.5 * ad * 0.01
        v = v + ad * 0.1 * 3.6
        time = time + 0.1
        time_list.append(time)
        print(time)
        v_list.append(v)
        #print(v)
        #print(F_all)
        r = r - F * d_l
        E=E+d_l*F_ab

        if l >= 1980:
            r = r - abs(135 - time) - v * 1000
            done = True
            break
        """
        if v <= 0:
            # done=True
            r = r - (1980 - l) * 10
            break
        """

    if l >= 1980:
        r = r - abs(135 - time) - v * 1000
        done = True
        break
    """
    if v <= 0:
        # done=True
        r = r - (1980 - l) * 10
        break
    """

    i = round(v)
    if i > 80:
        i = 80

    if i < 0:
        i = 0

    if l < 150:
        j = l / 10
    elif l < 400:
        j = (l - 150) / 50 + 15
    elif l < 1400:
        j = (l - 400) / 100 + 20
    elif l < 1800:
        j = (l - 1400) / 50 + 30
    else:
        j = (l - 1800) / 10 + 38

    j = round(j)
    if j > 56:
        j = 56

    k = time / 5
    k = round(k)
    if k > 29:
        k = 29

    ob[0]=i
    ob[1]=j
    ob[2]=k

    iterCnts += 1

plt.plot(time_list, v_list)
plt.legend()
plt.show()
