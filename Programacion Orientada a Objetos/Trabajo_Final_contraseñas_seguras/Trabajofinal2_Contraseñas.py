"""
Gestor de Contraseñas (Tkinter)
Archivo: gestor_contraseñas_tkinter.py

Características:
- Interfaz Tkinter para agregar, buscar, mostrar y borrar entradas.
- Generador de contraseñas seguras con opciones (longitud, usar símbolos/números/mayúsculas).
- Almacenamiento cifrado del «vault» (archivo) usando cryptography.Fernet.
- Derivación de clave desde contraseña maestra con PBKDF2HMAC y una sal guardada.

Requisitos:
- Python 3.8+
- Instalar la librería cryptography: pip install cryptography

Uso:
1) Ejecuta el archivo: python gestor_contraseñas_tkinter.py
2) Si es la primera vez, crea una contraseña maestra. Esa será necesaria para abrir el vault.
3) Guarda y administra tus contraseñas. El archivo cifrado se llama 'vault.enc' y la sal 'vault.salt'.

Nota de seguridad: Este es un ejemplo educativo. Para uso sensible, revisa y mejora la gestión de claves y backups.
"""

from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import json
import os
import base64
import secrets
import string

# Intentamos importar cryptography; si no está, avisamos.
try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
except Exception as e:
    raise ImportError("La librería 'cryptography' es obligatoria. Instálala con: pip install cryptography")

VAULT_FILE = 'vault.enc'
SALT_FILE = 'vault.salt'

backend = default_backend()

# --- Funciones de cifrado / descifrado ---

def derive_key(password: str, salt: bytes) -> bytes:
    password_bytes = password.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=backend
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key


def generate_salt() -> bytes:
    return secrets.token_bytes(16)


def load_salt() -> bytes:
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, 'rb') as f:
            return f.read()
    else:
        salt = generate_salt()
        with open(SALT_FILE, 'wb') as f:
            f.write(salt)
        return salt


def encrypt_data(data: dict, fernet: Fernet) -> bytes:
    raw = json.dumps(data).encode('utf-8')
    return fernet.encrypt(raw)


def decrypt_data(token: bytes, fernet: Fernet) -> dict:
    try:
        raw = fernet.decrypt(token)
        return json.loads(raw.decode('utf-8'))
    except InvalidToken:
        raise

# --- Funciones de manejo de vault ---

def load_vault(fernet: Fernet) -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, 'rb') as f:
        encrypted = f.read()
    return decrypt_data(encrypted, fernet)


def save_vault(data: dict, fernet: Fernet):
    encrypted = encrypt_data(data, fernet)
    with open(VAULT_FILE, 'wb') as f:
        f.write(encrypted)

# --- Generador de contraseñas ---

def generar_contrasena(length=16, use_upper=True, use_digits=True, use_symbols=True) -> str:
    alphabet = string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += '!@#$%^&*()-_=+[]{};:,.<>?'
    # Asegurar que contiene al menos un carácter de cada tipo elegido
    while True:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Validaciones mínimas
        if use_upper and not any(c.isupper() for c in pwd):
            continue
        if use_digits and not any(c.isdigit() for c in pwd):
            continue
        if use_symbols and not any(c in '!@#$%^&*()-_=+[]{};:,.<>?' for c in pwd):
            continue
        return pwd

# --- Interfaz gráfica ---

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestor de Contraseñas - Tkinter')
        self.root.geometry('760x520')

        # Variables
        self.master_password = None
        self.fernet = None
        self.vault = {}

        # Build UI
        self.build_login_screen()

    def build_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        Label(frame, text='Gestor de Contraseñas', font=('Helvetica', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0,15))
        Label(frame, text='Contraseña maestra:', anchor='w').grid(row=1, column=0, sticky='w')
        self.mp_entry = Entry(frame, show='*', width=30)
        self.mp_entry.grid(row=1, column=1, pady=5)

        btn_login = Button(frame, text='Abrir vault', command=self.open_vault)
        btn_login.grid(row=2, column=0, pady=10)
        btn_new = Button(frame, text='Crear nuevo vault', command=self.create_new_vault)
        btn_new.grid(row=2, column=1, pady=10)

        Label(frame, text='(Si olvidaste la contraseña maestra, no podrás recuperar los datos.)', fg='red').grid(row=3, column=0, columnspan=2, pady=(10,0))

    def create_new_vault(self):
        pw = self.mp_entry.get().strip()
        if not pw:
            messagebox.showwarning('Aviso', 'Introduce una contraseña maestra para crear el vault.')
            return
        if os.path.exists(VAULT_FILE):
            if not messagebox.askyesno('Confirmar', 'Ya existe un vault. ¿Deseas sobrescribirlo?'):
                return
        salt = load_salt()
        key = derive_key(pw, salt)
        self.fernet = Fernet(key)
        self.master_password = pw
        self.vault = {}
        save_vault(self.vault, self.fernet)
        messagebox.showinfo('Listo', 'Se creó el vault cifrado.')
        self.build_main_screen()

    def open_vault(self):
        pw = self.mp_entry.get().strip()
        if not pw:
            messagebox.showwarning('Aviso', 'Introduce la contraseña maestra.')
            return
        salt = load_salt()
        key = derive_key(pw, salt)
        fernet = Fernet(key)
        try:
            vault = load_vault(fernet)
        except InvalidToken:
            messagebox.showerror('Error', 'Contraseña maestra incorrecta o vault corrupto.')
            return
        self.master_password = pw
        self.fernet = fernet
        self.vault = vault
        self.build_main_screen()

    def build_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Left panel: form
        left = Frame(self.root, padx=10, pady=10)
        left.pack(side=LEFT, fill=Y)

        Label(left, text='Añadir / Editar entrada', font=('Helvetica', 14)).grid(row=0, column=0, columnspan=2, pady=(0,10))
        Label(left, text='Etiqueta (ej: Gmail):').grid(row=1, column=0, sticky='w')
        self.label_entry = Entry(left, width=30)
        self.label_entry.grid(row=1, column=1, pady=3)

        Label(left, text='Usuario:').grid(row=2, column=0, sticky='w')
        self.user_entry = Entry(left, width=30)
        self.user_entry.grid(row=2, column=1, pady=3)

        Label(left, text='Contraseña:').grid(row=3, column=0, sticky='w')
        self.pw_entry = Entry(left, width=30)
        self.pw_entry.grid(row=3, column=1, pady=3)

        self.show_var = IntVar(value=0)
        Checkbutton(left, text='Mostrar contraseña', variable=self.show_var, command=self.toggle_show).grid(row=4, column=1, sticky='w')

        Label(left, text='Notas:').grid(row=5, column=0, sticky='nw')
        self.notes_text = Text(left, width=30, height=6)
        self.notes_text.grid(row=5, column=1, pady=3)

        # Generador
        Label(left, text='Generador de contraseñas', font=('Helvetica', 12)).grid(row=6, column=0, columnspan=2, pady=(10,0))
        Label(left, text='Longitud:').grid(row=7, column=0, sticky='w')
        self.len_spin = Spinbox(left, from_=8, to=64, width=5)
        self.len_spin.grid(row=7, column=1, sticky='w')

        self.var_upper = IntVar(value=1)
        self.var_digits = IntVar(value=1)
        self.var_symbols = IntVar(value=1)
        Checkbutton(left, text='Mayúsculas', variable=self.var_upper).grid(row=8, column=1, sticky='w')
        Checkbutton(left, text='Números', variable=self.var_digits).grid(row=9, column=1, sticky='w')
        Checkbutton(left, text='Símbolos', variable=self.var_symbols).grid(row=10, column=1, sticky='w')

        Button(left, text='Generar', command=self.usar_generador).grid(row=11, column=1, pady=5, sticky='e')
        Button(left, text='Guardar entrada', command=self.guardar_entrada).grid(row=12, column=1, pady=8, sticky='e')

        # Right panel: lista y búsqueda
        right = Frame(self.root, padx=10, pady=10)
        right.pack(side=LEFT, fill=BOTH, expand=True)

        top_search = Frame(right)
        top_search.pack(fill=X)
        Label(top_search, text='Buscar:').pack(side=LEFT)
        self.search_var = StringVar()
        Entry(top_search, textvariable=self.search_var).pack(side=LEFT, fill=X, expand=True, padx=5)
        Button(top_search, text='Ir', command=self.buscar).pack(side=LEFT)
        Button(top_search, text='Mostrar todo', command=self.mostrar_todo).pack(side=LEFT, padx=5)

        # Treeview para mostrar entradas
        columns = ('usuario', 'nota')
        self.tree = ttk.Treeview(right, columns=columns, show='headings')
        self.tree.heading('usuario', text='Usuario')
        self.tree.heading('nota', text='Notas')
        self.tree.bind('<Double-1>', self.on_tree_double)
        self.tree.pack(fill=BOTH, expand=True, pady=(10,0))

        bottom_buttons = Frame(right)
        bottom_buttons.pack(fill=X, pady=8)
        Button(bottom_buttons, text='Ver contraseña', command=self.ver_contrasena).pack(side=LEFT)
        Button(bottom_buttons, text='Eliminar', command=self.eliminar).pack(side=LEFT, padx=5)
        Button(bottom_buttons, text='Cerrar sesión', command=self.cerrar_sesion).pack(side=RIGHT)

        self.mostrar_todo()

    def toggle_show(self):
        if self.show_var.get():
            self.pw_entry.config(show='')
        else:
            self.pw_entry.config(show='*')

    def usar_generador(self):
        length = int(self.len_spin.get())
        pwd = generar_contrasena(length=length, use_upper=bool(self.var_upper.get()), use_digits=bool(self.var_digits.get()), use_symbols=bool(self.var_symbols.get()))
        self.pw_entry.delete(0, END)
        self.pw_entry.insert(0, pwd)

    def guardar_entrada(self):
        label = self.label_entry.get().strip()
        user = self.user_entry.get().strip()
        pwd = self.pw_entry.get().strip()
        notes = self.notes_text.get('1.0', END).strip()
        if not label or not pwd:
            messagebox.showwarning('Aviso', 'La etiqueta y la contraseña son obligatorias.')
            return
        # Guardar en el vault
        self.vault[label] = {'usuario': user, 'contrasena': pwd, 'notas': notes}
        save_vault(self.vault, self.fernet)
        messagebox.showinfo('Guardado', f'Entrada "{label}" guardada.')
        self.limpiar_form()
        self.mostrar_todo()

    def limpiar_form(self):
        self.label_entry.delete(0, END)
        self.user_entry.delete(0, END)
        self.pw_entry.delete(0, END)
        self.notes_text.delete('1.0', END)

    def mostrar_todo(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for label, data in sorted(self.vault.items()):
            notas = data.get('notas', '')
            usuario = data.get('usuario', '')
            self.tree.insert('', END, iid=label, values=(usuario, notas))

    def buscar(self):
        term = self.search_var.get().strip().lower()
        if not term:
            self.mostrar_todo()
            return
        for i in self.tree.get_children():
            self.tree.delete(i)
        for label, data in sorted(self.vault.items()):
            if term in label.lower() or term in data.get('usuario', '').lower() or term in data.get('notas', '').lower():
                self.tree.insert('', END, iid=label, values=(data.get('usuario',''), data.get('notas','')))

    def on_tree_double(self, event):
        item = self.tree.focus()
        if not item:
            return
        data = self.vault.get(item)
        if not data:
            return
        # Rellenar formulario con datos
        self.label_entry.delete(0, END)
        self.label_entry.insert(0, item)
        self.user_entry.delete(0, END)
        self.user_entry.insert(0, data.get('usuario',''))
        self.pw_entry.delete(0, END)
        self.pw_entry.insert(0, data.get('contrasena',''))
        self.notes_text.delete('1.0', END)
        self.notes_text.insert('1.0', data.get('notas',''))

    def ver_contrasena(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning('Aviso', 'Selecciona una entrada de la lista.')
            return
        data = self.vault.get(item)
        if not data:
            messagebox.showerror('Error', 'Entrada no encontrada.')
            return
        # Mostrar en diálogo (advertencia sobre copiar al portapapeles)
        if messagebox.askyesno('Mostrar contraseña', '¿Deseas ver la contraseña? (Se recomienda no usar en equipo público)'):
            messagebox.showinfo(f'Contraseña — {item}', data.get('contrasena',''))

    def eliminar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning('Aviso', 'Selecciona una entrada.')
            return
        if not messagebox.askyesno('Confirmar', f'¿Eliminar "{item}" definitivamente?'):
            return
        del self.vault[item]
        save_vault(self.vault, self.fernet)
        self.mostrar_todo()

    def cerrar_sesion(self):
        self.master_password = None
        self.fernet = None
        self.vault = {}
        self.build_login_screen()


if __name__ == '__main__':
    root = Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
