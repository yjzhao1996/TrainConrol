import numpy as np
import matplotlib.pyplot as plt
mass=192

i=0
j=0
k=0

iterCnts=0
r=0
brake_pos=1800
all_policy=np.zeros((50,2))
g=0
E=0

policy = np.load('policy.npy')
time_list=[]
v_list=[]

while(1):

    a=policy[i][j][k][0]
    b=policy[i][j][k][1]
    all_policy[iterCnts][0]=a
    all_policy[iterCnts][1]=b
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

        if (l > brake_pos) and (v > 0):
            F = -B

        F_ab=abs(F)
        F_all = F - fric
        ad = F_all / mass + g
        d_l = v / 3.6 * 0.1 + 0.5 * ad * 0.01
        l = l + d_l
        v = v + ad * 0.1 * 3.6
        time = time + 0.1
        time_list.append(time)
        print(time)
        v_list.append(v)
        #print(v)
        #print(F_all)
        r = r - F * d_l
        E=E+d_l*F_ab
        if v <= 0 and l >= 1980:
            break

    if v <= 0 and l >= 1980:
        break

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


    iterCnts += 1

plt.plot(time_list, v_list)
plt.legend()
plt.show()
