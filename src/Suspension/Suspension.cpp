#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>

// Definir M_PI si no está definido
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

int main() {
    // Parámetros
    double m = 193.0 / 2.0;
    double g = 9.81;
    double Lo = 0.7;  // Elongación inicial en metros
    double dt = 0.01; // Paso de tiempo
    double totalTime = 10.0; // Tiempo total de simulación en segundos
    int steps = static_cast<int>(totalTime / dt);
    double k = m * M_PI * M_PI;
    double b = 0.25 * 2.0 * std::sqrt(k * m);

    // Condiciones iniciales
    double x = 0; // Desplazamiento inicial en metros
    double x_dot = 0; // Velocidad inicial en m/s
    double x_ddot; // Aceleración inicial en m/s^2

    // Vectores para almacenar resultados
    std::vector<double> times;
    std::vector<double> positions;

    // Bucle de simulación
    for (int i = 0; i < steps; ++i) {
        // Calcula la aceleración (x_ddot)
        x_ddot = (m * g - (x + Lo) * k - x_dot * b) / m;

        // Actualiza la velocidad y posición usando el método de Euler
        x_dot += x_ddot * dt;
        x += x_dot * dt;

        // Guarda los resultados
        times.push_back(i * dt);
        positions.push_back(0.7 - x);
    }

    // Escribir los resultados en un archivo CSV
    std::ofstream file("C:/Users/1M72696/Documents/1.MOISEBIM/Programas/srcsimulacion_suspension.csv");
    file << "Tiempo (s),Desplazamiento (m)\n";
    for (size_t i = 0; i < times.size(); ++i) {
        file << times[i] << "," << positions[i] << "\n";
    }
    file.close();

    std::cout << "Simulación completada. Resultados guardados en 'simulacion_suspension.csv'.\n";

    return 0;
}
