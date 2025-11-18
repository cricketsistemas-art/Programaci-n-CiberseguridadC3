import tkinter as tk
from tkinter import ttk, messagebox
import re

class GestorContrasenas:
    def _init_(self, root):
        self.root = root
        self.root.title("Gestor de Contraseñas Seguras")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Lista para almacenar usuarios registrados
        self.usuarios = []

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="Gestor de Contraseñas Seguras", 
                         font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
        titulo.pack(pady=20)

        # Frame principal
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10)

        # Usuario
        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_usuario = tk.Entry(frame, font=("Arial", 12), width=30)
        self.entry_usuario.grid(row=0, column=1, pady=10, padx=10)

        # Contraseña
        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.entry_password = tk.Entry(frame, font=("Arial", 12), width=30, show="*")
        self.entry_password.grid(row=1, column=1, pady=10, padx=10)

        # Botones
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        btn_registrar = tk.Button(btn_frame, text="Registrar Usuario", font=("Arial", 12, "bold"),
                                 bg="#3498db", fg="white", width=20, command=self.registrar_usuario)
        btn_registrar.grid(row=0, column=0, padx=10)

        btn_verificar = tk.Button(btn_frame, text="Verificar Contraseña", font=("Arial", 12, "bold"),
                                 bg="#e67e22", fg="white", width=20, command=self.verificar_solo_contrasena)
        btn_verificar.grid(row=0, column=1, padx=10)

        # Área de resultado
        tk.Label(self.root, text="Resultado de la verificación:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", padx=50)
        
        self.text_resultado = tk.Text(self.root, height=8, width=60, font=("Courier", 11), state="disabled",
                                     bg="white", relief="sunken", bd=2)
        self.text_resultado.pack(pady=10, padx=50)

        # Lista de usuarios registrados
        tk.Label(self.root, text="Usuarios Registrados:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", padx=50, pady=(20,5))
        
        self.lista_usuarios = tk.Listbox(self.root, height=6, font=("Arial", 11), selectbackground="#3498db")
        self.lista_usuarios.pack(padx=50, fill="x")

    def evaluar_fuerza_contrasena(self, password):
        puntaje = 0
        sugerencias = []

        if len(password) >= 8:
            puntaje += 1
        else:
            sugerencias.append("• Mínimo 8 caracteres")

        if re.search(r"[a-z]", password):
            puntaje += 1
        else:
            sugerencias.append("• Al menos una letra minúscula")

        if re.search(r"[A-Z]", password):
            puntaje += 1
        else:
            sugerencias.append("• Al menos una letra MAYÚSCULA")

        if re.search(r"\d", password):
            puntaje += 1
        else:
            sugerencias.append("• Al menos un número")

        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            puntaje += 1
        else:
            sugerencias.append("• Al menos un carácter especial")

        # Definir nivel
        if puntaje <= 2:
            nivel = "MUY DÉBIL"
            color = "red"
        elif puntaje == 3:
            nivel = "DÉBIL"
            color = "orange"
        elif puntaje == 4:
            nivel = "FUERTE"
            color = "green"
        else:
            nivel = "MUY FUERTE"
            color = "darkgreen"

        return nivel, puntaje, sugerencias, color

    def mostrar_resultado(self, mensaje):
        self.text_resultado.config(state="normal")
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(tk.END, mensaje)
        self.text_resultado.config(state="disabled")

    def registrar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()

        if not usuario or not password:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        if any(u["usuario"] == usuario for u in self.usuarios):
            messagebox.showerror("Error", "Este usuario ya está registrado")
            return

        nivel, puntaje, sugerencias, color = self.evaluar_fuerza_contrasena(password)

        if puntaje <= 2:
            if not messagebox.askyesno("Contraseña Débil", 
                f"La contraseña es {nivel}\n\n¿Deseas registrarla de todos modos?"):
                return

        # Registrar usuario
        self.usuarios.append({"usuario": usuario, "contraseña": password, "fuerza": nivel})
        self.lista_usuarios.insert(tk.END, f"{usuario} → {nivel}")

        # Mostrar resultado
        resultado = f"USUARIO REGISTRADO CON ÉXITO\n\n"
        resultado += f"Usuario: {usuario}\n"
        resultado += f"Fuerza: {nivel} ({puntaje}/5)\n"
        if sugerencias and puntaje < 5:
            resultado += "\nSugerencias para mejorar:\n" + "\n".join(sugerencias)

        self.mostrar_resultado(resultado)
        messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente")

        # Limpiar campos
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def verificar_solo_contrasena(self):
        password = self.entry_password.get()
        if not password:
            messagebox.showwarning("Error", "Ingresa una contraseña para verificar")
            return

        nivel, puntaje, sugerencias, color = self.evaluar_fuerza_contrasena(password)

        resultado = f"ANÁLISIS DE CONTRASEÑA\n\n"
        resultado += f"Fuerza: {nivel} ({puntaje}/5)\n\n"
        
        if puntaje >= 4:
            resultado += "¡Excelente contraseña!\nMuy segura."
        elif puntaje == 3:
            resultado += "Contraseña aceptable, pero puede mejorar."
        else:
            resultado += "¡CONTRASEÑA DÉBIL!\nSe recomienda cambiarla."
        
        if sugerencias:
            resultado += "\n\nPara mayor seguridad:\n" + "\n".join(sugerencias)

        self.mostrar_resultado(resultado)


# Ejecutar la aplicación
if __name__ == "_main_":
    root = tk.Tk()
    app = GestorContrasenas(root)
    root.mainloop() 