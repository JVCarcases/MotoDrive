import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import pandas as pd

# Definir las funciones de Pacejka para Fx y Fy
def pacejka_fx(kappa, B, C, D, E, N):
    """Calcula la fuerza longitudinal en función de kappa."""
    return D * np.sin(C * np.arctan(B * kappa - E * (B * kappa - np.arctan(B * kappa)))) * N

def pacejka_fy(sideslip_angle, camber_angle, B1, C1, D, E1, B2, C2, E2, N):
    """Calcula la fuerza lateral en función de sideslip_angle y camber_angle."""
    term1 = B1 * sideslip_angle - E1 * (B1 * sideslip_angle - np.arctan(B1 * sideslip_angle))
    term2 = B2 * camber_angle - E2 * (B2 * camber_angle - np.arctan(B2 * camber_angle))
    return N * D * (np.sin(C1 * np.arctan(term1)) + np.sin(C2 * np.arctan(term2)))

#Definimos los parámetros
Bx, Cx, Dx, Ex = 14, 1.6, 1.61, 0
By1, Cy1, D, Ey1 = 7, 1.2, 1.61, 0
By2, Cy2, Ey2 = 8, 0.6, 0
Fz = 193/2*9.81
mu = 0.8

######################################################################################################################
# ELIPSE DE FRICCIÓN VARIANDO EL SIDESLIP ANGLE Y CON CAMBER ANGLE NULO
######################################################################################################################


# kappa_values = np.linspace(-0.2, 0.2, 10000)
kappa_values = np.linspace(-0.1, 0.1, 10000)
# sideslip_values = np.linspace(-6*np.pi/180, 6*np.pi/180, 10000)
sideslip_values = np.linspace(-0.1, 0.1, 10000)
discrete_camber_degrees = [0, 10, 20, 30, 40, 50]  # Ángulos de camber en grados
discrete_camber_radians = np.radians(discrete_camber_degrees)  # Convertir grados a radianes

Fx1 = pacejka_fx(kappa_values, Bx, Cx, Dx, Ex, Fz)
Fy1 = pacejka_fy(sideslip_values, discrete_camber_radians[0], By1, Cy1, D, Ey1, By2, Cy2, Ey2, Fz)

Fx_grid1, Fy_grid1 = np.meshgrid(Fx1, Fy1)


F_total1 = np.sqrt(Fx_grid1**2 + Fy_grid1**2)

F_total_masked1 = np.ma.masked_where(F_total1 >= mu*Fz, F_total1)


######################################################################################################################
# ELIPSE DE FRICCIÓN VARIANDO EL CAMBER ANGLE Y CON SIDESLIP ANGLE NULO
######################################################################################################################

# kappa_values = np.linspace(-0.2, 0.2, 10000)
kappa_values = np.linspace(-0.1, 0.1, 10000)
# camber_values = np.linspace(-50*np.pi/180, 50*np.pi/180, 10000)
camber_values = np.linspace(-0.1, 0.1, 10000)
discrete_sideslip_degrees = [0, 1, 2, 3, 4]
discrete_sideslip_radians = np.radians(discrete_sideslip_degrees)  # Convertir grados a radianes

Fx2 = pacejka_fx(kappa_values, Bx, Cx, Dx, Ex, Fz)
Fy2 = pacejka_fy(discrete_sideslip_radians[0], camber_values, By1, Cy1, D, Ey1, By2, Cy2, Ey2, Fz)

Fx_grid2, Fy_grid2 = np.meshgrid(Fx2, Fy2)

F_total2 = np.sqrt(Fx_grid2**2 + Fy_grid2**2)

# Fy_max = np.max(Fy)
# Fy_min = np.min(Fy)

cols2 = Fx_grid2.shape[1]
mid_cols2 = cols2 // 2
F_total_masked2 = np.ma.masked_where(F_total2 >= F_total2[0][mid_cols2], F_total2)
# F_total_masked2 = np.ma.masked_where(F_total2 >= mu*Fz, F_total2)

# vertices = [(Fx_grid[0][mid_cols],Fy_min,F_total[0][mid_cols]), (Fx_grid[0][mid_cols],Fy_max,F_total[0][mid_cols])]


#Create a figure with two subplots
fig, axs = plt.subplots(1, 2, figsize=(15, 6), subplot_kw={'projection': '3d'})

# Plot for angle of camber null
surf1 = axs[0].plot_surface(Fx_grid1, Fy_grid1, F_total_masked1, cmap='YlOrRd', alpha=0.5)
contour1 = axs[0].contour(Fx_grid1, Fy_grid1, F_total1, levels=[mu*Fz], colors='black')
# axs[0].set_aspect('equal', adjustable='box')
axs[0].set_xlabel('Fx')
axs[0].set_ylabel('Fy')
axs[0].set_zlabel('')
axs[0].set_title('Elipse de fricción de Pacejka con ángulo de camber nulo')

# Plot for angle of sideslip null
surf2 = axs[1].plot_surface(Fx_grid2, Fy_grid2, F_total_masked2, cmap='YlOrRd', alpha=0.5)
contour2 = axs[1].contour(Fx_grid2, Fy_grid2, F_total2, levels=[F_total2[0][mid_cols2]], colors='black')
# contour2 = axs[1].contour(Fx_grid2, Fy_grid2, F_total2, levels=[mu*Fz], colors='black')
# axs[1].set_aspect('equal', adjustable='box')
axs[1].set_xlabel('Fx')
axs[1].set_ylabel('Fy')
axs[1].set_zlabel('')
axs[1].set_title('Elipse de fricción de Pacejka con ángulo de sideslip nulo')

# Add colorbars
cbar1 = fig.colorbar(surf1, ax=axs[0], ticks=np.arange(0, np.amax(F_total1), 50))
cbar2 = fig.colorbar(surf2, ax=axs[1], ticks=np.arange(0, np.amax(F_total2), 50))

# Show the plot
plt.tight_layout()
plt.show()


Ftotal_rounded1 = np.round(F_total1, 0)
indexes = np.where(Ftotal_rounded1 == int(mu * Fz))
indices = np.array([[indexes[0][i], indexes[1][i]] for i in range(len(indexes[0]))])

F_lim = np.array([[Fx_grid1[ind[0]][ind[1]], Fy_grid1[ind[0]][ind[1]]] for ind in indices])
Fx_lim_raw = F_lim[:, 0]
Fy_lim_raw = F_lim[:, 1]

# Split data based on y value
mask_arriba = Fy_lim_raw > 0
mask_abajo = ~mask_arriba  # This is the same as Fy_lim_raw <= 0

x_arriba = Fx_lim_raw[mask_arriba]
y_arriba = Fy_lim_raw[mask_arriba]
x_abajo = Fx_lim_raw[mask_abajo]
y_abajo = Fy_lim_raw[mask_abajo]

# Calculate mean by unique x values
def group_mean(x, y):
    unique_x = np.unique(x)
    mean_y = np.array([y[x == ux].mean() for ux in unique_x])
    return np.column_stack((unique_x, mean_y))

result_arriba = group_mean(x_arriba, y_arriba)
result_abajo = group_mean(x_abajo, y_abajo)

# Concatenate results
result = np.concatenate((result_abajo, result_arriba))

# Extract Fx_lim and Fy_lim
Fx_lim = result[:, 0]
Fy_lim = result[:, 1]


A = np.column_stack((Fx_lim**2, Fx_lim*Fy_lim, Fy_lim**2, Fx_lim, Fy_lim, np.ones(len(result))))

# Resolver por mínimos cuadrados
u, s, vh = np.linalg.svd(A, full_matrices=False)
v = vh.T
coef = v[:, -1]  # El vector propio correspondiente al valor singular más pequeño

# print("Coeficientes de la elipse: A, B, C, D, E, F")
# print(coef)

plt.figure()
plt.scatter(Fx_lim, Fy_lim, s=1)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.show()
