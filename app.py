import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ruta_archivo_log = '/root/server/logs/latest.log'  
historial_mensajes_archivo = 'historial_mensajes.txt'  
historial_mensajes = set()
try:
    with open(historial_mensajes_archivo, 'r') as archivo:
        historial_mensajes = set(archivo.read().splitlines())
except FileNotFoundError:
    pass

async def send_auto_message():
    channel_id =   
    channel = bot.get_channel(channel_id)

    while True:
        await asyncio.sleep(60)  

        nuevos_mensajes = obtener_nuevos_mensajes(ruta_archivo_log)
        for mensaje in nuevos_mensajes:
            if mensaje not in historial_mensajes:
                await enviar_mensaje(channel, mensaje)
                historial_mensajes.add(mensaje)
                with open(historial_mensajes_archivo, 'a') as archivo:
                    archivo.write(mensaje + '\n')

class ManejadorDeEventos(FileSystemEventHandler):
    async def on_modified(self, event):
        nuevos_mensajes = obtener_nuevos_mensajes(ruta_archivo_log)
        for mensaje in nuevos_mensajes:
            channel_id = TU_ID_DE_CANAL  
            channel = bot.get_channel(channel_id)
            if mensaje not in historial_mensajes:
                await enviar_mensaje(channel, mensaje)
                historial_mensajes.add(mensaje)
                with open(historial_mensajes_archivo, 'a') as archivo:
                    archivo.write(mensaje + '\n')

def obtener_nuevos_mensajes(ruta):
    palabras_clave = ["joined the game", 
                    "was slain by", 
                    "lost connection", 
                    "left the game", 
                    "has made the advancement", 
                    "fell from a high place", 
                    "drowned",
                    "tried to swim in lava"
                    ]

    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()

    mensajes_filtrados = []

    for linea in lineas:
        for palabra_clave in palabras_clave:
            if palabra_clave in linea:
                mensajes_filtrados.append(linea.strip())
                break  
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
