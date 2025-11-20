
import tkinter as tk
from tkinter import messagebox, simpledialog
import re

# Clase para el Gestor de Contraseñas
class PasswordManager:
    def __init__(self):
        self.users = {}  # Almacena usuarios y contraseñas

    def register_user(self, username, password):
        """Registra un nuevo usuario con su contraseña."""
        if username in self.users:
            return False  # El usuario ya existe
        self.users[username] = password
        return True

    def check_password_strength(self, password):
        """Verifica la fuerza de la contraseña."""
        if len(password) < 8:
            return "Débil: La contraseña debe tener al menos 8 caracteres."
        if not re.search("[a-z]", password):
            return "Débil: Debe contener al menos una letra minúscula."
        if not re.search("[A-Z]", password):
            return "Débil: Debe contener al menos una letra mayúscula."
        if not re.search("[0-9]", password):
            return "Débil: Debe contener al menos un número."
        if not re.search("[@#$%^&+=]", password):
            return "Débil: Debe contener al menos un carácter especial."
        return "Fuerte: La contraseña es segura."

    def generate_alerts(self):
        """Genera alertas para contraseñas débiles."""
        alerts = []
        for username, password in self.users.items():
            strength = self.check_password_strength(password)
            if "Débil" in strength:
                alerts.append(f"Alerta para {username}: {strength}")
        return alerts

    def get_users(self):
        """Devuelve la lista de usuarios registrados."""
        return list(self.users.keys())

# Clase para la interfaz gráfica
class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor de Contraseñas Seguras")
        self.master.geometry("600x400")
        self.master.configure(bg='lightblue')

        self.manager = PasswordManager()

        # Etiquetas y botones
        self.label = tk.Label(master, text="Gestor de Contraseñas", font=("Arial", 24), bg='lightblue')
        self.label.pack(pady=20)

        self.register_button = tk.Button(master, text="Registrar Usuario", command=self.register_user, bg='lightgreen')
        self.register_button.pack(pady=10)

        self.check_button = tk.Button(master, text="Verificar Contraseña", command=self.check_password, bg='lightyellow')
        self.check_button.pack(pady=10)

        self.alert_button = tk.Button(master, text="Generar Alertas", command=self.generate_alerts, bg='lightcoral')
        self.alert_button.pack(pady=10)

        self.view_button = tk.Button(master, text="Ver Usuarios Registrados", command=self.view_users, bg='lightblue')
        self.view_button.pack(pady=10)

    def register_user(self):
        """Solicita al usuario que ingrese un nombre de usuario y contraseña para registrarse."""
        username = simpledialog.askstring("Registrar Usuario", "Ingrese el nombre de usuario:")
        password = simpledialog.askstring("Registrar Contraseña", "Ingrese la contraseña:")
        if username and password:
            if self.manager.register_user(username, password):
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            else:
                messagebox.showwarning("Error", "El usuario ya existe.")

    def check_password(self):
        """Solicita al usuario que ingrese una contraseña para verificar su fuerza."""
        password = simpledialog.askstring("Verificar Contraseña", "Ingrese la contraseña a verificar:")
        if password:
            strength = self.manager.check_password_strength(password)
            messagebox.showinfo("Resultado de Verificación", strength)

    def generate_alerts(self):
        """Genera alertas para contraseñas débiles y las muestra."""
        alerts = self.manager.generate_alerts()
        if alerts:
            messagebox.showwarning("Alertas de Contraseña", "\n".join(alerts))
        else:
            messagebox.showinfo("Sin Alertas", "Todas las contraseñas son fuertes.")

    def view_users(self):
        """Muestra la lista de usuarios registrados."""
        users = self.manager.get_users()
        if users:
            messagebox.showinfo("Usuarios Registrados", "\n".join(users))
        else:
            messagebox.showinfo("Sin Usuarios", "No hay usuarios registrados.")

# Ejecución de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
