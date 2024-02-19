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
posX = 7
posY = 7

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
command = ["airodump-ng", "wlan0", "--output-format", "csv", "--write", "output"]
for x in range(1, posX+1):
    for y in range(1, posY+1):
        print("DEBUG | X:", x," - Y:", y)
        process = subprocess.Popen(command)
        time.sleep(TIEMPO_MUESTREO) # Esperar N segundos antes de detener el proceso
        process.terminate() # Terminar el proceso
        networks = {} # Parsear resultados
        weakest_signals = {} # Diccionario para almacenar la señal más debilitada por BSSID
        with open("output-01.csv", "r") as file:
            lines = file.readlines()
            for line in lines[2:]:  # Omitir las primeras dos líneas del encabezado
                parts = line.strip().split(",")
                #print("parts: ",parts)
                if len(parts) >= 14:  # Verifica si hay suficientes campos
                    bssid = parts[0].strip()
                    power = parts[8].strip()
                    ssid = parts[13].strip()
                    if ssid != "SSID" and ssid != "":
                        networks[bssid] = ssid
                    if bssid not in weakest_signals or weakest_signals[bssid] > power:
                        weakest_signals[bssid] = power

        # Tomar un registro de los SSID-BSSID para el post-procesado
        with open("SSID.temp", "a") as file:
            for bssid, ssid in networks.items():
                file.write(f"{bssid}:{ssid}\n")

        # Tomar una muestra de las redes WiFi disponibles en el punto x,y
        for bssid, power in weakest_signals.items():
            bssid_sanitized = bssid.replace(':', '')
            #print("bssid:",bssid," - power:",power)
            with open(f"{bssid_sanitized}.txt", "a") as file:
                file.write(f"{x} {y} {power}\n")  

        os.remove("output-01.csv") # Eliminar el output-*.csv            
        os.system("kill -9 $(ps -ef | grep airodump | awk '{print $2}') 2>/dev/null") # Matar el proceso airodump (en caso de no haberse cerrado bien)
        os.system("(cat SSID.temp | sort -fu >> SSID.txt; rm SSID.temp)") # Eliminar las SSIDs repetidas

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
