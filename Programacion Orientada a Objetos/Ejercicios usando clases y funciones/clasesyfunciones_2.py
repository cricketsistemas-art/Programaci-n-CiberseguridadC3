
class Rectangulo:
    def __init__(self, base, altura):
        """Inicializa el rectángulo con base y altura."""
        self.base = base
        self.altura = altura

    def area(self):
        """Calcula y devuelve el área del rectángulo."""
        return self.base * self.altura

# Ejemplo de uso
if __name__ == "__main__":
    rectangulo = Rectangulo(5, 10)
    print(f"El área del rectángulo es: {rectangulo.area()}")  # Salida: El área del rectángulo es: 50
