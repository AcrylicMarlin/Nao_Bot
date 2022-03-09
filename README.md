## Current changes to Nao_Bot
### main.py
```py
# Builtins
import asyncio
import os 
# External
import discord
from discord import app_commands
from dotenv import load_dotenv
import  groups.basic as basic # Groups must be imported manually
load_dotenv()

TOKEN = os.environ.get('TOKEN') 
NAO_NATION_ID = 695025143264706622 

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents, application_id=928269449407102987) # New client
'''This is where the commands will go. without it, no slash'''
tree = app_commands.CommandTree(client) 

@client.event
async def on_ready():
    await client.wait_until_ready()
    await initialise(tree=tree, client=client, NAO_NATION_ID=NAO_NATION_ID) #function explained below
    print('Nao_Bot is operational')




async def initialise(*, tree:app_commands.CommandTree, client:discord.Client, NAO_NATION_ID:int):
    """_summary_
    Initialises the bot
    Adds all of the groups to the client
    Syncs the commands to the server
    Later I will implement to choose between global or server side syncing
    Args:
        tree (app_commands.CommandTree): _description_ The client command tree
        client (discord.Client): _description_ The client
        NAO_NATION_ID (int): _description_ NAO_NATION_ID constant
    """
    tree.add_command(basic.Basic(client), guild=discord.Object(id=NAO_NATION_ID)) # Groups are sent to the command tree here
    await tree.sync(guild=discord.Object(id = NAO_NATION_ID)) 
    '''All of the commands are synced to the guild for now.
    I will add a choice between global and guild syncing later.
    '''


if __name__ == '__main__':
    # run client
    client.run(TOKEN)
```


### basic.py
```py
import discord
from discord import app_commands

''' Groups subclass app_commands.Group, not commands.Cog
class Basic(app_commands.Group):
    def __init__(self, client):
        '''Group has it's own init, so must super it'''
        super().__init__(description='Basic Commands')
        self.client:discord.Client = client
    
    '''Basic latency command'''
    @app_commands.command(name='latency')
    async def ping(self, interaction:discord.Interaction):
        await interaction.response.send_message(content=f'`{round(self.client.latency * 1000)}ms`')
    
    '''Makes the bot say something'''
    @app_commands.command(name='say', description='Make me say something') # name and description of command
    @app_commands.describe(message='Message you want me to say') description of parameter
    async def say(self, interaction:discord.Interaction, message:str):
        await interaction.response.send_message(f'{message}') #sends just like a button interaction

```
