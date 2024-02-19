TIEMPO_MUESTREO=3
posX=5
posY=5
comando="airodump-ng wlan0"

ifconfig wlan0 down 2>/dev/null #Apagar la interfaz de la placa Wi-Fi
iwconfig wlan0 mode monitor 2>/dev/null #Cambiar la placa Wi-Fi al modo monitor
ifconfig wlan0 up 2>/dev/null #Encender nuevamente la interfaz de la placa Wi-Fi
airmon-ng check kill 2>/dev/null #En caso haberlos, matar el servicio y se solucionará
airmon-ng start wlan0 2>/dev/null #Reiniciar el servicio

for x in $(seq 1 $posX); do
    for y in $(seq 1 $posY); do
		echo "DEBUG | X:"$x" - Y:"$y
		$comando > auxiliary.temp &
		pid=$!
		sleep $TIEMPO_MUESTREO
		kill -15 $pid
		for z in $(cat auxiliary.temp | grep -v "Elapsed:\|<length:\|Quitting" | awk '{print $2 ";" $1}' | grep "-" | sort -r | sort -fuk 2);do
			filename=$(echo "$z" | cut -d ";" -f 2 | tr -d :) #echo "Filename:"$filename
			echo $y" "$x" "$z | cut -d ";" -f 1 >> $filename.txt
		done
	done
done

rm auxiliary.temp
ifconfig wlan0 down 2>/dev/null #Apagar la interfaz de la placa Wi-Fi
iwconfig wlan0 mode managed 2>/dev/null #Cambiar la placa Wi-Fi al modo managed
ifconfig wlan0 up 2>/dev/null #Encender nuevamente la interfaz de la placa Wi-Fi
systemctl restart network-online.target

