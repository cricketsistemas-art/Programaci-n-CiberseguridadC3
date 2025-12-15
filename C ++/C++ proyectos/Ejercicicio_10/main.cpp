#include <iostream>
using namespace std;

int main() {
    int num, pares = 0, impares = 0;

    for (int i = 1; i <= 10; i++) {
        cout << "Ingrese numero " << i << ": ";
        cin >> num;

        if (num % 2 == 0)
            pares++;
        else
            impares++;
    }

    cout << "Cantidad de pares: " << pares << endl;
    cout << "Cantidad de impares: " << impares << endl;

    return 0;
}
