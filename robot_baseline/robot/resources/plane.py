import pybullet as p
import pybullet_data
import os
import time

class Plane:
    def __init__(self, client):
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.loadURDF(fileName="plane.urdf",physicsClientId=client)