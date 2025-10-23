vulnerabilidades = ('SQL Injection', 'Cross-Site Scripting', 'Buffer Overflow', 'Denegación de Servicio')       
print("El segundo elemento de la tupla es:", vulnerabilidades[1])       
print("Los dos últimos elementos de la tupla son:", vulnerabilidades[-2:])  
try:            
    vulnerabilidades[1] = 'XSS'        
except TypeError as e:            
    print("Error al intentar modificar un elemento de la tupla:", e)    