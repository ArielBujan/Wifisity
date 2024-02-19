def capture_wifi_info(interface, duration):
    command = ["airodump-ng", interface, "--output-format", "csv", "--write", "output"]
    process = subprocess.Popen(command)
    time.sleep(duration)
    process.terminate()

def parse_output_file(output_file):
    networks = {}
    with open(output_file + "-01.csv", "r") as file:
        lines = file.readlines()
        for line in lines[2:]:  # Skip the header rows
            parts = line.strip().split(",")
            if len(parts) >= 14:  # Verifica si hay suficientes campos
                bssid = parts[0].strip()
                ssid = parts[13].strip()
                if ssid != "SSID" and ssid != "":
                    networks[bssid] = ssid
    return networks

def save_to_file(networks, output_file):
    with open(output_file, "w") as file:
        for bssid, ssid in networks.items():
            file.write(f"{bssid}: {ssid}\n")

if __name__ == "__main__":
    interface = "wlan0"
    duration = 5  # seconds
    output_file = "SSID.txt"

    capture_wifi_info(interface, duration)
    networks = parse_output_file("output")
    save_to_file(networks, output_file)
