import discord
import asyncio
import os
import re
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from fractions import Fraction

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def evaluar_expresion_matematica(expresion):
    # Reemplazamos fracciones de la forma 'a/b' por 'Fraction(a, b)'
    expresion = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expresion)
    print("Expresión evaluada:", expresion)
    
    # Verificamos explícitamente la división por cero
    if re.search(r'Fraction\(\d+, 0\)', expresion) or re.search(r'/\s*0', expresion):
        return "División por cero, en este universo, No Existe.", None
 
    if re.match(r"^[\d()+\-*/\sFraction,]+$", expresion):  
        try:
            inicio = datetime.now()
            # Evaluamos la expresión en un entorno seguro
            resultado = eval(expresion, {"Fraction": Fraction})
            fin = datetime.now()
            tiempo_ejecucion = (fin - inicio).total_seconds()
            return str(resultado), tiempo_ejecucion
        except Exception as e:
            return f"Error al evaluar la expresión: {e}", None
    else:
        return "La expresión no es válida.", None

@bot.command()
async def calcular(ctx, *, expresion):
    resultado, tiempo_ejecucion = evaluar_expresion_matematica(expresion)
    if resultado:
        embed = discord.Embed(title="Calculadora",
                              description=f"```md\n# Operación\n{expresion}\n\n# Resultado\n{resultado}\n```",
                              colour=0x00b0f4,
                              timestamp=datetime.now())
        #embed.set_author(name="Math Bot")
        embed.set_footer(text=f"Tiempo de ejecución: {tiempo_ejecucion} segundos",
                         icon_url="https://slate.dan.onl/slate.png")
        await ctx.send(embed=embed)
    else:
        await ctx.send("La expresión no es válida.")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    bot.loop.create_task(send_auto_message())

@bot.command()
async def saludo(ctx):
    if ctx.author.id == 380118893181534219:  
        await ctx.send(f'Señor')
    else:
        await ctx.send(f'Hola {ctx.author.mention} ¿cómo estás?')

async def send_auto_message():
    channel_id = 1103919972771708949
    channel = bot.get_channel(channel_id)

    while True:
        await asyncio.sleep(600)  
        await channel.send("Este es un mensaje automático.")

bot.run(DISCORD_TOKEN)
