import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents, command_prefix='$')

@client.command
async def on_message(message):
    await message.channel.send('Hello!')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('Nzg3ODgyNjkxODM1MzMwNjQx.Gwv-uk.0mOpM4iYoo4Qw-17jXNWm3XYB4UevsMyCce6G0')