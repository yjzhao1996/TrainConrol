import numpy as np

policy=np.zeros((5,5,5,2))
bestAct=np.zeros(2)

bestAct[0]=2
bestAct[1]=4

policy[1][1][1]=bestAct

np.save('policy.npy', policy)

dict_data = np.load('policy.npy')

print(dict_data)