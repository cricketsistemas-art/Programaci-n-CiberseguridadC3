#include <iostream>
using namespace std;

int main() {
    int num, suma = 0;

    cout << "Ingrese numeros (0 para terminar):\n";
    while (true) {
        cin >> num;
        if (num == 0)
            break;
        suma += num;
    }

    cout << "Suma total: " << suma << endl;

    return 0;
}
