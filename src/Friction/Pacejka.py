import numpy as np
import matplotlib.pyplot as plt

# Definir los parámetros de Pacejka
Bx, Cx, Dx, Ex = 14, 1.6, 1.61, 0
By1, Cy1, D, Ey1 = 7, 1.2, 1.61, 0
By2, Cy2, Ey2 = 8, 0.6, 0
Fz = 1150

# Definir las funciones de Pacejka para Fx y Fy
def pacejka_fx(kappa, B, C, D, E, N):
    """Calcula la fuerza longitudinal en función de kappa."""
    return D * np.sin(C * np.arctan(B * kappa - E * (B * kappa - np.arctan(B * kappa)))) * N

def pacejka_fy(sideslip_angle, camber_angle, B1, C1, D, E1, B2, C2, E2, N):
    """Calcula la fuerza lateral en función de sideslip_angle y camber_angle."""
    term1 = B1 * sideslip_angle - E1 * (B1 * sideslip_angle - np.arctan(B1 * sideslip_angle))
    term2 = B2 * camber_angle - E2 * (B2 * camber_angle - np.arctan(B2 * camber_angle))
    return N * D * (np.sin(C1 * np.arctan(term1)) + np.sin(C2 * np.arctan(term2)))

# Generar valores para kappa, sideslip angle y camber angle
kappa_values = np.linspace(-1, 1, 400)
sideslip_angles = np.linspace(-0.035, 0.1, 400)
sideslip_angles_degrees = np.degrees(sideslip_angles)
camber_angles = np.linspace(0, 0.873, 400)
camber_angles_degrees = np.degrees(camber_angles)

# Generar valores discretos de los ángulos para estudiar varios casos
discrete_camber_degrees = [0, 10, 20, 30, 40, 50]  # Ángulos de camber en grados
discrete_camber_radians = np.radians(discrete_camber_degrees)  # Convertir grados a radianes
discrete_sideslip_degrees = [-1, 0, 1, 2]
discrete_sideslip_radians = np.radians(discrete_sideslip_degrees)

# Calcular Fx para una red de valores
Fx = [pacejka_fx(kappa, Bx, Cx, Dx, Ex, Fz) for kappa in kappa_values]

# Configurar la visualización de los gráficos
plt.figure(figsize=(12, 6))

# Graficar la fuerza longitudinal Fx en función de kappa
plt.subplot(2, 2, 1)
plt.plot(kappa_values, Fx, label='Fuerza Longitudinal $F_x$')
plt.title('Fuerza Longitudinal $F_x$ vs. Kappa')
plt.xlabel('Kappa ($\kappa$)')
plt.ylabel('Fuerza Longitudinal ($F_x$)')
plt.grid(True)
plt.legend()

# Graficar la fuerza lateral Fy en función del sideslip angle para varios ángulos de camber
plt.subplot(2, 2, 2)
for camber, deg in zip(discrete_camber_radians, discrete_camber_degrees):
    Fy_values = [pacejka_fy(sideslip, camber, By1, Cy1, D, Ey1, By2, Cy2, Ey2, Fz) for sideslip in sideslip_angles]
    plt.plot(sideslip_angles_degrees, Fy_values, label=f'Camber {deg}°')
plt.title('Fuerza Lateral $F_y$ vs. Sideslip Angle para diferentes Camber Angles')
#plt.ylim(0, 1.6)
#plt.xlim(-2, 6)
plt.xlabel('Sideslip Angle (grados º)')
plt.ylabel('Fuerza Lateral $F_y$')
plt.grid(True)
plt.legend()

# Graficar la fuerza lateral Fy en función del ángulo de camber y varios sideslip angles
plt.subplot(2, 2, 3)
for sideslip, deg in zip(discrete_sideslip_radians, discrete_sideslip_degrees):
    Fy_values = [pacejka_fy(sideslip, camber, By1, Cy1, D, Ey1, By2, Cy2, Ey2, Fz) for camber in camber_angles]
    plt.plot(camber_angles_degrees, Fy_values, label=f'Sideslip {deg}°')
plt.title('Fuerza Lateral $F_y$ vs. Camber Angle para diferentes Sideslip Angles')
#plt.ylim(0, 1.6)
#plt.xlim(0, 50)
plt.xlabel('Camber Angle (grados º)')
plt.ylabel('Fuerza Lateral $F_y$')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
