import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ruta_archivo_log = '/root/server/logs/latest.log'  # Reemplaza con la ruta correcta
last_sent_message = None

async def send_auto_message():
    global last_sent_message  # Asegura que estás utilizando la variable global
    
    channel_id = 1103919972771708949  # Reemplaza con el ID del canal
    channel = bot.get_channel(channel_id)

    while True:
        await asyncio.sleep(30)  # Espera 60 segundos antes de verificar el archivo

        # Verifica si hay nuevos mensajes en el archivo de registro relacionados con jugadores
        nuevos_mensajes = obtener_nuevos_mensajes(ruta_archivo_log)
        for mensaje in nuevos_mensajes:
            # Verifica si el mensaje es igual al último mensaje enviado
            if mensaje != last_sent_message:
                await enviar_mensaje(channel, mensaje)
                last_sent_message = mensaje

class ManejadorDeEventos(FileSystemEventHandler):
    async def on_modified(self, event):
        global last_sent_message  # Asegura que estás utilizando la variable global
        
        if event.src_path == ruta_archivo_log:
            nuevos_mensajes = obtener_nuevos_mensajes(ruta_archivo_log)
            for mensaje in nuevos_mensajes:
                channel_id = TU_ID_DE_CANAL  # Reemplaza con el ID del canal
                channel = bot.get_channel(channel_id)
            
                if mensaje != last_sent_message:
                    await enviar_mensaje(channel, mensaje)
                    last_sent_message = mensaje

def obtener_nuevos_mensajes(ruta):
    palabras_clave = ["joined the game", 
                    "was slain by", 
                    "lost connection", 
                    "left the game", 
                    "has made the advancement", 
                    "fell from a high place", 
                    "drowned"]

    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()

    mensajes_filtrados = []

    for linea in lineas:
        for palabra_clave in palabras_clave:
            if palabra_clave in linea:
                mensajes_filtrados.append(linea.strip())
                break  # Termina el bucle interno si se encuentra una palabra clave

    return mensajes_filtrados

async def enviar_mensaje(channel, contenido):
    embed = discord.Embed(
        title="Nuevo mensaje del servidor de Minecraft",
        description=f"```\n{contenido}\n```",
        color=0x00b0f4,
        timestamp=datetime.now()
    )
    embed.set_author(name="Info Minecraft World")
    embed.set_footer(icon_url="https://slate.dan.onl/slate.png")

    await channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    
    observador = Observer()
    observador.schedule(ManejadorDeEventos(), path=ruta_archivo_log)
    observador.start()

    bot.loop.create_task(send_auto_message())

bot.run('')  # Coloca tu token aquí
