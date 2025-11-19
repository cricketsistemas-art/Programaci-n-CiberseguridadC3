import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from cryptography.fernet import Fernet
import secrets
import string
import os

class GestorContraseñas:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Gestor de Contraseñas Seguro")
        self.root.geometry("600x400")

        # Generar clave de cifrado si no existe
        self.crear_clave_cifrado()

        # Crear la base de datos y tabla
        self.crear_base_datos()

        # Variables para los campos de entrada
        self.nombre_servicio = tk.StringVar()
        self.contraseña = tk.StringVar()
        self.generada_contraseña = tk.StringVar()

        self.crear_interfaz()

    def crear_clave_cifrado(self):
        """Crear o cargar la clave de cifrado"""
        if not os.path.exists('clave.key'):
            key = Fernet.generate_key()
            with open('clave.key', 'wb') as key_file:
                key_file.write(key)
        self.cipher_suite = Fernet(open('clave.key', 'rb').read())

    def crear_base_datos(self):
        """Crear la base de datos SQLite y la tabla de contraseñas"""
        conn = sqlite3.connect('contraseñas.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contraseñas
            (servicio TEXT PRIMARY KEY, contraseña BLOB)
        ''')
        conn.commit()
        conn.close()

    def generar_contraseña(self):
        """Generar una contraseña segura"""
        caracteres = string.ascii_letters + string.digits + string.punctuation
        longitud = 16
        nueva_contraseña = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        self.generada_contraseña.set(nueva_contraseña)

    def agregar_contraseña(self):
        """Agregar una nueva contraseña al sistema"""
        servicio = self.nombre_servicio.get()
        contra = self.contraseña.get() or self.generada_contraseña.get()
        
        if not servicio or not contra:
            messagebox.showerror("Error", "Por favor ingrese todos los campos")
            return

        try:
            # Cifrar la contraseña
            contra_cifrada = self.cipher_suite.encrypt(contra.encode())
            
            # Guardar en la base de datos
            conn = sqlite3.connect('contraseñas.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contraseñas VALUES (?, ?)', (servicio, contra_cifrada))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", "Contraseña guardada exitosamente")
            self.limpiar_campos()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Este servicio ya existe")

    def obtener_contraseña(self):
        """Obtener una contraseña específica"""
        servicio = self.nombre_servicio.get()
        
        if not servicio:
            messagebox.showerror("Error", "Por favor ingrese el nombre del servicio")
            return

        try:
            conn = sqlite3.connect('contraseñas.db')
            cursor = conn.cursor()
            cursor.execute('SELECT contraseña FROM contraseñas WHERE servicio = ?', (servicio,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                # Descifrar la contraseña
                contra_descifrada = self.cipher_suite.decrypt(resultado[0]).decode()
                messagebox.showinfo("Contraseña", f"Contraseña para {servicio}: {contra_descifrada}")
            else:
                messagebox.showerror("Error", "Servicio no encontrado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def listar_contraseñas(self):
        """Listar todas las contraseñas almacenadas"""
        try:
            conn = sqlite3.connect('contraseñas.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contraseñas')
            
            resultados = cursor.fetchall()
            conn.close()
            
            mensaje = "Lista de Contraseñas:\n\n"
            for servicio, contra_cifrada in resultados:
                contra_descifrada = self.cipher_suite.decrypt(contra_cifrada).decode()
                mensaje += f"Servicio: {servicio}\nContraseña: {contra_descifrada}\n\n"
            
            messagebox.showinfo("Contraseñas Almacenadas", mensaje)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_campos(self):
        """Limpiar todos los campos de entrada"""
        self.nombre_servicio.set("")
        self.contraseña.set("")
        self.generada_contraseña.set("")

    def crear_interfaz(self):
        """Crear la interfaz gráfica"""
        # Frame principal
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campo de nombre del servicio
        ttk.Label(frame, text="Servicio:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.nombre_servicio).grid(row=0, column=1, padx=5, pady=5)

        # Campo de contraseña
        ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.contraseña, show="*").grid(row=1, column=1, padx=5, pady=5)

        # Botón para generar contraseña
        ttk.Button(frame, text="Generar Contraseña", command=self.generar_contraseña).grid(row=2, column=0, columnspan=2, pady=5)

        # Botón para agregar contraseña
        ttk.Button(frame, text="Agregar Contraseña", command=self.agregar_contraseña).grid(row=3, column=0, columnspan=2, pady=5)

        # Botón para obtener contraseña
        ttk.Button(frame, text="Obtener Contraseña", command=self.obtener_contraseña).grid(row=4, column=0, columnspan=2, pady=5)

        # Botón para listar contraseñas
        ttk.Button(frame, text="Listar Contraseñas", command=self.listar_contraseñas).grid(row=5, column=0, columnspan=2, pady=5)

        # Botón para limpiar campos
        ttk.Button(frame, text="Limpiar Campos", command=self.limpiar_campos).grid(row=6, column=0, columnspan=2, pady=5)

    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GestorContraseñas()
    app.ejecutar()