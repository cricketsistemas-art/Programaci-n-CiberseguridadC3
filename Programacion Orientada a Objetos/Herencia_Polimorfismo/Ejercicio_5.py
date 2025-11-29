class Dispositivo:
    def encender(self):
        """Método para encender el dispositivo."""
        raise NotImplementedError("Este método debe ser sobreescrito por las clases hijas.")

class Laptop(Dispositivo):
    def encender(self):
        """Encender la laptop."""
        return "La laptop se ha encendido."

class Telefono(Dispositivo):
    def encender(self):
        """Encender el teléfono."""
        return "El teléfono se ha encendido."

# Ejemplos de uso
if __name__ == "__main__":
    # Crear instancias de Laptop y Telefono
    mi_laptop = Laptop()
    mi_telefono = Telefono()

    # Encender los dispositivos
    print(mi_laptop.encender())  # Salida: La laptop se ha encendido.
    print(mi_telefono.encender())  # Salida: El teléfono se ha encendido.