
class Coche:
    def __init__(self, marca, velocidad=0):
        """
        Inicializa un objeto Coche con una marca y una velocidad inicial.
        
        :param marca: str - La marca del coche.
        :param velocidad: int - La velocidad inicial del coche (por defecto es 0).
        """
        self.marca = marca
        self.velocidad = velocidad

    def aumentar_velocidad(self, incremento):
        """
        Aumenta la velocidad del coche en un valor dado.
        
        :param incremento: int - El valor por el cual se aumentará la velocidad.
        """
        self.velocidad += incremento
        print(f"La velocidad del coche {self.marca} ahora es {self.velocidad} km/h.")

# Ejemplo de uso
if __name__ == "__main__":
    mi_coche = Coche("Toyota")
    mi_coche.aumentar_velocidad(20)  # Aumenta la velocidad en 20 km/h
    mi_coche.aumentar_velocidad(15)  # Aumenta la velocidad en 15 km/h
