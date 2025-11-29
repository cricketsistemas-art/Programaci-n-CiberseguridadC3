import math

class Figura:
    """Clase base para figuras geométricas."""
    
    def area(self):
        """Método para calcular el área. Debe ser implementado en las clases hijas."""
        raise NotImplementedError("Este método debe ser implementado por las clases hijas.")

class Circulo(Figura):
    """Clase para representar un círculo."""
    
    def __init__(self, radio):
        """Inicializa el círculo con un radio dado."""
        self.radio = radio
    
    def area(self):
        """Calcula el área del círculo."""
        return math.pi * (self.radio ** 2)

class Cuadrado(Figura):
    """Clase para representar un cuadrado."""
    
    def __init__(self, lado):
        """Inicializa el cuadrado con un lado dado."""
        self.lado = lado
    
    def area(self):
        """Calcula el área del cuadrado."""
        return self.lado ** 2

# Ejemplos de uso
if __name__ == "__main__":
    circulo = Circulo(5)
    print(f"Área del círculo: {circulo.area()}")  # Área del círculo: 78.53981633974483

    cuadrado = Cuadrado(4)
    print(f"Área del cuadrado: {cuadrado.area()}")  # Área del cuadrado: 16