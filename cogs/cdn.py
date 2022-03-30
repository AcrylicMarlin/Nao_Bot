from code import interact
import json
from json import JSONDecodeError
import os
import sys
import traceback

import aiohttp
import discord
from discord import Attachment, app_commands
from discord.ext import commands

from bot_class import NaoBot
from utils import Nao_Credentials
from utils import check_if_not_dm






class CDNCog(commands.Cog):
    def __init__(self, client):
        self.client:NaoBot = client
    
    async def cog_load(self) -> None:
        async with aiohttp.ClientSession('https://cdn.naonation.com', timeout=aiohttp.ClientTimeout(total = 15)) as session:
            headers = {
                'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
                'upload_token': f'{Nao_Credentials.CDN.value}'
            }
            async with session.get('/status', headers = headers) as response:
                resp = await response.read()
                resp = json.dumps(json.loads(resp), indent=4)
                print(resp)

    @app_commands.command(name='cdn-status')
    @check_if_not_dm()
    async def cdn(self, interaction:discord.Interaction):
        if interaction.user.id not in Nao_Credentials.OWNERS.value:
            return await interaction.channel.send('You do not have permission to use this command')


        embed = discord.Embed()
        embed.title = 'CDN'
        embed.set_footer(text=f'{interaction.user.display_name}', icon_url=f'{interaction.user.avatar.url}')
        embed.color = discord.Color.random()
        
        async with aiohttp.ClientSession('https://cdn.naonation.com', timeout=aiohttp.ClientTimeout(total = 15)) as session:
            headers = {
                'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
                'upload_token': f'{Nao_Credentials.CDN.value}'
            }
            async with session.get('/status', headers = headers) as response:
                resp = await response.read()
                resp = json.dumps(json.loads(resp), indent=4)
                embed.description = f'```{resp}```'
                await interaction.channel.send(embed = embed)




    @app_commands.command(name='-upload')
    @check_if_not_dm()
    async def cdn_upload(self, interaction:discord.Interaction, *, file:discord.Attachment):
        if interaction.user.id not in Nao_Credentials.OWNERS.value:
            return await interaction.channel.send('You do not have permission to use this command')

        
        await file.save(f'{file.filename}')
        async with aiohttp.ClientSession('https://cdn.naonation.com', timeout=aiohttp.ClientTimeout(total = 15)) as session:
            headers = {
                'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
                'upload_token': f'{Nao_Credentials.CDN.value}'
            }
            async with session.post('/upload', headers = headers, data = {'file': open(f'{file.filename}', 'rb')}) as response:
                resp = await response.read()
                resp = json.dumps(json.loads(resp), indent=4)
                await interaction.response.send_message(f'```{resp}```')
        
        if os.path.exists(f'{file.filename}'):
            os.remove(f'{file.filename}')



async def setup(client:NaoBot):
    await client.add_cog(CDNCog(client))