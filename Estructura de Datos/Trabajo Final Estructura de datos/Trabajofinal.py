#!/usr/bin/env python3
"""
Gestor de Contraseñas Seguras
Archivo: gestor_contrasenas.py

Funciones principales:
- RegistrarUsuario()
- VerificarContrasena()
- GenerarAlertas()
- Autenticación básica y almacenamiento en users.json con hash PBKDF2 (no se guarda la contraseña en texto plano).
"""

import json
import os
import re
import hashlib
import secrets
import getpass
from typing import Dict, Tuple, List

USERS_FILE = "users.json"
COMMON_PASSWORDS = {
    # una lista corta de ejemplos; en un proyecto real ampliar esta lista
    "123456", "password", "12345678", "qwerty", "abc123", "111111", "123456789", "12345", "iloveyou"
}

# ---------- Helpers para almacenamiento seguro ----------
def _load_users() -> Dict[str, Dict]:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_users(users: Dict[str, Dict]) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def _hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """
    Devuelve (salt_hex, hash_hex). Usa PBKDF2-HMAC-SHA256.
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    else:
        salt = bytes.fromhex(salt)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return salt.hex(), dk.hex()

def _verify_hash(password: str, salt_hex: str, hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return dk.hex() == hash_hex

# ---------- Funciones requeridas ----------
def VerificarContrasena(password: str) -> Dict[str, object]:
    """
    Verifica la fuerza de la contraseña.
    Devuelve un dict con:
      - 'fuerte': bool
      - 'puntuacion': int (0-5)
      - 'detalles': list de strings con observaciones
    Criterios:
      - Longitud >= 12
      - Mayúscula
      - Minúscula
      - Dígito
      - Carácter especial
      - No estar en lista de comunes
    """
    detalles: List[str] = []
    puntuacion = 0

    if len(password) >= 12:
        puntuacion += 1
    else:
        detalles.append("La contraseña tiene menos de 12 caracteres.")

    if re.search(r"[A-Z]", password):
        puntuacion += 1
    else:
        detalles.append("Falta letra mayúscula.")

    if re.search(r"[a-z]", password):
        puntuacion += 1
    else:
        detalles.append("Falta letra minúscula.")

    if re.search(r"[0-9]", password):
        puntuacion += 1
    else:
        detalles.append("Falta número.")

    if re.search(r"[^\w\s]", password):  # carácter especial
        puntuacion += 1
    else:
        detalles.append("Falta carácter especial (p. ej. !@#$).")

    if password.lower() in COMMON_PASSWORDS:
        detalles.append("La contraseña es demasiado común.")
        # penaliza si es común: reduce puntuacion si es alta
        if puntuacion > 0:
            puntuacion -= 1

    fuerte = puntuacion >= 4  # criterio configurable
    return {"fuerte": fuerte, "puntuacion": puntuacion, "detalles": detalles}

def GenerarAlertas(users: Dict[str, Dict]) -> List[str]:
    """
    Recorre los usuarios y genera alertas para contraseñas débiles.
    Devuelve una lista de mensajes de alerta.
    """
    alertas = []
    for username, info in users.items():
        # no tenemos la contraseña en texto; asumimos que guardamos un marcador 'last_strength' si existe
        # en este ejemplo, almacenamos 'evaluacion' al guardar. Si no existe, generamos alerta 'sin evaluación'.
        evaluacion = info.get("evaluacion")
        if evaluacion is None:
            alertas.append(f"[{username}] No se ha verificado la fortaleza de la contraseña.")
        else:
            if not evaluacion.get("fuerte", False):
                detalles = evaluacion.get("detalles", [])
                alertas.append(f"[{username}] CONTRASEÑA DÉBIL. Razones: {', '.join(detalles)}")
    return alertas

def RegistrarUsuario(username: str, password: str, confirm: bool = True) -> Tuple[bool, str]:
    """
    Registra un usuario (si no existe).
    - verifica fuerza con VerificarContrasena
    - guarda salt+hash en users.json junto con evaluación de fuerza
    Devuelve (exito, mensaje)
    """
    users = _load_users()
    if username in users:
        return False, "El usuario ya existe."

    ver = VerificarContrasena(password)
    salt_hex, hash_hex = _hash_password(password)
    users[username] = {
        "salt": salt_hex,
        "hash": hash_hex,
        "evaluacion": ver
    }
    _save_users(users)
    if ver["fuerte"]:
        return True, "Usuario registrado correctamente. Contraseña considerada FUERTE."
    else:
        return True, "Usuario registrado, pero la contraseña es DÉBIL. " + " ".join(ver["detalles"])

# ---------- Funciones adicionales útiles ----------
def AutenticarUsuario(username: str, password: str) -> bool:
    users = _load_users()
    info = users.get(username)
    if not info:
        return False
    return _verify_hash(password, info["salt"], info["hash"])

def listar_usuarios() -> List[str]:
    users = _load_users()
    return list(users.keys())

# ---------- Interfaz de consola simple ----------
def menu():
    print("=" * 40)
    print("Gestor de Contraseñas Seguras")
    print("=" * 40)
    print("1) Registrar usuario")
    print("2) Autenticar usuario")
    print("3) Listar usuarios")
    print("4) Generar alertas (contraseñas débiles)")
    print("5) Ver evaluación de un usuario")
    print("0) Salir")

def main_loop():
    while True:
        menu()
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            username = input("Usuario: ").strip()
            # usar getpass para no mostrar la contraseña en consola
            password = getpass.getpass("Contraseña: ")
            ok, msg = RegistrarUsuario(username, password)
            print(msg)
        elif opcion == "2":
            username = input("Usuario: ").strip()
            password = getpass.getpass("Contraseña: ")
            if AutenticarUsuario(username, password):
                print("Autenticación correcta.")
            else:
                print("Usuario o contraseña incorrecta.")
        elif opcion == "3":
            users = listar_usuarios()
            if not users:
                print("No hay usuarios registrados.")
            else:
                print("Usuarios registrados:")
                for u in users:
                    print(" -", u)
        elif opcion == "4":
            users = _load_users()
            alertas = GenerarAlertas(users)
            if not alertas:
                print("No hay alertas. Todas las contraseñas tienen evaluación o no hay usuarios.")
            else:
                print("ALERTAS:")
                for a in alertas:
                    print(a)
        elif opcion == "5":
            username = input("Usuario a consultar: ").strip()
            users = _load_users()
            info = users.get(username)
            if not info:
                print("Usuario no encontrado.")
            else:
                evalu = info.get("evaluacion", {})
                print("Evaluación para", username)
                print(" - Fuerte:", evalu.get("fuerte"))
                print(" - Puntuación:", evaluacion_get(evalu, "puntuacion"))
                print(" - Detalles:", ", ".join(evaluacion_get(evalu, "detalles")))
        elif opcion == "0":
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def evaluacion_get(evaluacion, key):
    """Pequeña función para evitar KeyError."""
    return evaluacion.get(key) if evaluacion else None

if __name__ == "_main_":
 main_loop()