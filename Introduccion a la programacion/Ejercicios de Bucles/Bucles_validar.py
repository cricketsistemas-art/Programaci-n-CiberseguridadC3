#Valida una contraseña. Mientras no sea '1234', vuelve a pedirla
contraseña = input("Introduce la contraseña: ")
while contraseña != "1234":     
    print("Contraseña incorrecta. Intenta de nuevo.")
    contraseña = input("Introduce la contraseña: ") 
print("¡Contraseña correcta!")