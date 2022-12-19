# Initialize variables for integration
prev_time = None
positions = []
velocities = []

# Loop through each data point
for data in imu_data:
    # Extract time, acceleration, and gyroscope data
    time = data["time"]
    acceleration = data["acceleration"]
    gyro = data["gyro"]

    # If this is the first data point, just add it to the positions and velocities lists
    # and set the previous time to the current time
    if prev_time is None:
        positions.append((acceleration["x"], acceleration["y"], acceleration["z"]))
        velocities.append((gyro["x"], gyro["y"], gyro["z"]))
        prev_time = time
        continue

    # Calculate the time difference between the current data point and the previous one
    dt = time - prev_time

    # Use the acceleration and gyroscope data to update the position and velocity
    # using the formulas:
    # position = position + velocity * dt + 0.5 * acceleration * dt^2
    # velocity = velocity + acceleration * dt
    x = positions[-1][0] + velocities[-1][0] * dt + 0.5 * acceleration["x"] * dt**2
    y = positions[-1][1] + velocities[-1][1] * dt + 0.5 * acceleration["y"] * dt**2
    z = positions[-1][2] + velocities[-1][2] * dt + 0.5 * acceleration["z"] * dt**2
    positions.append((x, y, z))
    vx = velocities[-1][0] + acceleration["x"] * dt
    vy = velocities[-1][1] + acceleration["y"] * dt
    vz = velocities[-1][2] + acceleration["z"] * dt
    velocities.append((vx, vy, vz))

    # Set the previous time to the current time for the next iteration
    prev_time = time

# Now you can plot the positions to visualize the 3D trajectory
