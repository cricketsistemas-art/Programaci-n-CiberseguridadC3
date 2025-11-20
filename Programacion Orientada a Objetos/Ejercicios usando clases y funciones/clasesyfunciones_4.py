
class CuentaBancaria:
    def __init__(self, titular, balance=0):
        """Inicializa la cuenta bancaria con un titular y un balance inicial."""
        self.titular = titular
        self.balance = balance

    def depositar(self, cantidad):
        """Deposita una cantidad en la cuenta."""
        if cantidad > 0:
            self.balance += cantidad
            print(f"Se han depositado {cantidad}. Nuevo balance: {self.balance}.")
        else:
            print("La cantidad a depositar debe ser mayor que cero.")

    def retirar(self, cantidad):
        """Retira una cantidad de la cuenta si hay suficiente balance."""
        if cantidad > 0:
            if cantidad <= self.balance:
                self.balance -= cantidad
                print(f"Se han retirado {cantidad}. Nuevo balance: {self.balance}.")
            else:
                print("Fondos insuficientes para realizar el retiro.")
        else:
            print("La cantidad a retirar debe ser mayor que cero.")

# Ejemplo de uso
if __name__ == "__main__":
    cuenta = CuentaBancaria("Juan Pérez", 1000)
    cuenta.depositar(500)  # Deposita 500
    cuenta.retirar(200)     # Retira 200
    cuenta.retirar(1500)    # Intenta retirar más de lo que hay en la cuenta
