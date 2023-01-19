import matplotlib.pyplot as plt

#dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bagpy
from bagpy import bagreader

def part_a_trajectory(filename):
    bag = bagreader(filename)

    gyro_df = pd.read_csv(bag.message_by_topic('/imu/angular_velocity'))

    # calculate time difference between measurements
    timesteps = (gyro_df['header.stamp.secs'].diff(1) + gyro_df['header.stamp.nsecs'].diff(1) / 1e9).to_numpy()
    vec_gyro_raw = gyro_df[['vector.x', 'vector.y', 'vector.z']].rolling(20).mean().to_numpy()

    # replace nan values using closest value
    def replace_nan(a):
        ind = np.where(~np.isnan(a))[0]
        first, last = ind[0], ind[-1]
        a[:first] = a[first]
        a[last + 1:] = a[last]
        return a
    timesteps = replace_nan(timesteps)
    vec_gyro_raw = replace_nan(vec_gyro_raw)

    vec_rotation = np.cumsum(vec_gyro_raw * timesteps[:, np.newaxis], axis=0)

    # rotation calculations
    vec_velocity_rotated = np.zeros_like(vec_gyro_raw)
    for nr, (roll, pitch, yaw) in enumerate(vec_rotation):    # loop over vectors
        rollMatrix = np.matrix([                    # rotation about x
            [1, 0,             0           ],
            [0, np.cos(roll), -np.sin(roll)],
            [0, np.sin(roll),  np.cos(roll)]])
        pitchMatrix = np.matrix([                   # rotation about y
            [ np.cos(pitch), 0, np.sin(pitch)],
            [0,              1,  0           ],
            [-np.sin(pitch), 0, np.cos(pitch)]])
        yawMatrix = np.matrix([                     # rotation about z
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw),  np.cos(yaw), 0],
            [0,            0,           1]])

        R = yawMatrix * pitchMatrix * rollMatrix        # combined rotation matrix
        accel_rotated = np.matmul(R, [0.75, 0, 0])     # matrix multiplication with accel vector

        vec_velocity_rotated[nr, :] = accel_rotated        # add to array

    # integrate accel and velocity to get position (multiply with timestep, then cumulative sum)
    vec_position = np.cumsum(vec_velocity_rotated * timesteps[:, np.newaxis], axis=0)

    start_offset = 1300
    return vec_position[start_offset:-1000] - vec_position[start_offset]


# echo the ros topic into a file, this function takes the x, y values back out
def get_trajectory(filename):
    trajectory_x = []
    trajectory_y = []
    in_points = False

    with open(filename) as f:
        for line in f:
            # find the start of the section that contains all point
            if 'points' in line:
                in_points = True
                trajectory_x = []
                trajectory_y = []
            if 'color' in line:
                in_points = False
            
            # if not in correct section, continue with next lines
            if not in_points:
                continue
            
            # get the x and y values
            if 'x' in line:
                val = line.split(':')[-1]
                val = float(val)
                trajectory_x.append(val)
            if 'y' in line:
                val = line.split(':')[-1]
                val = float(val)
                trajectory_y.append(val)

    return trajectory_x, trajectory_y


# process the files to get trajectories
rel_path = 'RPCN/Part_B/code/data/'
part_a_traject = part_a_trajectory(rel_path+"test3.bag")
x_no_imu, y_no_imu = get_trajectory(rel_path+'trajectory_no_imu.txt')
x_with_imu, y_with_imu = get_trajectory(rel_path+'trajectory_with_imu.txt')

# plot overlayed trajectories
plt.plot(part_a_traject[:, 0], part_a_traject[:, 1], label='Only IMU')
plt.plot(x_no_imu, y_no_imu, label='Only lidar')
plt.plot(x_with_imu, y_with_imu, label='Lidar and IMU')
plt.legend()
plt.title('trajectories as calculated from IMU and Lidar data')

plt.show(block=True)

