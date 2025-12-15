#include <iostream>
using namespace std;

int main() {
    int opcion;
    float a, b;

    do {
        cout << "\n1. Sumar\n2. Restar\n3. Multiplicar\n4. Salir\n";
        cout << "Seleccione una opcion: ";
        cin >> opcion;

        if (opcion >= 1 && opcion <= 3) {
            cout << "Ingrese dos numeros: ";
            cin >> a >> b;
        }

        switch (opcion) {
            case 1: cout << "Resultado: " << a + b << endl; break;
            case 2: cout << "Resultado: " << a - b << endl; break;
            case 3: cout << "Resultado: " << a * b << endl; break;
            case 4: cout << "Saliendo...\n"; break;
            default: cout << "Opcion invalida\n";
        }

    } while (opcion != 4);

    return 0;
}
