#include <iostream>
#include <vector>
#include <string>
#include <cctype>

using namespace std;

// Vectores globales
vector<string> usuarios;
vector<string> contrasenas;

// Prototipos de funciones
bool VerificarContrasena(string pass);
void RegistrarUsuario();
void GenerarAlertas();
void MostrarUsuarios();

int main() {
    int opcion;

    do {
        cout << "\n===== GESTOR DE CONTRASENAS SEGURAS =====\n";
        cout << "1. Registrar usuario\n";
        cout << "2. Mostrar usuarios\n";
        cout << "3. Verificar contrasenas debiles\n";
        cout << "4. Salir\n";
        cout << "Seleccione una opcion: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                RegistrarUsuario();
                break;
            case 2:
                MostrarUsuarios();
                break;
            case 3:
                GenerarAlertas();
                break;
            case 4:
                cout << "Saliendo del programa...\n";
                break;
            default:
                cout << "Opcion invalida\n";
        }

    } while (opcion != 4);

    return 0;
}

// ================= FUNCIONES =================

// Registrar usuario y contraseña
void RegistrarUsuario() {
    string user, pass;

    cout << "\nIngrese nombre de usuario: ";
    cin >> user;

    cout << "Ingrese contrasena: ";
    cin >> pass;

    usuarios.push_back(user);
    contrasenas.push_back(pass);

    if (VerificarContrasena(pass)) {
        cout << "Contrasena segura registrada correctamente.\n";
    } else {
        cout << "ADVERTENCIA: Contrasena debil.\n";
    }
}

// Verificar fuerza de la contraseña
bool VerificarContrasena(string pass) {
    bool mayuscula = false;
    bool minuscula = false;
    bool numero = false;
    bool simbolo = false;

    if (pass.length() < 8)
        return false;

    for (int i = 0; i < pass.length(); i++) {
        if (isupper(pass[i])) mayuscula = true;
        else if (islower(pass[i])) minuscula = true;
        else if (isdigit(pass[i])) numero = true;
        else simbolo = true;
    }

    return mayuscula && minuscula && numero && simbolo;
}

// Generar alertas de contraseñas débiles
void GenerarAlertas() {
    bool hayDebiles = false;

    cout << "\n--- ALERTAS DE SEGURIDAD ---\n";

    for (int i = 0; i < contrasenas.size(); i++) {
        if (!VerificarContrasena(contrasenas[i])) {
            cout << "Usuario: " << usuarios[i]
                 << " -> CONTRASENA DEBIL\n";
            hayDebiles = true;
        }
    }

    if (!hayDebiles) {
        cout << "Todas las contrasenas son seguras.\n";
    }
}

// Mostrar usuarios registrados
void MostrarUsuarios() {
    cout << "\n--- USUARIOS REGISTRADOS ---\n";

    if (usuarios.empty()) {
        cout << "No hay usuarios registrados.\n";
        return;
    }

    for (int i = 0; i < usuarios.size(); i++) {
        cout << i + 1 << ". " << usuarios[i] << endl;
    }
}
