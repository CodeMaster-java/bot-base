import disnake
import os
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = disnake.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.voice_states = True
client = commands.InteractionBot(intents=intents)

# Load and add the cogs
initial_extensions = ['cogs.ping_cog', ]

for extension in initial_extensions:
    client.load_extension(extension)


num_extensions = len(client.extensions)


extension_names = list(client.extensions.keys())


print(f"Foram carregadas {num_extensions} extensões:")
for name in extension_names:
    print(name)

@client.event
async def on_ready():
    print("Bot está pronto!")
    print(f"Nome do Bot: {client.user.name}")
    print(f"ID do Bot: {client.user.id}")
    print("------")
    
    # Definir o status e a atividade do bot ao iniciar
    activity = disnake.Activity(
        type=disnake.ActivityType.watching,
        name="por interações!"
    )
    await client.change_presence(activity=activity)

client.run(TOKEN)