import asyncio
from email.mime import application
from http import client
import os

import discord
from discord import app_commands
from dotenv import load_dotenv
import  groups.basic as basic
load_dotenv()

TOKEN = os.environ.get('TOKEN')
NAO_NATION_ID = 695025143264706622

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents, application_id=928269449407102987)
tree = app_commands.CommandTree(client)
@client.event
async def on_ready():
    await client.wait_until_ready()
    await initialise(tree=tree, client=client, NAO_NATION_ID=NAO_NATION_ID)
    print('Nao_Bot is operational')




async def initialise(*, tree:app_commands.CommandTree, client:discord.Client, NAO_NATION_ID:int):
    """_summary_
    Initialises the bot
    Adds all of the groups to the client
    Syncs the commands to the server
    Later I will implement to choose between global or server side syncing
    Args:
        tree (app_commands.CommandTree): _description_
        client (discord.Client): _description_
        NAO_NATION_ID (int): _description_
    """
    tree.add_command(basic.Basic(client), guild=discord.Object(id=NAO_NATION_ID))
    await tree.sync(guild=discord.Object(id = NAO_NATION_ID))


if __name__ == '__main__':
    
    client.run(TOKEN)