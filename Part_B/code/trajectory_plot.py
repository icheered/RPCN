import matplotlib.pyplot as plt

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
rel_path = 'Part_B/code/data/'
x_no_imu, y_no_imu = get_trajectory(rel_path+'trajectory_no_imu.txt')
x_with_imu, y_with_imu = get_trajectory(rel_path+'trajectory_with_imu.txt')

# plot overlayed trajectories
plt.plot(x_no_imu, y_no_imu, label='no IMU')
plt.plot(x_with_imu, y_with_imu, label='with IMU')
plt.legend()

plt.show(block=True)

