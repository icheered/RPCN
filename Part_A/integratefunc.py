from math import sin, cos

def integrate_imu_data(imu_data, dt):
    positions = []
    velocities = []
    orientations = []

    prev_time = 0
    prev_orientation = (0, 0, 0)  # roll, pitch, yaw
    prev_velocity = (0, 0, 0)  # x, y, z
    prev_position = (0, 0, 0)  # x, y, z

    for data in imu_data:
        time = data["time"]
        acceleration = data["acceleration"]
        gyro = data["gyro"]

        # Calculate the elapsed time since the last data point
        elapsed_time = time - prev_time

        # Integrate the gyroscope data to get the orientation
        roll = prev_orientation[0] + gyro["x"] * elapsed_time
        pitch = prev_orientation[1] + gyro["y"] * elapsed_time
        yaw = prev_orientation[2] + gyro["z"] * elapsed_time
        orientation = (roll, pitch, yaw)

        # Rotate the acceleration vector by the current orientation to
        # get the acceleration in the global frame
        x_accel = acceleration["x"] * cos(pitch) + acceleration["z"] * sin(pitch)
        y_accel = acceleration["x"] * sin(roll) * sin(pitch) + acceleration["y"] * cos(roll) - acceleration["z"] * sin(roll) * cos(pitch)
        z_accel = -acceleration["x"] * cos(roll) * sin(pitch) + acceleration["y"] * sin(roll) + acceleration["z"] * cos(roll) * cos(pitch)
        rotated_acceleration = (x_accel, y_accel, z_accel)

        # Integrate the acceleration to get the velocity
        x_velocity = prev_velocity[0] + rotated_acceleration[0] * elapsed_time
        y_velocity = prev_velocity[1] + rotated_acceleration[1] * elapsed_time
        z_velocity = prev_velocity[2] + rotated_acceleration[2] * elapsed_time
        velocity = (x_velocity, y_velocity, z_velocity)

        # Integrate the velocity to get the position
        x_position = prev_position[0] + x_velocity * elapsed_time
        y_position = prev_position[1] + y_velocity * elapsed_time
        z_position = prev_position[2] + z_velocity * elapsed_time
        position = (x_position, y_position, z_position)

        positions.append(position)
        velocities.append(velocity)
        orientations.append(orientation)

        prev_time = time
        prev_orientation = orientation
        prev_velocity = velocity
        prev_position = position

    return positions, velocities, orientations
