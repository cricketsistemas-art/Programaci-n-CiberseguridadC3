#include <iostream>
#include <string>
using namespace std;

struct Producto {
    string nombre;
    float precio;
    int cantidad;
};

int main() {
    Producto p[5];
    float total = 0;

    for (int i = 0; i < 5; i++) {
        cout << "\nProducto " << i + 1 << endl;
        cout << "Nombre: ";
        cin.ignore();
        getline(cin, p[i].nombre);
        cout << "Precio: ";
        cin >> p[i].precio;
        cout << "Cantidad: ";
        cin >> p[i].cantidad;

        total += p[i].precio * p[i].cantidad;
    }

    cout << "\nValor total del inventario: " << total << endl;

    return 0;
}
