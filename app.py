import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ruta_archivo_log = 'RUTA_AL_ARCHIVO_DE_LOG_DEL_SERVIDOR'  # Reemplaza con la ruta correcta

async def send_auto_message():
    channel_id = TU_ID_DE_CANAL  # Reemplaza con el ID del canal
    channel = bot.get_channel(channel_id)

    while True:
        await asyncio.sleep(60)  # Espera 60 segundos antes de verificar el archivo

        # Verifica si hay nuevos mensajes en el archivo de registro relacionados con jugadores
        nuevos_mensajes = obtener_nuevos_mensajes(ruta_archivo_log)
        for mensaje in nuevos_mensajes:
            await enviar_mensaje(channel, mensaje)

class ManejadorDeEventos(FileSystemEventHandler):
    async def on_modified(self, event):
        if event.src_path == ruta_archivo_log:
            # Verifica si hay nuevos mensajes en el archivo de registro relacionados con jugadores
            nuevos_mensajes = obtener_nuevos_mensajes(ruta_archivo_log)
            for mensaje in nuevos_mensajes:
                channel_id = TU_ID_DE_CANAL  # Reemplaza con el ID del canal
                channel = bot.get_channel(channel_id)
                await enviar_mensaje(channel, mensaje)

def obtener_nuevos_mensajes(ruta):
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
        
        # Filtra las líneas que contienen información sobre la entrada, derrota, pérdida de conexión o salida de jugadores
        mensajes_filtrados = [linea.strip() for linea in lineas if "joined the game" in linea or "was slain by" in linea or "lost connection" in linea or "left the game" in linea]

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
    
    # Inicializa el observador y lo asocia con la clase de manejo de eventos
    observador = Observer()
    observador.schedule(ManejadorDeEventos(), path=ruta_archivo_log)
    observador.start()

    # Inicia la tarea para enviar mensajes automáticos
    bot.loop.create_task(send_auto_message())

bot.run('')  # Coloca tu token aquí
