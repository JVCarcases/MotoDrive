#define _USE_MATH_DEFINES

#include <iostream>
#include <vector>
#include <cmath>
#include <map>
#include <algorithm>
#include <math.h>

using namespace std;

// Convert degrees to radians manually
double radians(double degrees) 
{
    return degrees * M_PI / 180.0;
}

vector<double> linspace(double start, double stop, int num)
{
    vector<double> result(num);
    double step = (stop - start) / (num - 1);
    for (int i = 0; i < num; i++) {
        result[i] = start + i * step;
    }
    return result;
}

vector<double> pacejka_fx(const vector<double>& kappa, double B, double C, double D, double E, double N)
{
    vector<double> result(kappa.size());
    for (size_t i = 0; i < kappa.size(); i++) {
        result[i] = D * sin(C * atan(B * kappa[i] - E * (B * kappa[i] - atan(B * kappa[i])))) * N;
    }
    return result;
}

vector<double> pacejka_fy(const vector<double>& alpha, double gamma, double B1, double C1, double D, double E1, double B2, double C2, double E2, double N)
{
    vector<double> result(alpha.size());
    for (size_t i = 0; i < alpha.size(); i++) {
        result[i] = N * D * (sin(C1 * atan(B1 * alpha[i] - E1 * (B1 * alpha[i] - atan(B1 * alpha[i])))) +
                             sin(C2 * atan(B2 * gamma - E2 * (B2 * gamma - atan(B2 * gamma)))));
    }
    return result;
}

vector<pair<double, double>> group_mean(const vector<double>& x, const vector<double>& y)
{
    map<double, pair<double, int>> sums_counts;
    for (size_t i = 0; i < x.size(); i++) {
        sums_counts[x[i]].first += y[i];
        sums_counts[x[i]].second++;
    }
    vector<pair<double, double>> means;
    for (const auto& p : sums_counts) {
        means.emplace_back(p.first, p.second.first / p.second.second);
    }
    return means;
}

int main() {
    const int N = 5000;
    double Bx = 14, Cx = 1.6, Dx = 1.61, Ex = 0;
    double By1 = 7, Cy1 = 1.2, D = 1.61, Ey1 = 0;
    double By2 = 8, Cy2 = 0.6, Ey2 = 0;
    double Fz = 193 / 2 * 9.81;
    double mu = 0.8;

    vector<double> kappa_values = linspace(-0.1, 0.1, N);
    vector<double> sideslip_values = linspace(-0.1, 0.1, N);
    vector<double> discrete_camber_degrees = {0, 10, 20, 30, 40, 50};
    vector<double> discrete_camber_radians;

    for (double deg : discrete_camber_degrees)
    {
        discrete_camber_radians.push_back(radians(deg)); // Convert to radians using the manual function
    }

    vector<double> Fx = pacejka_fx(kappa_values, Bx, Cx, Dx, Ex, Fz);
    vector<double> Fy = pacejka_fy(sideslip_values, discrete_camber_radians[0], By1, Cy1, D, Ey1, By2, Cy2, Ey2, Fz);

    // 2D Grid creation
    vector<vector<double>> Fx_grid(N, vector<double>(N));
    vector<vector<double>> Fy_grid(N, vector<double>(N));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            Fx_grid[i][j] = Fx[i];
            Fy_grid[i][j] = Fy[j];
        }
    }

    // Calculate total force and apply masking condition
    vector<vector<double>> F_total(N, vector<double>(N));
    vector<vector<double>> F_total_masked(N, vector<double>(N, -1));
    double muFz = mu * Fz;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            double total_force = sqrt(Fx_grid[i][j] * Fx_grid[i][j] + Fy_grid[i][j] * Fy_grid[i][j]);
            if (total_force < muFz) {
                F_total[i][j] = total_force;
                F_total_masked[i][j] = round(total_force);
            }
        }
    }

    // Extracting indexes where force equals mu*Fz rounded
    vector<pair<int, int>> indexes;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (F_total_masked[i][j] == int(muFz)) {
                indexes.emplace_back(i, j);
            }
        }
    }

    // Extract forces where total force equals mu*Fz
    vector<double> Fx_lim, Fy_lim;
    for (auto& idx : indexes) {
        Fx_lim.push_back(Fx_grid[idx.first][idx.second]);
        Fy_lim.push_back(Fy_grid[idx.first][idx.second]);
    }

    // Group and print the results
    vector<pair<double, double>> results = group_mean(Fx_lim, Fy_lim);
    for (auto& result : results) {
        cout << "Fx: " << result.first << ", Fy: " << result.second << endl;
    }

    return 0;
}