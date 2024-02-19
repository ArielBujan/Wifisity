# Versión básica del código, con simulación de movimiento sobre una matriz de NxM
#------------------------------------------------------------------------------------------------
# LIBRERÍAS
#------------------------------------------------------------------------------------------------
import subprocess
import time
import os
#------------------------------------------------------------------------------------------------
# VARIABLES
#------------------------------------------------------------------------------------------------
TIEMPO_MUESTREO = 5
posX = 5
posY = 6

#------------------------------------------------------------------------------------------------
# CONFIGURACIÓN - INICIO
#------------------------------------------------------------------------------------------------
print("DEBUG | Configurando placa de red")
os.system("ifconfig wlan0 down 2>/dev/null") #Apagar la interfaz de la placa Wi-Fi
os.system("iwconfig wlan0 mode monitor 2>/dev/null") #Cambiar la placa Wi-Fi al modo monitor
os.system("ifconfig wlan0 up 2>/dev/null") #Encender nuevamente la interfaz de la placa Wi-Fi
os.system("airmon-ng check kill 2>/dev/null") #En caso haberlos, matar el servicio y se solucionará
os.system("airmon-ng start wlan0 2>/dev/null") #Reiniciar el servicio
time.sleep(1)

#------------------------------------------------------------------------------------------------
# WIFISITY
#------------------------------------------------------------------------------------------------
# Tomar una muestra de las redes WiFi disponibles en el punto x,y
comando1 = "airodump-ng wlan0 | awk '{print $2\";\"$1}' | grep '-'"
for x in range(1, posX+1):
    for y in range(1, posY+1):
        print("DEBUG | X:", x," - Y:", y)
        with open(f"archivo_temp.txt", "w") as archivo_temp:
            proceso = subprocess.Popen(comando1, shell=True, stdout=archivo_temp) # Ejecutar el comando airodump-ng y almacenar la salida en archivo.temp
            time.sleep(TIEMPO_MUESTREO) # Esperar N segundos antes de detener el proceso
            proceso.terminate() # Terminar el proceso
            archivo_temp.close() # Cerrar archivo temporal

        # Obtener el nombre del archivo por BSSID y almacenar la perdida de señal por BSSID en cada ubicación (x y loss)
        os.system(f"for linea in $(cat archivo_temp.txt | sort -r | tr -d ':' | awk -F ';' '!seen[$2]++'); do \
            longitud=$(echo \"$linea\" | cut -d \";\" -f 2 | wc -c); \
            if [ \"$longitud\" -eq 13 ]; then \
                filename=$(echo \"$linea\" | cut -d ';' -f 2); \
                echo '{x} {y}' $linea | cut -d \";\" -f 1 >> $filename.txt; \
            fi \
        done")

        os.remove("archivo_temp.txt") # Eliminar el archivo.temp
        os.system("kill -9 $(ps -ef | grep airodump | awk '{print $2}') 2>/dev/null") # Matar el proceso airodump (en caso de no haberse cerrado bien)

# Tomar un registro de los SSID-BSSID para el post-procesado
comando2 = ["airodump-ng", "wlan0", "--output-format", "csv", "--write", "output"]
process = subprocess.Popen(comando2)
time.sleep(2*TIEMPO_MUESTREO)
process.terminate()

# Parsear resultados de la lista de redes
networks = {}
with open("output-01.csv", "r") as file:
    lines = file.readlines()
    for line in lines[2:]:  # Skip the header rows
        parts = line.strip().split(",")
        if len(parts) >= 14:  # Verifica si hay suficientes campos
            bssid = parts[0].strip()
            ssid = parts[13].strip()
            if ssid != "SSID" and ssid != "":
                networks[bssid] = ssid

# Guardar el resultado en el archivo SSID.txt
with open("SSID.txt", "w") as file:
    for bssid, ssid in networks.items():
        file.write(f"{bssid}: {ssid}\n")
os.remove("output-01.csv") # Eliminar el output-01.csv

#------------------------------------------------------------------------------------------------
# CONFIGURACIÓN - FIN
#------------------------------------------------------------------------------------------------
print("DEBUG | Restaurando configuración de la placa de red")
os.system("ifconfig wlan0 down 2>/dev/null") #Apagar la interfaz de la placa Wi-Fi
os.system("iwconfig wlan0 mode managed 2>/dev/null") #Cambiar la placa Wi-Fi al modo managed
os.system("ifconfig wlan0 up 2>/dev/null") #Encender nuevamente la interfaz de la placa Wi-Fi
os.system("systemctl restart network-online.target") #Reiniciar el servicio
time.sleep(1)
#------------------------------------------------------------------------------------------------