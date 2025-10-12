Algoritmo  SistemaInventarioRed
    Definir num_equipos, i Como Entero
    Definir equipos, ips, ubicaciones, estados Como Cadena
    Definir opcion Como Entero
	
    Dimension equipos[100], ips[100], ubicaciones[100], estados[100]
    num_equipos <- 0
	
    Repetir
        Escribir "===== SISTEMA DE INVENTARIO DE RED ====="
        Escribir "1. Registrar equipo"
        Escribir "2. Mostrar inventario"
        Escribir "3. Generar alertas"
        Escribir "4. Salir"
        Escribir "========================================"
        Escribir "Ingrese una opción:"
        Leer opcion
		
        Segun opcion Hacer
            1:  // Registrar equipo
                Si num_equipos < 100 Entonces
                    num_equipos <- num_equipos + 1
                    Escribir "Ingrese nombre del equipo:"
                    Leer equipos[num_equipos]
                    Escribir "Ingrese ubicación:"
                    Leer ubicaciones[num_equipos]
                    Escribir "Ingrese IP:"
                    Leer ips[num_equipos]
                    Escribir "Ingrese estado (1=Activo / 0=Inactivo):"
                    Leer estados[num_equipos]
                    Escribir "Equipo registrado con éxito."
                SiNo
                    Escribir "Límite de equipos alcanzado."
                FinSi
				
            2:  // Mostrar inventario
                Si num_equipos = 0 Entonces
                    Escribir "No hay equipos registrados."
                SiNo
                    Escribir "===== INVENTARIO DE EQUIPOS ====="
                    Para i <- 1 Hasta num_equipos Con Paso 1 Hacer
                        Escribir "Equipo ", i, ": ", equipos[i]
                        Escribir "  IP: ", ips[i]
                        Escribir "  Ubicación: ", ubicaciones[i]
                        Escribir "  Estado: ", estados[i]
                        Escribir "----------------------------------"
                    FinPara
                FinSi
				
            3:  // Generar alertas
                Si num_equipos = 0 Entonces
                    Escribir "No hay equipos registrados para analizar."
                SiNo
                    Escribir "===== ALERTAS DE EQUIPOS INACTIVOS ====="
                    Para i <- 1 Hasta num_equipos Con Paso 1 Hacer
                        Si estados[i] = "0" Entonces
                            Escribir "? ALERTA: El equipo ", equipos[i], " (IP ", ips[i], ") está INACTIVO."
                        FinSi
                    FinPara
                    Escribir "========================================"
                FinSi
				
            4:
                Escribir "Saliendo del sistema..."
        FinSegun
		
    Hasta Que opcion = 4
FinAlgoritmo
