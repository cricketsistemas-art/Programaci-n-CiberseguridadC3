#Adivina el número secreto (ejemplo: 7).    
secreto = 7
adivina = int(input("Adivina el número secreto (entre 1 y 10): "))
while adivina != secreto:       
    print("¡Incorrecto! Intenta de nuevo.")
    adivina = int(input("Adivina el número secreto (entre 1 y 10): "))  
print("¡Felicidades! ¡Has adivinado el número secreto!")