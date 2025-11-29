class Vehiculo:
    """Clase base para todos los vehículos."""
    
    def mover(self):
        """Método que debe ser implementado por las clases hijas."""
        raise NotImplementedError("Este método debe ser implementado por las clases hijas.")


class Carro(Vehiculo):
    """Clase que representa un carro, hereda de Vehiculo."""
    
    def mover(self):
        """Implementación del método mover para un carro."""
        return "El carro se está moviendo por la carretera."


class Bicicleta(Vehiculo):
    """Clase que representa una bicicleta, hereda de Vehiculo."""
    
    def mover(self):
        """Implementación del método mover para una bicicleta."""
        return "La bicicleta se está moviendo por el sendero."


# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancias de Carro y Bicicleta
    mi_carro = Carro()
    mi_bicicleta = Bicicleta()
    
    # Llamar al método mover de cada vehículo
    print(mi_carro.mover())       # Salida: El carro se está moviendo por la carretera.
    print(mi_bicicleta.mover())   # Salida: La bicicleta se está moviendo por el sendero.