# Wifisity
Esta herramienta permite generar mapas de calor a partir del análisis de redes inalámbricas, utilizando como base la ejecución del comando **airodump-ng**, el cual escanea las redes Wi-Fi cercanas y proporciona información sobre sus señales y otros parámetros relevantes.
De este modo. el usuario puede visualizar y analizar la intensidad de la señal para cada una de las redes Wi-Fi cercanas, con el objetivo de planificar, diseñar y optimizar la cobertura de red inalámbrica en un área específica.

#Instalar tkinter
- `apt-get install python3-tk`

# Ejecutar el script de muestreo
- `python3 wifisity_muestreo.py`

Realizar el descubrimiento de la red a través de un recorrido físico de las instalaciones:
> - Mover hacia adelante con la flecha de arriba
> - Mover hacia atras con la flecha de abajo
> - Girar dirección hacia la derecha con la flecha derecha
> - Girar dirección hacia la izquierda con la flecha izquierda
> - Tomar captura del recorrido realizado con el boton "Photo" con Ctrl+*
> - Agregar punto de interes en el mapa con el boton "+"
> - Finalizar el recorrido con Ctrl+C

![image](https://github.com/ArielBujan/Wifisity/assets/8824124/079c4e20-4878-4a0c-81fb-6c8323ab230f)

# Gráficar mapa de calor de las redes inalambricas
- `python3 wifisity_graficoInterp.py`

Se generará un mapa de calor para cada red SSID, identificandolas como `{BSSID}.png`
![image](https://github.com/ArielBujan/Wifisity/assets/8824124/b58a6b15-a7de-4dd7-b18c-d018c5ce3bc5)
![image](https://github.com/ArielBujan/Wifisity/assets/8824124/ad0e58b6-dc6f-45a4-9bf3-f0232171ba84)

# Spray Password | Brute-Forcing Authentication
 A la salida del script de muestreo ejecutar el siguiente comando:
- `cat SSID.json | cut -d ";" -f 2 >> SSID.txt`

Luego enviar el listado de redes a brute-forcear con sus respectivas contraseñas candidatas:
- `python3 wifisity_spray.py SSID.txt -p '12345678'`
- `python3 wifisity_spray.py SSID.txt -P passwords.txt`

Los resultados se mostrarán en el archivo `resultados.txt` del siguiente modo:
> - SSID_WiFi-XXXXXX:12345678:`[-] ~~~~~ Conexión fallida`
> - SSID2_WiFi-XXXXX:12345678:`[+] Conexión exitosa!!`
