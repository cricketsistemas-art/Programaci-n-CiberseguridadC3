
class Estudiante:
    def __init__(self, nombre, calificaciones):
        """
        Inicializa un nuevo estudiante con un nombre y una lista de calificaciones.

        :param nombre: str - Nombre del estudiante
        :param calificaciones: list - Lista de calificaciones del estudiante
        """
        self.nombre = nombre
        self.calificaciones = calificaciones

    def calcular_promedio(self):
        """
        Calcula el promedio de las calificaciones del estudiante.

        :return: float - Promedio de las calificaciones
        """
        if not self.calificaciones:
            return 0.0  # Retorna 0 si no hay calificaciones

        return sum(self.calificaciones) / len(self.calificaciones)

# Ejemplo de uso
if __name__ == "__main__":
    estudiante1 = Estudiante("Juan", [85, 90, 78, 92])
    promedio = estudiante1.calcular_promedio()
    print(f"El promedio de {estudiante1.nombre} es: {promedio:.2f}")
