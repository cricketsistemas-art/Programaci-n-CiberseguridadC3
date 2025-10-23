#Ingresa el monto de una compra. Si es mayor a 500 aplica un 10% de descuento, sino paga precio normal. 
monto = float(input("Ingresa el monto de la compra: "))
if monto > 500:
    descuento = monto * 0.10
    total = monto - descuento
    print(f"Se aplicó un descuento de {descuento:.2f}. Total a pagar: {total:.2f}")     
else:
    print(f"No se aplicó descuento. Total a pagar: {monto:.2f}")