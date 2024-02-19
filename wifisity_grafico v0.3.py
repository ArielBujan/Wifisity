import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Obtener la lista de archivos .txt en el directorio actual
archivos = [archivo for archivo in os.listdir() if archivo.endswith('.txt')]

# Verificar si hay archivos .txt
if not archivos:
    print("ERROR: No se encontraron archivos .txt en el directorio actual")
    exit(1)

# Definir la escala de colores personalizada
#colores = ['darkred', 'red', 'orange', 'yellow', 'green']
colores = ['#F8696B', '#FB8D72', '#FCAC78', '#FFE784', '#8BC97D']
valores = [-100, -75, -50, -25, 0]

n_colores = len(colores)
n_valores = len(valores)

# Interpolación de colores
if n_colores < n_valores:
    raise ValueError("La cantidad de colores debe ser igual o mayor que la cantidad de valores")
elif n_colores > n_valores:
    # Interpolar colores para tener una escala gradual
    colores_interp = []
    for i in range(n_valores - 1):
        colores_interp.append(colores[i])
        colores_interp.append(((np.array(plt.get_cmap('hot')(i/n_valores)[:3]) + np.array(plt.get_cmap('hot')((i+1)/n_valores)[:3]))/2).tolist())
    colores_interp.append(colores[-1])
else:
    colores_interp = colores

# Definir la escala de colores personalizada
cmap_personalizado = LinearSegmentedColormap.from_list("custom_colormap", colores_interp)

# Iterar sobre los archivos .txt
for archivo in archivos:
    print("Procesando", archivo)
    if os.path.isfile(archivo):
        with open(archivo, 'r') as f:
            # Leer las líneas del archivo
            lineas = f.readlines()
        # Inicializar listas para almacenar los datos
        x = []
        y = []
        weight = []

        # Procesar cada línea del archivo
        for linea in lineas:
            datos = linea.strip().split()
            x.append(int(datos[0]))
            y.append(int(datos[1]))
            weight.append(float(datos[2]))

        # Crear una cuadrícula para el mapa de calor
        x_grid, y_grid = np.meshgrid(np.arange(1, max(x) + 1), np.arange(1, max(y) + 1))

        # Crear una matriz de pesos para el mapa de calor
        weight_grid = np.zeros_like(x_grid, dtype=float)
        for i in range(len(x)):
            weight_grid[y[i] - 1, x[i] - 1] = weight[i]

        # Graficar el mapa de calor con la escala de colores personalizada
        print("Graficando...")
        plt.figure(figsize=(10, 8))
        plt.imshow(weight_grid, cmap=cmap_personalizado, interpolation='nearest', origin='lower', extent=[0.5, max(x) + 0.5, 0.5, max(y) + 0.5])
        plt.colorbar(label='Perdida de señal')
        plt.title('Mapa de Calor')
        plt.xlabel('Posición X')
        plt.ylabel('Posición Y')
        plt.grid(True)

        # Guardar el mapa de calor como una imagen PNG
        nombre_salida = archivo.split('.')[0] + '_heatmap.png'
        plt.savefig(nombre_salida)
        print("Finalizado: Se ha guardado el mapa de calor como:", nombre_salida)
        plt.show()
    else:
        print("ERROR: No se encontró el archivo ", archivo)
        continue
