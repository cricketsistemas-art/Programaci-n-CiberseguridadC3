import tkinter as tk
from tkinter import messagebox
import re

class GestorContrasenas:
    def _init_(self, root):
        self.root = root
        self.root.title("Gestor de Contraseñas Seguras")
        self.root.geometry("620x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#ecf0f1")

        self.usuarios = []  # Aquí se guardan los usuarios registrados
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(self.root, text="GESTOR DE CONTRASEÑAS SEGURAS", 
                         font=("Arial", 18, "bold"), bg="#ecf0f1", fg="#2c3e50")
        titulo.pack(pady=20)

        # Frame para los campos
        frame = tk.Frame(self.root, bg="#ecf0f1")
        frame.pack(pady=10)

        # Campo Usuario
        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_usuario = tk.Entry(frame, font=("Arial", 12), width=35)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)

        # Campo Contraseña
        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_password = tk.Entry(frame, font=("Arial", 12), width=35, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(self.root, bg="#ecf0f1")
        btn_frame.pack(pady=20)

        btn_registrar = tk.Button(btn_frame, text="Registrar Usuario", font=("Arial", 12, "bold"),
                                  bg="#27ae60", fg="white", width=20, command=self.registrar_usuario)
        btn_registrar.grid(row=0, column=0, padx=15)

        btn_verificar = tk.Button(btn_frame, text="Verificar Contraseña", font=("Arial", 12, "bold"),
                                  bg="#e74c3c", fg="white", width=20, command=self.verificar_solo_contrasena)
        btn_verificar.grid(row=0, column=1, padx=15)

        # Área de resultado
        tk.Label(self.root, text="Resultado de la verificación:", font=("Arial", 12, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", padx=40, pady=(20,5))

        self.text_resultado = tk.Text(self.root, height=10, width=70, font=("Consolas", 11), 
                                     state="disabled", bg="white", relief="solid", bd=1)
        self.text_resultado.pack(pady=10, padx=40)

        # Lista de usuarios registrados
        tk.Label(self.root, text="Usuarios Registrados:", font=("Arial", 12, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(anchor="w", padx=40, pady=(15,5))

        self.lista_usuarios = tk.Listbox(self.root, height=8, font=("Arial", 11), selectbackground="#3498db")
        self.lista_usuarios.pack(padx=40, fill="x", pady=5)

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

        # Nivel de fuerza
        if puntaje <= 2:
            nivel = "MUY DÉBIL"
        elif puntaje == 3:
            nivel = "DÉBIL"
        elif puntaje == 4:
            nivel = "FUERTE"
        else:
            nivel = "MUY FUERTE"

        return nivel, puntaje, sugerencias

    def mostrar_resultado(self, mensaje):
        self.text_resultado.config(state="normal")
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(tk.END, mensaje)
        self.text_resultado.config(state="disabled")

    def registrar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()

        if not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")
            return

        if any(u["usuario"] == usuario for u in self.usuarios):
            messagebox.showerror("Error", "Este usuario ya existe")
            return

        nivel, puntaje, sugerencias = self.evaluar_fuerza_contrasena(password)

        if puntaje <= 2:
            if not messagebox.askyesno("Contraseña débil", 
                f"La contraseña es {nivel} ({puntaje}/5)\n\n"
                "¿Deseas registrarla igual?"):
                return

        # Registrar
        self.usuarios.append({"usuario": usuario, "contraseña": password, "fuerza": nivel})
        self.lista_usuarios.insert(tk.END, f"{usuario}  →  {nivel}")

        resultado = f"USUARIO REGISTRADO CORRECTAMENTE\n\n"
        resultado += f"Usuario: {usuario}\n"
        resultado += f"Nivel de seguridad: {nivel} ({puntaje}/5)\n\n"
        if sugerencias:
            resultado += "Sugerencias para mejorar:\n" + "\n".join(sugerencias)

        self.mostrar_resultado(resultado)
        messagebox.showinfo("Éxito", f"Usuario '{usuario}' registrado correctamente")

        # Limpiar campos
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def verificar_solo_contrasena(self):
        password = self.entry_password.get()
        if not password:
            messagebox.showwarning("Campo vacío", "Escribe una contraseña para verificar")
            return

        nivel, puntaje, sugerencias = self.evaluar_fuerza_contrasena(password)

        resultado = f"ANÁLISIS DE CONTRASEÑA\n\n"
        resultado += f"Fuerza: {nivel} ({puntaje}/5)\n\n"

        if puntaje >= 4:
            resultado += "¡EXCELENTE! Contraseña muy segura."
        elif puntaje == 3:
            resultado += "Contraseña aceptable, pero puede mejorar."
        else:
            resultado += "¡ADVERTENCIA! Contraseña débil o muy débil."

        if sugerencias:
            resultado += "\n\nRecomendaciones:\n" + "\n".join(sugerencias)

        self.mostrar_resultado(resultado)


# ==================== EJECUCIÓN CORRECTA ====================
if __name__ == "_main_":
    root = tk.Tk()
    app = GestorContrasenas(root)
    root.mainloop()
# =======================