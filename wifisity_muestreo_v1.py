#########################################################################################################
#####################################           WIFISITY           ######################################
#########################################################################################################
#                                   Desarrollado por Ariel Bujan                                        #
#########################################################################################################
# Por la presente se autoriza, de forma gratuita, a cualquier persona que obtenga una copia de este     #
# software y de los archivos de documentación asociados, para tratar con el Software sin restricción    #
# alguna, incluidos, sin limitación, los derechos de utilizar, copiar, modificar, fusionar, publicar,   #
# y/o distribuir copias del Software, y a permitir que las personas a las que se facilite el Software,  #
# con sujeción a las siguientes condiciones:                                                            #
#########################################################################################################
# EL SOFTWARE SE PROPORCIONA "AS IS", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUIDAS,      #
# ENTRE OTRAS, LAS GARANTÍAS DE COMERCIABILIDAD, IDONEIDAD PARA UN FIN DETERMINADO Y NO INFRACCIÓN.     #
# EN NINGÚN CASO LOS AUTORES NI LOS TITULARES DE LOS DERECHOS DE AUTOR SERÁN RESPONSABLES DE NINGUNA    #
# RESPONSABILIDAD, YA SEA CONTRACTUAL, EXTRACONTRACTUAL O DE OTRO TIPO, DERIVADA DE, O EN RELACIÓN CON  #
# EL MAL USO DEL SOFTWARE U OTRAS OPERACIONES RELACIONADAS CON EL SOFTWARE.                             #
#########################################################################################################
# LIBRERÍAS
#--------------------------------------------------------------------------------------------------------
import subprocess
import time
import os
import sys
import signal
import tkinter as tk
from PIL import ImageGrab
from tkinter.simpledialog import askinteger

#--------------------------------------------------------------------------------------------------------
# CONFIGURACIÓN
#--------------------------------------------------------------------------------------------------------
TIEMPO_MUESTREO = 2
def config(): # CONFIGURACIÓN - INICIO
    print("DEBUG | Configurando placa de red")
    os.system("ifconfig wlan0 down 2>/dev/null") #Apagar la interfaz de la placa Wi-Fi
    os.system("iwconfig wlan0 mode monitor 2>/dev/null") #Cambiar la placa Wi-Fi al modo monitor
    os.system("ifconfig wlan0 up 2>/dev/null") #Encender nuevamente la interfaz de la placa Wi-Fi
    os.system("airmon-ng check kill 2>/dev/null") #En caso haberlos, matar el servicio y se solucionará
    os.system("airmon-ng start wlan0 2>/dev/null") #Reiniciar el servicio
    time.sleep(1)

def def_handler(sig, frame):# Función para manejar la señal SIGINT (Ctrl+C)
    print("\n[!] Ctrl+C. Saliendo del programa.")
    print("DEBUG | Restaurando configuración de la placa de red")
    os.system("ifconfig wlan0 down 2>/dev/null") #Apagar la interfaz de la placa Wi-Fi
    os.system("iwconfig wlan0 mode managed 2>/dev/null") #Cambiar la placa Wi-Fi al modo managed
    os.system("ifconfig wlan0 up 2>/dev/null") #Encender nuevamente la interfaz de la placa Wi-Fi
    os.system("systemctl restart network-online.target") #Reiniciar el servicio
    os.system("(cat SSID.temp | sort -fu >> SSID.json)") # Eliminar las SSIDs repetidas
    if os.path.exists("SSID.temp"):
        os.remove("SSID.temp") # Eliminar el archivo SSID.temp
    sys.exit(1)
    
#--------------------------------------------------------------------------------------------------------
# MAPEO
#--------------------------------------------------------------------------------------------------------
class MatrixNavigator:
    def __init__(self, master, rows, cols, cell_size):
        self.master = master
        self.rows = rows
        self.cols = cols
        #self.pointer_pos = [rows-1, 1]  # Posición inicial en la esquina inferior izquierda (En caso de usar esta opción, es necesario adaptar el gráfico)
        self.pointer_pos = [1, 1]  # Posición inicial
        self.direction = "right"  # Dirección inicial hacia la derecha
        self.path = set()
        self.points = []  # Lista para almacenar los puntos adicionales
        self.cell_size = cell_size
        self.create_canvas()
        self.create_widgets()  # Se llama a un nuevo método para crear widgets
        self.bind_keys()
        self.blink_pointer()
        self.update_title()

    def generar_archivo(self, nombre, datos):
        with open(nombre, 'w') as file:
            file.write(datos)

    def agregar_archivo(self, nombre, datos):
        with open(nombre, 'a') as file:
            file.write(datos)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.master, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="#D9D9D9")
        self.canvas.pack()

    def create_widgets(self):
        # Se crea el botón "+" y se asocia a la función add_point
        self.add_button = tk.Button(self.master, text="+", command=self.add_point)
        self.add_button.pack(side=tk.LEFT)  # Se coloca a la izquierda

        # Se crea el botón "Photo" y se asocia a la función save_screenshot
        self.photo_button = tk.Button(self.master, text="Photo", command=self.save_screenshot)
        self.photo_button.pack(side=tk.LEFT)  # Se coloca a la izquierda

    def update_pointer(self):
        self.canvas.delete("all")
        for i in range(1,self.rows+1):
            for j in range(1,self.cols+1):
                x0, y0 = (j-1) * self.cell_size, (i-1) * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                if (i, j) in self.path:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#0094FF", outline="")
                elif i == self.pointer_pos[0] and j == self.pointer_pos[1]:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#C60000", outline="")
                    self.path.add((i, j))
        for point in self.points:  # Graficar puntos adicionales
            x, y = point
            x0, y0 = (x-1) * self.cell_size, (y-1) * self.cell_size
            x1, y1 = x0 + self.cell_size, y0 + self.cell_size
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#4BC12A", outline="")

    def move_pointer_forward(self):
        next_pos = self.get_next_position_forward()
        if self.is_valid_position(next_pos):
            self.pointer_pos = next_pos
            self.update_pointer()
            self.update_title()
            #print("pos[0]:",self.pointer_pos[0]," - pos[1]:",self.pointer_pos[1])
            self.muestreo(next_pos)

    def move_pointer_backward(self):
        next_pos = self.get_next_position_backward()
        if self.is_valid_position(next_pos):
            self.pointer_pos = next_pos
            self.update_pointer()
            self.update_title()
            self.muestreo(next_pos)

    def get_next_position_forward(self):
        if self.direction == "up":
            return [self.pointer_pos[0] - 1, self.pointer_pos[1]]
        elif self.direction == "down":
            return [self.pointer_pos[0] + 1, self.pointer_pos[1]]
        elif self.direction == "left":
            return [self.pointer_pos[0], self.pointer_pos[1] - 1]
        elif self.direction == "right":
            return [self.pointer_pos[0], self.pointer_pos[1] + 1]

    def get_next_position_backward(self):
        if self.direction == "up":
            return [self.pointer_pos[0] + 1, self.pointer_pos[1]]
        elif self.direction == "down":
            return [self.pointer_pos[0] - 1, self.pointer_pos[1]]
        elif self.direction == "left":
            return [self.pointer_pos[0], self.pointer_pos[1] + 1]
        elif self.direction == "right":
            return [self.pointer_pos[0], self.pointer_pos[1] - 1]

    def is_valid_position(self, pos):
        return 1 <= pos[0] < self.rows and 1 <= pos[1] < self.cols

    def turn_right(self):
        if self.direction == "up":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "up"
        self.update_title()

    def turn_left(self):
        if self.direction == "up":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "up"
        self.update_title()

    def blink_pointer(self):
        current_color = "#C60000" if (self.pointer_pos[0], self.pointer_pos[1]) not in self.path else "#D9D9D9"
        self.update_pointer()
        self.master.after(500, self.blink_pointer)

    def bind_keys(self):
        self.master.bind("<Up>", lambda event: self.move_pointer_forward())
        self.master.bind("<Down>", lambda event: self.move_pointer_backward())
        self.master.bind("<Right>", lambda event: self.turn_right())
        self.master.bind("<Left>", lambda event: self.turn_left())
        self.master.bind("<Control-asterisk>", self.save_screenshot)  # Bind Control + * key to save screenshot

    def save_screenshot(self, event=None):
        x0 = self.master.winfo_rootx()
        y0 = self.master.winfo_rooty()
        x1 = x0 + self.master.winfo_width()
        y1 = y0 + self.master.winfo_height()
        ImageGrab.grab().crop((x0, y0, x1, y1)).save("screenshot.png")
        print("Se guardó una captura de pantalla con el nombre: screenshot.png")

    def update_title(self):
        direction_symbol = {"up": "↑", "down": "↓", "right": "→", "left": "←"}
        direction_text = direction_symbol[self.direction]
        self.master.title("Mapa del recorrido realizado: Posición X: {} Y: {} Dirección: {}".format(self.pointer_pos[1], self.pointer_pos[0], direction_text))

    def add_point(self, event=None):
        x = askinteger("Coordenada X", "Ingrese la coordenada X del punto:")
        y = askinteger("Coordenada Y", "Ingrese la coordenada Y del punto:")
        if x is not None and y is not None:
            self.points.append([x, y])
            self.update_pointer()

    def muestreo(self, pos): # Funcionalidad básica de muestreo
        output_filename = f"output-{pos[0]}_{pos[1]}"
        command = ["airodump-ng", "wlan0", "--output-format", "csv", "-w", output_filename]
        output_filename = f"output-{pos[0]}_{pos[1]}-01.csv" # Actualiza la variable porque airodumo incluye -01
        networks = {} # Parsear resultados
        weakest_signals = {} # Diccionario para almacenar la señal más debilitada por BSSID

        process = subprocess.Popen(command)
        time.sleep(TIEMPO_MUESTREO) # Esperar N segundos antes de detener el proceso
        process.terminate() # Terminar el proceso
        process.wait() # Esperar a que el proceso termine completamente

        with open(output_filename, "r") as file:
            lines = file.readlines()
            #print("DEBUG | lines:",lines)
            for line in lines[2:]:  # Omitir las primeras dos líneas del encabezado
                parts = line.strip().split(",")
                #print("DEBUG | parts: ",parts)
                if len(parts) >= 14:  # Verifica si hay suficientes campos
                    bssid = parts[0].strip()
                    power = parts[8].strip()
                    ssid = parts[13].strip()
                    if ssid != "SSID" and ssid != "":
                        networks[bssid] = ssid
                        #print("DEBUG | networks[",bssid,"]:",ssid)
                    if bssid not in weakest_signals or weakest_signals[bssid] > power:
                        weakest_signals[bssid] = power
                        #print("DEBUG | weakest_signals[",bssid,"] = ", weakest_signals[bssid],"Nuevo valor: ", power)
        #file.close()

        # Tomar un registro de los SSID-BSSID para el post-procesado
        for bssid, ssid in networks.items():
            self.agregar_archivo("SSID.temp", f"{bssid};{ssid}\n")

        # Tomar una muestra de las redes WiFi disponibles en el punto x,y
        for bssid, power in weakest_signals.items():
            bssid_sanitized = bssid.replace(':', '')
            #print("bssid:",bssid," - power:",power)
            self.agregar_archivo(f"{bssid_sanitized}.txt", f"{pos[0]} {pos[1]} {power}\n")
        os.system("kill -9 $(ps -ef | grep airodump | awk '{print $2}') 2>/dev/null") # Matar el proceso airodump (en caso de no haberse cerrado bien)

    # Ctrl+C
    signal.signal(signal.SIGINT,def_handler)

def main():
    config()
    root = tk.Tk()
    root.geometry("1200x800")  # Tamaño de la ventana
    navigator = MatrixNavigator(root, 81, 121, 9)  # Tamaño de la celda
    root.mainloop()
    #while True:
    #    time.sleep(1)  # Espera de 1 segundo antes de imprimir el siguiente mensaje

if __name__ == "__main__":
    main()
