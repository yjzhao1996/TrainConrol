import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

class TrainEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.observation_space = spaces.Box(
            low=0, high=80, shape=(3,1))
        self.action_space = spaces.Box(
            low=1, high=10, shape=(2,1))
        self.state=np.zeros((3,1), dtype=int)

    def step(self, action):
        mass=192 #ton
        pos_state=self.state[1][0]
        v=self.state[0][0]
        a=action[0][0]
        b=action[1][0]
        brake_pos=1600
        r=0
        F=310
        if pos_state<15:
            l=pos_state*10
        elif pos_state<20:
            l=(pos_state-15)*50+150
        elif pos_state<30:
            l=(pos_state-20)*100+400
        elif pos_state<38:
            l=(pos_state-30)*50+1400
        else:
            l=(pos_state-38)*10+1800

        time=self.state[2][0]*5

        for t in range(1,6):
            if l<=130:
                speed_limit=53
            elif l<=1820:
                speed_limit=80
            else:
                speed_limit=46

            #traction
            if v<=36:
                T=310
            else:
                T=310-(v-36)*5

            if v<=60:
                B=260
            else:
                B=260-(v-60)*5

            if l<=470:
                g=0
            elif l<=520:
                g=0.04
            elif l<=700:
                g=0.08
            elif l<=750:
                g=0
            elif l<=850:
                g=-0.07
            elif l<=1020:
                g=-0.12
            elif l<=1120:
                g=0
            elif l<=1400:
                g=0.02
            elif l<=1780:
                g=0.03
            elif l<=1800:
                g=0.02
            elif l<=1820:
                g=0.01
            else:
                g=0

            fric=3.858*0.0001*v*v-0.064*v+2.965

            #v_target-b
            v1=speed_limit-b
            #v_target-a
            v2=speed_limit-a

            if v>=v2:
                F=0
            elif v<=v1:
                F=T

            if (l>brake_pos) and (v>0):
                F=-B

            F_all=F-fric
            ad=F_all/mass+g
            d_l=v/3.6*1+0.5*ad*1
            l=l+d_l
            v=v+ad*1*3.6
            time=time+1
            r=r-F*d_l
            if v <= 0 and l >= 1980:
                r=r-abs(135-time)
                break

        next_v=round(v)
        if next_v>80:
            next_v=80

        if next_v<0:
            next_v=0

        if l<150:
            next_pos=l/10
        elif l<400:
            next_pos=(l-150)/50+15
        elif l<1400:
            next_pos=(l-400)/100+20
        elif l<1800:
            next_pos=(l-1400)/50+30
        else:
            next_pos=(l-1800)/10+38

        next_pos=round(next_pos)
        if next_pos>56:
            next_pos=56

        next_time=time/5
        next_time=round(next_time)
        if next_time>29:
            next_time=29

        ob_next=np.zeros((3,1), dtype=int)
        ob_next[0][0]=next_v
        ob_next[1][0]=next_pos
        ob_next[2][0]=next_time

        self.state=ob_next

        done=False
        if next_v==0 and next_pos==56:
            done=True

        return ob_next, r, done, {}

    def reset(self):
        self.state[0][0] = 0
        self.state[1][0] = 0
        self.state[2][0] = 0
        return

    def render(self, mode='human'):
        return

    def close(self):
        return