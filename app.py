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

        # Verifica si hay un nuevo mensaje en el archivo de registro
        nuevo_mensaje = obtener_ultimo_mensaje(ruta_archivo_log)
        if nuevo_mensaje:
            await enviar_ultimo_mensaje(channel, nuevo_mensaje)

class ManejadorDeEventos(FileSystemEventHandler):
    async def on_modified(self, event):
        if event.src_path == ruta_archivo_log:
            # Verifica si hay un nuevo mensaje en el archivo de registro
            nuevo_mensaje = obtener_ultimo_mensaje(ruta_archivo_log)
            if nuevo_mensaje:
                channel_id = TU_ID_DE_CANAL  # Reemplaza con el ID del canal
                channel = bot.get_channel(channel_id)
                await enviar_ultimo_mensaje(channel, nuevo_mensaje)

def obtener_ultimo_mensaje(ruta):
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
        if lineas:
            return lineas[-1].strip()
        else:
            return None

async def enviar_ultimo_mensaje(channel, contenido):
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
