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
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == "23:20":
            embed = discord.Embed(title="¡Qué pasa con las!", description="")
            file = discord.File('img/FMO2fvaXIAkfjPR.jpeg', filename='FMO2fvaXIAkfjPR.jpeg')
            embed.set_image(url="attachment://FMO2fvaXIAkfjPR.jpeg")

            await channel.send(embed=embed, file=file)

        await asyncio.sleep(60)

# Clase para manejar eventos de cambio en el archivo de registro
class ManejadorDeEventos(FileSystemEventHandler):
    async def on_modified(self, event):
        if event.src_path == ruta_archivo_log:
            nuevas_lineas = obtener_nuevas_lineas(ruta_archivo_log)
            for linea in nuevas_lineas:
                await enviar_mensaje(linea)

# Función para obtener las nuevas líneas agregadas al archivo de registro
def obtener_nuevas_lineas(ruta):
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
        return lineas

# Función para enviar mensajes al canal de Discord
async def enviar_mensaje(contenido):
    channel_id = TU_ID_DE_CANAL  # Reemplaza con el ID del canal
    channel = bot.get_channel(channel_id)
    await channel.send(contenido)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    
    # Inicializa el observador y lo asocia con la clase de manejo de eventos
    observador = Observer()
    observador.schedule(ManejadorDeEventos(), path=ruta_archivo_log)
    observador.start()

    # Inicia la tarea para enviar mensajes automáticos
    bot.loop.create_task(send_auto_message())

bot.run('')
