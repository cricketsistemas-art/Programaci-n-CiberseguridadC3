#include <iostream>
using namespace std;

int main() {
    float base, altura, area;

    cout << "Ingrese la base: ";
    cin >> base;
    cout << "Ingrese la altura: ";
    cin >> altura;

    area = base * altura;

    cout << "Area del rectangulo: " << area << endl;

    return 0;
}
