#Pide 10 números y calcula la suma total    
suma_total = 0
for _ in range(10):     
    numero = int(input("Ingrese un número: "))
    suma_total += numero    
print(f"La suma total de los 10 números ingresados es: {suma_total}")   