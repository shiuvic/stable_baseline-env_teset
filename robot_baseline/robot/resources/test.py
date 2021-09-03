from sphere import sphere
import pybullet as p
while True:
    op3 = sphere(p.connect(p.GUI))
    print('>>>>>>>>',op3.get_pos)