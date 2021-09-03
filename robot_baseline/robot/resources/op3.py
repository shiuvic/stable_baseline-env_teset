import time
from threading import Thread
import pybullet_data
import pybullet as p
import os
import numpy as np


op3_joints = ['l_hip_yaw',
              'l_hip_roll',
              'l_hip_pitch',
              'l_knee',
              'l_ank_pitch',
              'l_ank_roll',
              'r_hip_yaw',
              'r_hip_roll',
              'r_hip_pitch',
              'r_knee',
              'r_ank_pitch',
              'r_ank_roll',
              'l_sho_pitch',
              'l_sho_roll',
              'l_el',
              'link1',
              'r_sho_pitch',
              'r_sho_roll',
              'r_el',
              'head_pan',
              'head_tilt']
angles = {'l_hip_yaw': -0.0006003781295184577, 'l_hip_roll': 0.00027541140297364884,
                'l_hip_pitch': -0.0027132214875610623, 'l_knee': -0.0003529878949643889,
                'l_ank_pitch': 0.00234694503638634, 'l_ank_roll': 0.00221300029210034,
                'r_hip_yaw': -0.0003914124825885725, 'r_hip_roll': 0.00041712889275416005,
                'r_hip_pitch': -0.0011724624759162654, 'r_knee': 0.0047281000738706065,
                'r_ank_pitch': -0.0036229814257040358, 'r_ank_roll': 0.0038011178078730906,
                'l_sho_pitch': -5.9948193227529784e-05, 'l_sho_roll': 0.0003006644446475642,
                'l_el': 0.00027580599176571416, 'r_sho_pitch': -3.449540793066871e-05,
                'r_sho_roll': 0.0001028452376745412, 'r_el': 9.637206668694198e-05, 'head_pan': 0.00048666303033982546,
                'head_tilt': -0.00015481243935058867}


class OP3:
    def __init__(self, client):
        self.client = client
        # f_name = os.path.join(os.path.dirname(__file__), 'robotis_op3.urdf')
        f_name = os.path.join(os.path.dirname(__file__), 'testurdf.urdf')
        self.robot = p.loadURDF(fileName=f_name,basePosition=[0, 0, 0.3],physicsClientId=client)
        self.arm = dict()
        self.numJoints = p.getNumJoints(self.robot)
        self.joints = op3_joints
        self._set_joint()
        self.state = [0,0,0]
        p.setJointMotorControl(self.robot, 12, p.POSITION_CONTROL, 2, 100)
        # self.update_camera_th()
        for joint in range(self.numJoints):
            print(p.getJointInfo(self.robot, joint))

    def resetandstart(self):
        for joint in range(self.numJoints):
            # print(p.getJointInfo(self.robot, joint))
            p.setJointMotorControl(self.robot, joint, p.POSITION_CONTROL, 0, 100)

    def get_ids(self):
        return self.robot, self.client

    def apply_action(self, action):

        move1,move2,move3 = action
        # Clip 到合理範圍
        move1 = 0.5 * move1
        move2 = 0.5 * move2
        move3 = 0.5 * move3

        move1 = max(min(move1, 2.), -2.)
        move2 = max(min(move2, 2.), -2.)
        move3 = max(min(move3, 2.), -2.)
        self.arm['l_sho_pitch'] = move1
        self.arm['l_sho_roll'] = move2
        self.arm['l_el'] = move3
        self.set_angles(self.arm)

    def getlel(self):
        pos = p.getLinkState(self.robot, 15)[0]
        return pos

    def get_observation(self):
        # 取得位置
        l_sho_pitch = p.getJointState(self.robot,12)[0]
        l_sho_roll = p.getJointState(self.robot, 13)[0]
        l_el = p.getJointState(self.robot, 14)[0]
        pos = [l_sho_pitch,l_sho_roll,l_el]
        observation = pos
        return observation

    def set_angles(self, angles):
        for j, v in angles.items():
            p.setJointMotorControl(self.robot, op3_joints.index(j), p.POSITION_CONTROL, v, 100)

    def set_angles_slow(self, stop_angles, delay=2):
        start_angles = {'l_hip_yaw': -0.0006003781295184577, 'l_hip_roll': 0.00027541140297364884,
                'l_hip_pitch': -0.0027132214875610623, 'l_knee': -0.0003529878949643889,
                'l_ank_pitch': 0.00234694503638634, 'l_ank_roll': 0.00221300029210034,
                'r_hip_yaw': -0.0003914124825885725, 'r_hip_roll': 0.00041712889275416005,
                'r_hip_pitch': -0.0011724624759162654, 'r_knee': 0.0047281000738706065,
                'r_ank_pitch': -0.0036229814257040358, 'r_ank_roll': 0.0038011178078730906,
                'l_sho_pitch': -5.9948193227529784e-05, 'l_sho_roll': 0.0003006644446475642,
                'l_el': 0.00027580599176571416, 'r_sho_pitch': -3.449540793066871e-05,
                'r_sho_roll': 0.0001028452376745412, 'r_el': 9.637206668694198e-05, 'head_pan': 0.00048666303033982546,
                'head_tilt': -0.00015481243935058867}
        start = time.time()
        stop = start + delay
        while True:
            t = time.time()
            if t > stop: break
            ratio = (t - start) / delay
            angles = interpolate(stop_angles, start_angles, ratio)
            self.set_angles(angles)
            time.sleep(0.1)

    def _set_joint(self):
        for j, v in angles.items():
            if j not in self.joints:
                AssertionError("Invalid joint name " + j)
                continue
            p.setJointMotorControl(self.robot, op3_joints.index(j), p.POSITION_CONTROL, v, 100)

    # def update_camera_th(self):
    #     def _setCameraPicAndGetPic():
    #         while True:
    #             width = 224
    #             height = 224
    #             BASE_RADIUS = 3
    #             BASE_THICKNESS = 3
    #             # basePos = p.getLinkState(self.robot, 19)[0]
    #             basePos,baseOrientation = p.getBasePositionAndOrientation(self.robot, physicsClientId=self.client)
    #
    #             matrix = p.getMatrixFromQuaternion(baseOrientation, physicsClientId=self.client)
    #             tx_vec = np.array([matrix[0], matrix[3], matrix[6]])  # 变换后的x轴
    #             tz_vec = np.array([matrix[2], matrix[5], matrix[8]])  # 变换后的z轴
    #
    #             basePos = np.array(basePos)
    #             # 摄像头的位置
    #             cameraPos = basePos + BASE_RADIUS * tx_vec + 0.5 * BASE_THICKNESS * tz_vec
    #             targetPos = cameraPos + 1 * tx_vec
    #
    #             viewMatrix = p.computeViewMatrix(
    #                 cameraEyePosition=cameraPos,
    #                 cameraTargetPosition=targetPos,
    #                 cameraUpVector=tz_vec,
    #                 physicsClientId=self.client
    #             )
    #             projectionMatrix = p.computeProjectionMatrixFOV(
    #                 fov=50.0,  # 摄像头的视线夹角
    #                 aspect=1.0,
    #                 nearVal=0.01,  # 摄像头焦距下限
    #                 farVal=20,  # 摄像头能看上限
    #                 physicsClientId=self.client
    #             )
    #
    #             width, height, rgbImg, depthImg, segImg = p.getCameraImage(
    #                 width=width, height=height,
    #                 viewMatrix=viewMatrix,
    #                 projectionMatrix=projectionMatrix,
    #                 renderer=p.ER_BULLET_HARDWARE_OPENGL,
    #                 physicsClientId=self.client
    #             )
    #             return width, height, rgbImg, depthImg, segImg
    #     Thread(target=_setCameraPicAndGetPic).start()

def interpolate(anglesa, anglesb, coefa):
    z = {}
    joints = anglesa.keys()
    for j in joints:
        z[j] = anglesa[j] * coefa + anglesb[j] * (1 - coefa)
    return z

