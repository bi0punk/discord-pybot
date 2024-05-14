import discord
import asyncio
import os
import re
import nltk
from nltk.chat.util import Chat, reflections
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from fractions import Fraction

# Descargamos los datos necesarios de NLTK
nltk.download('punkt')
nltk.download('wordnet')

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Definimos pares de patrones y respuestas para el chatbot
pairs = [
    (r'Hola|hola|Hi|hi|Hey|hey', ['Hola, ¿cómo estás?', '¡Hola! ¿Cómo te puedo ayudar?']),
    (r'¿Cuál es tu nombre\??', ['Soy un bot de Discord. ¿Cuál es tu nombre?']),
    (r'¿Cómo estás\??', ['Estoy bien, gracias por preguntar.', '¡Estoy genial!']),
    (r'¿Qué puedes hacer\??', ['Puedo ayudarte con cálculos matemáticos y responder preguntas básicas.']),
    (r'Adiós|adiós|adios|Bye|bye', ['Adiós, ¡que tengas un buen día!', '¡Hasta luego!'])
]

chatbot = Chat(pairs, reflections)

def evaluar_expresion_matematica(expresion):
    expresion = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expresion)
    print("Expresión evaluada:", expresion)
    
    if re.search(r'Fraction\(\d+, 0\)', expresion) or re.search(r'/\s*0', expresion):
        return "Error: División por cero.", None
    
    if re.match(r"^[\d()+\-*/\sFraction,]+$", expresion):  
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
        embed.set_author(name="Math Bot")
        embed.set_footer(text=f"Tiempo de ejecución: {tiempo_ejecucion} segundos",
                         icon_url="https://slate.dan.onl/slate.png")
        await ctx.send(embed=embed)
    else:
        await ctx.send("La expresión no es válida.")

@bot.command()
async def responder(ctx, *, pregunta):
    respuesta = chatbot.respond(pregunta)
    if respuesta:
        await ctx.send(respuesta)
    else:
        await ctx.send("No tengo una respuesta para eso.")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    bot.loop.create_task(send_auto_message())

@bot.command()
async def saludo(ctx):
    if ctx.author.id == OWNER_ID:
        await ctx.send(f'Señor')
    else:
        await ctx.send(f'Hola {ctx.author.mention} ¿cómo estás?')

async def send_auto_message():
    channel = bot.get_channel(CHANNEL_ID)

    while True:
        await asyncio.sleep(600)  
        await channel.send("Este es un mensaje automático.")

bot.run(DISCORD_TOKEN)
