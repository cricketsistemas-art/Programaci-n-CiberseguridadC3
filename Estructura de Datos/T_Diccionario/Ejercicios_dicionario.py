dispositivo_red = {     
    'IP': ' 192.168 .1.10',     
    'Hostname': 'Firewall-Corp',    
    'Estado': 'Activo' 
}       
print("Hostname:", dispositivo_red['Hostname'])     
dispositivo_red['Ubicación'] = 'Centro de Datos'    
dispositivo_red['Estado'] = 'Inactivo'  
print("Diccionario actualizado:", dispositivo_red)                                                             