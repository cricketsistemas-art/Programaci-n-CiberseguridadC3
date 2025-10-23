#Muestra la tabla de multiplicar de un número ingresado por el usuario  
num = int(input("Ingrese un número para ver su tabla de multiplicar: "))
print(f"Tabla de multiplicar del {num}:")   
for i in range(1, 11):
    resultado = num * i
    print(f"{num} x {i} = {resultado}") 