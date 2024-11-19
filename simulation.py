import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81            # Gravitational acceleration (m/s^2)
mp = 0.1            # Mass of pendulum (kg)
mc = 1.0            # Mass of cart (kg)
m = mp + mc         # Total mass (kg)
l = 0.5             # Length of the pendulum (m)
tau = 0.02          # Time step for Euler integration (s)
total_time = 10.0   # Total simulation time (s)
steps = int(total_time / tau)  # Number of simulation steps

# Initial conditions
theta = 0.1           # Initial angle measured from vertical (rad)
theta_dot = 0.0    # Initial angular velocity (rad/s)
h_dot = 0.0        # Initial cart velocity (m/s)
h = 0.0            # Initial cart position (m)
F = 0.0            # Initial force (N), set externally for control

# Arrays to store results
theta_array = np.zeros(steps)
theta_dot_array = np.zeros(steps)
h_array = np.zeros(steps)
h_dot_array = np.zeros(steps)
time_array = np.linspace(0, total_time, steps)

# Initial conditions
theta_array[0] = theta
theta_dot_array[0] = theta_dot
h_array[0] = h
h_dot_array[0] = h_dot

# Simulation loop using Euler's method
for i in range(1, steps):
    #TODO: Compute force based on previous state
    #F = 
    
    # Compute angular acceleration (theta_ddot)
    numerator = (
        m * g * np.sin(theta) -
        np.cos(theta) * (F + mp * l * theta_dot**2 * np.sin(theta))
    )
    denominator = (4/3) * m * l - mp * l * np.cos(theta)**2
    theta_ddot = numerator / denominator

    # Compute horizontal acceleration (h_ddot)
    h_ddot = (
        F + mp * l * (theta_dot**2 * np.sin(theta) - theta_ddot * np.cos(theta))
    ) / m

    # Euler integration
    theta_dot += tau * theta_ddot
    theta += tau * theta_dot
    h_dot += tau * h_ddot
    h += tau * h_dot

    # Check for failure state?
    # if (abs(theta) >= np.pi):
    #     theta_dot = 0
    #     h_dot = 0

    # Store results
    theta_array[i] = theta
    theta_dot_array[i] = theta_dot
    h_array[i] = h
    h_dot_array[i] = h_dot


# Save results to file
np.save("data/h_values.npy", h_array)
np.save("data/theta_values.npy", theta_array)

# Plot results
plt.figure(figsize=(12, 6))

# Pendulum angle
plt.subplot(2, 1, 1)
plt.plot(time_array, theta_array, label="Theta (rad)")
plt.xlabel("Time (s)")
plt.ylabel("Pendulum Angle (rad)")
plt.grid()
plt.legend()

# Cart position
plt.subplot(2, 1, 2)
plt.plot(time_array, h_array, label="Cart Position (m)")
plt.xlabel("Time (s)")
plt.ylabel("Cart Position (m)")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
