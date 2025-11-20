
class Usuario:
    def __init__(self, nombre, edad):
        """Inicializa los atributos nombre y edad del usuario."""
        self.nombre = nombre
        self.edad = edad

    def mostrar_datos(self):
        """Muestra los datos del usuario."""
        print(f"Nombre: {self.nombre}, Edad: {self.edad}")

# Ejemplo de uso
if __name__ == "__main__":
    usuario1 = Usuario("Juan", 30)
    usuario1.mostrar_datos()  # Salida: Nombre: Juan, Edad: 30
