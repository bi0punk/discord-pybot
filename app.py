
import discord
import asyncio
from discord.ext import commands
from datetime import datetime
import schedule
# Configura las intenciones requeridas
intents = discord.Intents.default()
intents.message_content = True

# Configura el bot con las intenciones
bot = commands.Bot(command_prefix='!', intents=intents)


async def send_auto_message():
    channel = bot.get_channel()  

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time)
        if current_time == "21:20":
            print(current_time)
            # Crea un mensaje "embed" con una imagen
            embed = discord.Embed(title="Que pasa con las", description="")
            file = discord.File('img/FMO2fvaXIAkfjPR.jpeg', filename='FMO2fvaXIAkfjPR.jpeg')
            embed.set_image(url="attachment://FMO2fvaXIAkfjPR.jpeg")

            # Envía el "embed" al canal
            await channel.send(embed=embed, file=file)

        await asyncio.sleep(60)  



# Evento de inicio del bot
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    # Inicia la función de enviar mensajes automáticos
    bot.loop.create_task(send_auto_message())

# Inicia el bot con el token
bot.run('token')
