import discord
import asyncio
from discord.ext import commands
import os
import re
from dotenv import load_dotenv
from pylatex import Document, NoEscape, Command
import matplotlib.pyplot as plt
import tempfile
import requests
import os
from pdf2image import convert_from_path
from PIL import Image

from pylatex import Document, Section, Subsection, Math
from pylatex.utils import italic


# Carga las variables de entorno desde el archivo .env
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Función para generar una imagen LaTeX con la expresión y su resultado
def generar_imagen_latex(expresion, resultado):
    latex_expression = f"\\text{{Expresión: }} {expresion} \\quad \\text{{Resultado: }} {resultado}"
    url = f"https://latex2image.joeraut.com/api/latex?text={latex_expression}&format=png"
    response = requests.get(url)
    if response.status_code == 200:
        with open("latex_image.png", "wb") as f:
            f.write(response.content)
        return "latex_image.png"
    else:
        return None

# Comando para calcular expresiones matemáticas
@bot.command()
async def calcular(ctx, *, expresion):
    resultado = evaluar_expresion_matematica(expresion)
    if resultado is not None:
        # Generar imagen LaTeX
        latex_image_path = generar_imagen_latex(expresion, resultado)
        if latex_image_path:
            # Enviar la imagen generada a Discord
            with open(latex_image_path, 'rb') as f:
                await ctx.send(file=discord.File(f))
            # Eliminar la imagen temporal
            os.remove(latex_image_path)
        else:
            await ctx.send("Error al generar la imagen LaTeX.")
    else:
        await ctx.send("La expresión no es válida.")
# Función para evaluar expresiones matemáticas
def evaluar_expresion_matematica(expresion):
    if re.match(r"^\d+(\.\d+)?([+\-*/]\d+(\.\d+)?)*$", expresion):
        try:
            resultado = eval(expresion)
            return str(resultado)
        except Exception as e:
            return f"Error al evaluar la expresión: {e}"
    else:
        return None

# Función para obtener respuesta
def obtener_respuesta(mensaje):
    resultado_matematico = evaluar_expresion_matematica(mensaje)
    if resultado_matematico is not None:
        return resultado_matematico
    else:
        respuesta = chatbot.respond(mensaje)
        if respuesta is None:
            respuesta = "Lo siento, no entiendo tu pregunta."
        return respuesta

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    bot.loop.create_task(send_auto_message())

# Comando para saludar
@bot.command()
async def saludo(ctx):
    if ctx.author.id == 380118893181534219:  
        await ctx.send(f'Señor')
    else:
        await ctx.send(f'Hola {ctx.author.mention} ¿cómo estás?')



# Función para enviar un mensaje automático
async def send_auto_message():
    channel_id = 1103919972771708949
    channel = bot.get_channel(channel_id)

    while True:
        await asyncio.sleep(600)  
        await channel.send("Este es un mensaje automático.")

bot.run(DISCORD_TOKEN)