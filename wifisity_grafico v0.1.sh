#!/bin/bash

#sudo apt update --fix-missing
#sudo apt-get install gnuplot
#https://gnuplot.sourceforge.net/demo/heatmaps.html

# Comprobar si hay archivos .txt en el directorio actual
shopt -s nullglob
archivos=(*.txt)

if (( ${#archivos[@]} == 0 )); then
    echo "No se encontraron archivos .txt en el directorio actual."
    exit 1
fi

# Iterar sobre los archivos .txt
for archivo in "${archivos[@]}"; do
    if [[ -f "$archivo" ]]; then
        echo "Graficando $archivo..."
        gnuplot -e "set terminal pngcairo enhanced font 'arial,10' size 800,800; \
	set output '${archivo%.*}_heatmap.png'; \
	unset key; set view map scale 1; set style data lines;unset cbtics; \
	set palette defined (-100 'dark-red', -75 'red', -50 'orange', -25 'yellow', 0 'green'); \
	set dgrid 15,15 gauss  kdensity 4, 4; \
	set border 31; set tmargin 4;\
	set yrange[0:10]; set xrange [0:10]; set cbrange [0:100]; \
	set title 'Mapa de calor de señal WiFi'; \
        set xlabel 'Posición X'; set ylabel 'Posición Y'; \
	set view map; \
	splot '$archivo' using 1:2:(3) with pm3d, '' using 1:2:(3) with points lc "black" pt 5 ps 0.5 nogrid"
    else
        echo "No se encontraron archivos .txt en el directorio actual."
        exit 1
    fi
done
echo "Finalizado!"