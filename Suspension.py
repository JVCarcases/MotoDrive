import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to update the plot in real-time
def update_plot(frame, times, displacements):
    ax.clear()
    ax.plot([-1, 1], [0, 0], 'k')  # Suspension line
    ax.plot([0, 0], [0, displacements[frame]], 'r-')  # Spring
    ax.plot(0, displacements[frame], 'bs', markersize=10)  # Mass
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.set_title(f'Time: {times[frame]:.2f}s')

def suspension_system(m, k, r, F, dt, T):
    # Initial conditions
    v = 0  # initial velocity
    x = 0  # initial displacement
    
    # Arrays to store results
    times = np.arange(0, T, dt)
    displacements = []
    velocities = []
    
    # Simulation loop
    for t in times:
        # Compute acceleration using Newton's second law
        a = (F - k * x - r * v) / m
        
        # Update velocity and displacement using Euler's method
        v += a * dt
        x += v * dt
        
        # Store results
        displacements.append(x)
        velocities.append(v)
        
    return times, displacements, velocities



# System parameters
m = 1300/4  # mass (kg)
k = 4*np.pi*np.pi*m # spring stiffness (N/m)
r = 0.25*2*np.sqrt(k*m)  # damping coefficient (Ns/m)
F = -2000  # external force (N)
dt = 0.01  # time step (s)
T = 10  # total simulation time (s)

# Simulate the suspension system
times, displacements, velocities = suspension_system(m, k, r, F, dt, T)


# Plot results
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(times, displacements)
plt.title('Displacement vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')

plt.subplot(2, 1, 2)
plt.plot(times, velocities)
plt.title('Velocity vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')

plt.tight_layout()
plt.show()

# Create the animation
fig, ax = plt.subplots()
animation = FuncAnimation(fig, update_plot, frames=len(times), fargs=(times, displacements), interval=dt*1000)

plt.show()