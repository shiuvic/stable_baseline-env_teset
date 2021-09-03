import pybullet as p
import os
import random
import numpy as np
from robot.resources.op3 import OP3
class sphere:
    def __init__(self, client):
        self.f_name = os.path.join(os.path.dirname(__file__), 'ball.urdf')
        x = random.uniform(0, 0.15)
        y = random.uniform(0.07, 0.13)
        z = random.uniform(0.1, 0.3)
        # arr1 = [0.09, 0.06, 0.26]
        self.arr = [[0.16, 0.13, 0.32],
                    [0.10, 0.07, 0.27],
                    [0.13, 0.10, 0.29]]
        arr1 = [x,y,z]
        self.x = 0
        self.ball= p.loadURDF(fileName=self.f_name, basePosition=arr1, physicsClientId=client)

    def get_pos(self):
        pos, _ = p.getBasePositionAndOrientation(self.ball)
        return pos

    def newpos(self):
        p.resetBasePositionAndOrientation(self.ball, self.arr[self.x], [0,0,0,1])
        self.x += 1
        if self.x > 2:
            self.x = 0
        print(self.get_pos())

class box:
    def __init__(self, client):
        self.f_name = os.path.join(os.path.dirname(__file__), 'redbox.urdf')
        # x = random.uniform(0, 0.15)
        # y = random.uniform(0.07, 0.13)
        # z = random.uniform(0.1, 0.3)
        arr1 = [1, 0.0, 0.0]
        # self.arr = [[0.16, 0.13, 0.32],
        #             [0.10, 0.07, 0.27],
        #             [0.13, 0.10, 0.29]]
        # arr1 = [x, y, z]
        self.x = 0
        self.box = p.loadURDF(fileName=self.f_name, basePosition=arr1, physicsClientId=client)