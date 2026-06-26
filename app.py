import discord
import asyncio
import os
import ast
import operator
import nltk
from nltk.chat.util import Chat, reflections
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

def asegurar_datos_nltk() -> None:
    """Descarga los datos necesarios de NLTK si no están presentes."""
    for pkg in ['punkt', 'wordnet']:
        try:
            nltk.data.find(f'tokenizers/{pkg}')
        except LookupError:
            nltk.download(pkg)

asegurar_datos_nltk()

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN no está definido en el archivo .env")
try:
    OWNER_ID = int(os.getenv('OWNER_ID'))
    CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
except (TypeError, ValueError):
    raise ValueError("OWNER_ID y CHANNEL_ID deben ser números enteros válidos en el archivo .env")

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

def evaluar_expresion_matematica(expresion: str) -> tuple:
    """Evalúa una expresión matemática de forma segura usando AST."""
    try:
        inicio = datetime.now()
        expresion_safe = expresion.replace("×", "*").replace("÷", "/")
        tree = ast.parse(expresion_safe, mode='eval')
        resultado = safe_eval_ast(tree.body)
        fin = datetime.now()
        tiempo_ejecucion = (fin - inicio).total_seconds()
        return str(resultado), tiempo_ejecucion
    except ZeroDivisionError:
        return "Error: División por cero.", None
    except Exception as e:
        return f"Error al evaluar la expresión: {e}", None

def safe_eval_ast(node: ast.AST) -> float:
    """Evalúa un nodo AST de forma segura con operaciones permitidas."""
    allowed_ops = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos,
    }
    if isinstance(node, ast.Expression):
        return safe_eval_ast(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Tipo no soportado")
    if isinstance(node, ast.BinOp):
        op_func = allowed_ops.get(type(node.op))
        if not op_func:
            raise ValueError("Operación no soportada")
        return op_func(safe_eval_ast(node.left), safe_eval_ast(node.right))
    if isinstance(node, ast.UnaryOp):
        op_func = allowed_ops.get(type(node.op))
        if not op_func:
            raise ValueError("Operación no soportada")
        return op_func(safe_eval_ast(node.operand))
    raise ValueError("Expresión no válida")

@bot.command()
async def calcular(ctx: commands.Context, *, expresion: str) -> None:
    """Evalúa una expresión matemática y muestra el resultado."""
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
async def responder(ctx: commands.Context, *, pregunta: str) -> None:
    """Responde preguntas usando el chatbot NLTK."""
    respuesta = chatbot.respond(pregunta)
    if respuesta:
        await ctx.send(respuesta)
    else:
        await ctx.send("No tengo una respuesta para eso.")

@bot.event
async def on_ready() -> None:
    """Evento ejecutado cuando el bot se conecta correctamente."""
    print(f'Bot conectado como {bot.user.name}')
    bot.loop.create_task(send_auto_message())

@bot.command()
async def saludo(ctx: commands.Context) -> None:
    """Saluda al usuario, con tratamiento especial para el dueño."""
    if ctx.author.id == OWNER_ID:
        await ctx.send(f'Señor')
    else:
        await ctx.send(f'Hola {ctx.author.mention} ¿cómo estás?')

async def send_auto_message() -> None:
    """Envía un mensaje automático cada 60 segundos al canal configurado."""
    channel = bot.get_channel(CHANNEL_ID)

    while True:
        await asyncio.sleep(60)  
        await channel.send("/play https://www.youtube.com/watch?v=vT0oJWPbIZs&ab_channel=Ozuna")

bot.run(DISCORD_TOKEN)