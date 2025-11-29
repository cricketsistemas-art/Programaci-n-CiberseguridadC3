class Empleado:
    def __init__(self, nombre, salario):
        """Inicializa un empleado con nombre y salario."""
        self.nombre = nombre
        self.salario = salario

    def calcular_bono(self):
        """Método que debe ser implementado en las clases hijas."""
        raise NotImplementedError("Este método debe ser implementado por las clases hijas.")

class Gerente(Empleado):
    def calcular_bono(self):
        """Calcula el bono del gerente como el 20% del salario."""
        return self.salario * 0.20

class Tecnico(Empleado):
    def calcular_bono(self):
        """Calcula el bono del técnico como el 10% del salario."""
        return self.salario * 0.10

# Ejemplo de uso
if __name__ == "__main__":
    gerente = Gerente("Alice", 5000)
    tecnico = Tecnico("Bob", 3000)

    print(f"Bono del gerente {gerente.nombre}: {gerente.calcular_bono()}")
    print(f"Bono del técnico {tecnico.nombre}: {tecnico.calcular_bono()}")
