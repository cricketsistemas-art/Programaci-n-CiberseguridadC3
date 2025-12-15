#include <iostream>
using namespace std;

int main() {
    float celsius, fahrenheit;

    cout << "Ingrese grados Celsius: ";
    cin >> celsius;

    fahrenheit = (celsius * 9 / 5) + 32;

    cout << "Equivalente en Fahrenheit: " << fahrenheit << endl;

    return 0;
}
