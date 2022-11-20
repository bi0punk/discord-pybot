import asyncpg
from discord import channel
from discord.ext import tasks, commands
import discord
import datetime, random
import asyncio

vbot = commands.Bot(command_prefix='*', description="Datos vrios Chile informaciones", intents=discord.Intents.all())

@vbot.event #creacion de eventos
async def on_ready():
    print('. . . O N  L I N E . . . ')
    await mensaje_automatico()



@vbot.command()
async def mmm(contexto):
    embed=discord.Embed(title="Sismos", description="muestra sismos", color=0xda0000)
    embed.set_thumbnail(url="https://n9.cl/yqsvw")
    embed.fields
    embed.set_footer(text="aca")
    await contexto.send(embed)


async def mensaje_automatico():
    while(True):
        ahora  = datetime.datetime.now()
        print(ahora)
        """ despues  = ahora+datetime.timedelta(days=1) """
        despues = ahora.replace(hour=00,minute=35)
        tiempo_espera = (despues-ahora).total_seconds()
        await asyncio.sleep(tiempo_espera)
        """ print(ahora)
        print(despues) """
        print(tiempo_espera)
        channel = vbot.get_channel(835940738201288727)
        await channel.send("JP hacela corta")
        return mensaje_automatico()


vbot.run('Nzg3ODgyNjkxODM1MzMwNjQx.Gwv-uk.0mOpM4iYoo4Qw-17jXNWm3XYB4UevsMyCce6G0')

