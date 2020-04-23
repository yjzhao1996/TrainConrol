import gym
import numpy as np
import math

env=gym.make('gym_train:train-v0')
act=np.zeros((2,1))

value=np.zeros((81,57,30))

for i in range(0,30,1):
    value[0][56][i]=-abs(135-i*5)

iterCounts=120

while iterCounts:
    print(iterCounts)
    iterCounts-=1
    delta=0
    for i in range(0,81):
        print(i)
        for j in range(0,57):
            for k in range(0,30):
                if i==0 and j==56:
                    continue
                else:
                    tmp_value=value[i][j][k]
                    Q = np.zeros((10, 10))
                    for b in range(1,11):
                        for a in range(0,b):
                            act[0][0]=a
                            act[1][0]=b
                            ob_next, reward, done, info=env.step(act)
                            Q[a][b-1]=reward+value[ob_next[0][0]][ob_next[1][0]][ob_next[2][0]]
                    value[i][j][k]=np.amax(Q)
                    delta=max(delta,abs(tmp_value-value[i][j][k]))
    print(delta)
    if(delta==0):
        break

policy=np.zeros((81,57,30,2))
eps_pol = 10 ** -8;
for i in range(0, 81):
    for j in range(0, 57):
        for k in range(0, 30):
            bestVal=-math.inf
            bestAct=np.zeros(2)
            for b in range(1, 11):
                for a in range(0, b):
                    act[0][0] = a
                    act[1][0] = b
                    ob_next, reward, done, info = env.step(act)
                    tmpValue=reward + value[ob_next[0][0]][ob_next[1][0]][ob_next[2][0]]
                    if (tmpValue-eps_pol)>bestVal:
                        bestVal=tmpValue
                        bestAct[0]=a
                        bestAct[1]=b

            policy[i][j][k]=bestAct

np.save('policy.npy', policy)
#https://machinelearningmastery.com/how-to-save-a-numpy-array-to-file-for-machine-learning/


