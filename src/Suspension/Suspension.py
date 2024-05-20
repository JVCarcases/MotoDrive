import math
import matplotlib.pyplot as plt

# Parámetros
m = 193.0 / 2.0
g = 9.81
Lo = 0.7  # Elongación inicial en metros
dt = 0.01  # Paso de tiempo
totalTime = 10.0  # Tiempo total de simulación en segundos
steps = int(totalTime / dt)
k = m * math.pi * math.pi
b = 0.25 * 2.0 * math.sqrt(k * m)

# Condiciones iniciales
x = 0  # Desplazamiento inicial en metros
x_dot = 0  # Velocidad inicial en m/s
x_ddot = 0 # Aceleración inicial en m/s^2

# Listas para almacenar resultados
times = []
positions = []

# Bucle de simulación
for i in range(steps):
    # Calcula la aceleración (x_ddot)
    x_ddot = (m * g - (x + Lo) * k - x_dot * b) / m

    # Actualiza la velocidad y posición usando el método de Euler
    x_dot += x_ddot * dt
    x += x_dot * dt

    # Guarda los resultados
    times.append(i * dt)
    positions.append(0.7-x)

    # Imprime los resultados (opcional)
    print(f"Tiempo: {i * dt:.2f} s, Desplazamiento: {x:.4f} m, Velocidad: {x_dot:.4f} m/s, Aceleración: {x_ddot:.4f} m/s^2")

# Graficar el desplazamiento en función del tiempo
plt.figure(figsize=(10, 6))
plt.plot(times, positions, label='x (m)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Desplazamiento (m)')
plt.title('Desplazamiento en función del tiempo')
plt.ylim(0,1)
plt.legend()
plt.grid(True)
plt.show()
