# machineinfo
Questo script Python raccoglie informazioni sulla macchina in uso e le invia a un webhook.

## Dipendenze
- requests
- psutil

## Utilizzo
1. Clona il repository.
2. Installa le dipendenze con `pip install -r requirements.txt`.
3. Modifica il file `config.py` con l'URL del tuo webhook.
4. Esegui lo script con `python machineinfo.py`.

## Informazioni sulla macchina
Lo script raccoglie le seguenti informazioni sulla macchina:
- Utilizzo della memoria
- ID della macchina corrente
- Informazioni sul sistema operativo
- Informazioni sulla CPU
- Indirizzo MAC dell'interfaccia di rete

## Webhook
Lo script invia le informazioni sulla macchina al webhook specificato nel file `config.py`.
