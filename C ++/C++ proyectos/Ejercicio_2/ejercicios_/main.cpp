#include <iostream>
using namespace std;

int main() {
    string nombre;
    int edad;
    float estatura;

    cout << "Ingrese su nombre: ";
    getline(cin, nombre);
    cout << "Ingrese su edad: ";
    cin >> edad;
    cout << "Ingrese su estatura: ";
    cin >> estatura;

    cout << "\n--- FICHA PERSONAL ---\n";
    cout << "Nombre: " << nombre << endl;
    cout << "Edad: " << edad << endl;
    cout << "Estatura: " << estatura << endl;

    return 0;
}
