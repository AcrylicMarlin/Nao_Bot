import asyncio
import os
import json

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import groups.basic as basic
import groups.info as info
import groups.urls as urls

load_dotenv()

TOKEN = os.environ.get('TOKEN')
TINYAPITOKEN = os.environ.get('TINYAPITOKEN')
NAO_NATION_ID = 695025143264706622
NAO_NATION = discord.Object(id = NAO_NATION_ID)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents, application_id=928269449407102987)
tree = app_commands.CommandTree(client)
@client.event
async def on_ready():
    await client.wait_until_ready()
    await initialise(tree=tree, client=client, NAO_NATION=NAO_NATION, TINYAPITOKEN=TINYAPITOKEN)
    print('Nao_Bot is operational')


@tree.command(name = 'foo', description='Trial command [FOR DEVS ONLY]', guild=NAO_NATION)
async def foo(interaction:discord.Interaction):
    '''
        "body":{
        "url":interaction.guild.icon.url,
        "domain":"tiny.one",
        "alias":f"{interaction.guild.name}icon"
    '''
    if interaction.user.id == 846398473115795456 or interaction.user.id == 432613614168571904:
        data = {
            "url":"https://media.discordapp.net/attachments/908752890456322110/941409051126951946/IMG_7549.png?width=567&height=676",
            "domain":"tiny.one",
            "alias":"randommemefromserver"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://api.tinyurl.com/create?api_token={TINYAPITOKEN}", data=data) as response:

                item = await response.json()
                embed = discord.Embed()
                embed.title = 'Testing aiohttp Requests'
                embed.description = f"""
                ```
                {json.dumps(item, indent=4)}
                ```
                """
                await interaction.response.send_message(embed=embed)
                

    else:
        await interaction.response.send_message("This command is for devs only.")

async def initialise(*, tree:app_commands.CommandTree, client:discord.Client, NAO_NATION:discord.Object, TINYAPITOKEN:str):
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
    tree.add_command(basic.Basic(client), guild=NAO_NATION)
    tree.add_command(info.Info(client), guild=NAO_NATION)
    tree.add_command(urls.Urls(client, TINYAPITOKEN), guild=NAO_NATION)

    await tree.sync(guild=NAO_NATION)


if __name__ == '__main__':
    
    client.run(TOKEN)