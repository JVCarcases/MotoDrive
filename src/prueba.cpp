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


int main() {
    vector<double> v;
    v = linspace(1,10,10);
    for(int i : v)
    {
        cout << i << " ";
    }
    return 0;
}