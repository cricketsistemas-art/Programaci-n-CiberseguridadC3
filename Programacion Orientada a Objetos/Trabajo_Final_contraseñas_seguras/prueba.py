import os
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
import string
import pyperclip  # ya esta instalado

    # ==================== CONFIGURACIÓN ====================
DB_FILE = "passwords.db.enc"
SALT_SIZE = 16
IV_SIZE = 16
KEY_SIZE = 32  # AES-256
ITERATIONS = 600000  # Recomendado en 2025

    # ==================== FUNCIONES DE CIFRADO ====================
def derivar_clave(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            iterations=ITERATIONS,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

def cifrar_datos(data: str, password: str) -> bytes:
        salt = os.urandom(SALT_SIZE)
        iv = os.urandom(IV_SIZE)
        key = derivar_clave(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(salt + iv + ciphertext)

def descifrar_datos(encrypted_data: bytes, password: str) -> str:
        data = base64.b64decode(encrypted_data)
        salt = data[:SALT_SIZE]
        iv = data[SALT_SIZE:SALT_SIZE + IV_SIZE]
        ciphertext = data[SALT_SIZE + IV_SIZE:]

        key = derivar_clave(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return data.decode()

    # ==================== GESTOR DE CONTRASEÑAS ====================
class PasswordManager:
        def _init_(self):
            self.entries = []  # Lista de diccionarios: {"sitio": ..., "usuario": ..., "contraseña": ...}
            self.master_password = None
            self.archivo_existe = os.path.exists(DB_FILE)

        def crear_nueva_base(self, password):
            self.master_password = password
            self.entries = []
            self.guardar()

        def cargar_base(self, password):
            if not os.path.exists(DB_FILE):
                return False
            try:
                with open(DB_FILE, "rb") as f:
                    encrypted = f.read()
                json_str = descifrar_datos(encrypted, password)
                self.entries = json.loads(json_str)
                self.master_password = password
                return True
            except Exception as e:
                messagebox.showerror("Error", "Contraseña maestra incorrecta o archivo corrupto.")
                return False

        def guardar(self):
            if not self.master_password:
                return
            json_str = json.dumps(self.entries, indent=2)
            encrypted = cifrar_datos(json_str, self.master_password)
            with open(DB_FILE, "wb") as f:
                f.write(encrypted)

        def agregar_entrada(self, sitio, usuario, contraseña):
            self.entries.append({"sitio": sitio, "usuario": usuario, "contraseña": contraseña})
            self.guardar()

        def buscar(self, texto):
            texto = texto.lower()
            return [e for e in self.entries if texto in e["sitio"].lower() or texto in e["usuario"].lower()]

    # ==================== GENERADOR DE CONTRASEÑAS ====================
def generar_contraseña(longitud=20, incluir_simbolos=True):
        caracteres = string.ascii_letters + string.digits
        if incluir_simbolos:
            caracteres += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return ''.join(secrets.choice(caracteres) for _ in range(longitud))

    # ==================== INTERFAZ GRÁFICA ====================
class PasswordManagerGUI:
        def _init_(self):
            self.pm = PasswordManager()
            self.root = tk.Tk()
            self.root.title("Gestor de Contraseñas Seguro")
            self.root.geometry("800x600")
            self.root.resizable(False, False)

            if self.pm.archivo_existe:
                self.pedir_master_password()
            else:
                self.crear_nueva_base()

        def pedir_master_password(self):
            password = simpledialog.askstring("Contraseña Maestra", "Ingresa tu contraseña maestra:", show='*')
            if password is None:
                self.root.quit()
                return
            if self.pm.cargar_base(password):
                self.mostrar_interfaz_principal()
            else:
                if messagebox.askretrycancel("Error", "¿Quieres intentarlo de nuevo?"):
                    self.pedir_master_password()

        def crear_nueva_base(self):
            if self.pm.archivo_existe:
                if not messagebox.askyesno("Archivo existente", "¿Sobrescribir la base de datos existente?"):
                    self.root.quit()
                    return

            password = simpledialog.askstring("Nueva Base", "Crea una contraseña maestra fuerte:", show='*')
            if not password or len(password) < 8:
                messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres.")
                self.crear_nueva_base()
                return

            password2 = simpledialog.askstring("Confirmar", "Repite la contraseña maestra:", show='*')
            if password != password2:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                self.crear_nueva_base()
                return

            self.pm.crear_nueva_base(password)
            messagebox.showinfo("Éxito", "¡Base de datos creada correctamente!")
            self.mostrar_interfaz_principal()

        def mostrar_interfaz_principal(self):
            for widget in self.root.winfo_children():
                widget.destroy()

            # Barra de búsqueda
            tk.Label(self.root, text="Buscar:", font=("Helvetica", 12)).pack(pady=10)
            self.entry_buscar = tk.Entry(self.root, width=50, font=("Helvetica", 12))
            self.entry_buscar.pack()
            self.entry_buscar.bind('<KeyRelease>', lambda e: self.actualizar_lista())

            # Botón agregar
            btn_agregar = tk.Button(self.root, text="Agregar Nueva Contraseña", bg="#4CAF50", fg="white",
                                    font=("Helvetica", 12), command=self.ventana_agregar)
            btn_agregar.pack(pady=10)

            # Treeview para mostrar entradas
            columns = ("sitio", "usuario", "contraseña")
            # Treeview para mostrar entradas
            columns = ("sitio", "usuario", "contraseña")
            self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
            
            self.tree.heading("sitio", text="Sitio Web / App")
            self.tree.heading("usuario", text="Usuario / Email")
            self.tree.heading("contraseña", text="Contraseña")
            
            self.tree.column("sitio", width=250)
            self.tree.column("usuario", width=250)
            self.tree.column("contraseña", width=250, anchor="center")

            self.tree.pack(padx=20, pady=10, fill="both", expand=True)

            # Botones de acción en cada fila
            self.tree.bind("Double-Button-1", self.copiar_contraseña)

            # Botón eliminar seleccionado
            btn_eliminar = tk.Button(self.root, text="Eliminar Seleccionado", bg="#f44336", fg="white",
                                    command=self.eliminar_entrada)
            btn_eliminar.pack(pady=5)

            self.actualizar_lista()

        def actualizar_lista(self):
            for item in self.tree.get_children():
                self.tree.delete(item)

            texto = self.entry_buscar.get()
            resultados = self.pm.buscar(texto) if texto else self.pm.entries

            for entry in resultados:
                # Mostramos asteriscos en la tabla por seguridad
                self.tree.insert("", "end", values=(entry["sitio"], entry["usuario"], "••••••••••••"))

        def copiar_contraseña(self, event=None):
            seleccion = self.tree.selection()
            if not seleccion:
                return
            item = self.tree.item(seleccion[0])["values"]
            sitio = item[0]

            # Buscar la contraseña real
            for e in self.pm.entries:
                if e["sitio"] == sitio:
                    pyperclip.copy(e["contraseña"])
                    messagebox.showinfo("Copiado", f"Contraseña de '{sitio}' copiada al portapapeles")
                    break

        def ventana_agregar(self):
            ventana = tk.Toplevel(self.root)
            ventana.title("Agregar Nueva Contraseña")
            ventana.geometry("500x400")
            ventana.resizable(False, False)
            ventana.grab_set()

            tk.Label(ventana, text="Sitio Web / Aplicación:", font=("Helvetica", 12)).pack(pady=10)
            entry_sitio = tk.Entry(ventana, width=50)
            entry_sitio.pack(pady=5)

            tk.Label(ventana, text="Usuario o Email:", font=("Helvetica", 12)).pack(pady=10)
            entry_usuario = tk.Entry(ventana, width=50)
            entry_usuario.pack(pady=5)

            tk.Label(ventana, text="Contraseña:", font=("Helvetica", 12)).pack(pady=10)
            entry_pass = tk.Entry(ventana, width=50, show='*')
            entry_pass.pack(pady=5)

            def generar_y_llenar():
                nueva = generar_contraseña(20)
                entry_pass.delete(0, tk.END)
                entry_pass.insert(0, nueva)
                pyperclip.copy(nueva)
                messagebox.showinfo("Generada", "¡Contraseña segura generada y copiada al portapapeles!")

            btn_generar = tk.Button(ventana, text="Generar Contraseña Segura", bg="#2196F3", fg="white",
                                    command=generar_y_llenar)
            btn_generar.pack(pady=15)

            def guardar():
                sitio = entry_sitio.get().strip()
                usuario = entry_usuario.get().strip()
                contraseña = entry_pass.get()

                if not sitio or not usuario or not contraseña:
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return

                self.pm.agregar_entrada(sitio, usuario, contraseña)
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "¡Contraseña guardada correctamente!")
                ventana.destroy()

            btn_guardar = tk.Button(ventana, text="Guardar", bg="#4CAF50", fg="white", font=("Helvetica", 12), command=guardar)
            btn_guardar.pack(pady=20)

        def eliminar_entrada(self):
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar", "Por favor selecciona una entrada para eliminar")
                return

            item = self.tree.item(seleccion[0])["values"]
            sitio = item[0]

            if messagebox.askyesno("Confirmar", f"¿Eliminar la entrada de '{sitio}'?"):
                self.pm.entries = [e for e in self.pm.entries if e["sitio"] != sitio]
                self.pm.guardar()
                self.actualizar_lista()
                messagebox.showinfo("Eliminado", "Entrada eliminada correctamente")

        def run(self):
            self.root.mainloop()

    # ==================== EJECUTAR LA APLICACIÓN ====================
if __name__ == "_main_":
    app = PasswordManagerGUI()
    app.run()