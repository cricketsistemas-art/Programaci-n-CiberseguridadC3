class Animal:
    """Clase base que representa un animal."""
    
    def hablar(self):
        """Método que debe ser sobreescrito por las clases hijas."""
        raise NotImplementedError("Este método debe ser sobreescrito por las subclases.")


class Perro(Animal):
    """Clase que representa un perro, hereda de Animal."""
    
    def hablar(self):
        """Implementación del método hablar para un perro."""
        return "¡Guau!"


class Gato(Animal):
    """Clase que representa un gato, hereda de Animal."""
    
    def hablar(self):
        """Implementación del método hablar para un gato."""
        return "¡Miau!"


# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancias de Perro y Gato
    mi_perro = Perro()
    mi_gato = Gato()
    
    # Llamar al método hablar
    print("El perro dice:", mi_perro.hablar())  # Salida: El perro dice: ¡Guau!
    print("El gato dice:", mi_gato.hablar())    # Salida: El gato dice: ¡Miau!