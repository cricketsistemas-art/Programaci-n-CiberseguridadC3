#include <iostream>
#include <string>
using namespace std;

struct Estudiante {
    string nombre;
    int edad;
    float promedio;
};

int main() {
    Estudiante e[3];
    int mejor = 0;

    for (int i = 0; i < 3; i++) {
        cout << "\nEstudiante " << i + 1 << endl;
        cout << "Nombre: ";
        cin.ignore();
        getline(cin, e[i].nombre);
        cout << "Edad: ";
        cin >> e[i].edad;
        cout << "Promedio: ";
        cin >> e[i].promedio;

        if (e[i].promedio > e[mejor].promedio)
            mejor = i;
    }

    cout << "\nMejor promedio:\n";
    cout << "Nombre: " << e[mejor].nombre << endl;
    cout << "Promedio: " << e[mejor].promedio << endl;

    return 0;
}
