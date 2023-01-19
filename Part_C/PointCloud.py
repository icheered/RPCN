from rosbag import Bag
import numpy as np

S0_Translation = [-0.31542722, -0.14370224, -0.20138267]
S0_rotation_row1 = [-0.17536324, -0.88242307, -0.43655155]
S0_rotation_row2 = [0.56780261,   0.27159240, -0.77706999]
S0_rotation_row3 = [0.80426857,  -0.38414462,  0.45341480]
S1_Translation = [0.31813329,  -0.14264865, -0.19282741]
S1_rotation_row1 = [0.03916269,   0.87931668,  0.47462455]
S1_rotation_row2 = [-0.53352080,  0.42001741, -0.73412596]
S1_rotation_row3 = [-0.84487978, -0.22447172,  0.48558275]

scan0 = {}
scan1 = {}
for topic, msg, t in Bag('data/run1.bag'):
    if topic == '/scan0':
        # print(msg.header.seq)
        x = []
        y = []
        index = 0
        for i in msg.ranges:
            x.append(i*np.sin(msg.angle_min+msg.angle_increment*index))
            y.append(i*np.cos(msg.angle_min+msg.angle_increment*index))
            index += 1
        scan0[msg.header.seq] = x, y
    elif topic == '/scan1':
        # print(msg.header.seq)
        x = []
        y = []
        index = 0
        for i in msg.ranges:
            x.append(i*np.sin(msg.angle_min+msg.angle_increment*index))
            y.append(i*np.cos(msg.angle_min+msg.angle_increment*index))
            index += 1
        scan0[msg.header.seq] = x, y
