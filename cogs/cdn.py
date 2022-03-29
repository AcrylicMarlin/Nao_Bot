import json
import os

import aiohttp
import discord
from discord import Attachment, app_commands
from discord.ext import commands

from bot_class import NaoBot
from utils import Nao_Credentials
from utils.errors import NotDmChannel

def check_if_dm():
    def predicate(ctx:commands.Context):
        if ctx.guild is not None:
            raise NotDmChannel()
        else:
            return True
    return commands.check(predicate)

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

    @commands.group(name='cdn', invoke_without_command=True)
    @check_if_dm()
    async def cdn(self, ctx:commands.Context):
        embed = discord.Embed()
        embed.title = 'CDN'
        embed.description = 'This command requires authorization.\nPlease enter your password below.\nIf you do not have a password, you are not authorized XD.'
        await ctx.send(embed = embed)
        msg:discord.Message = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        async with aiohttp.ClientSession('https://cdn.naonation.com', timeout=aiohttp.ClientTimeout(total = 15)) as session:
            headers = {
                'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
                'upload_token': f'{Nao_Credentials.CDN.value}'
            }
            async with session.get('/authorize', headers = headers, data = {'password': f'{msg.content}'}) as response:
                resp = await response.read()
                resp = json.dumps(json.loads(resp), indent=4)
                embed.description = f'```{resp}```'
                await ctx.send(embed = embed)
        # async with aiohttp.ClientSession('https://cdn.naonation.com', timeout=aiohttp.ClientTimeout(total = 15)) as session:
        #     headers = {
        #         'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
        #         'upload_token': f'{Nao_Credentials.CDN.value}'
        #     }
        #     async with session.get('/status', headers = headers) as response:
        #         resp = await response.read()
        #         resp = json.dumps(json.loads(resp), indent=4)
        #         embed.description = f"""```{resp}```"""
        
        embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar.url}')
        embed.color = discord.Color.random()
        await ctx.send(embed=embed)

    @cdn.command(name='-upload')
    @commands.has_any_role()
    async def cdn_upload(self, ctx:commands.Context):
        
        file:Attachment = ctx.message.attachments[0]
        await file.save(f'{file.filename}')
        async with aiohttp.ClientSession('https://cdn.naonation.com', timeout=aiohttp.ClientTimeout(total = 15)) as session:
            headers = {
                'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
                'upload_token': f'{Nao_Credentials.CDN.value}'
            }
            async with session.post('/upload', headers = headers, data = {'file': open(f'{file.filename}', 'rb')}) as response:
                resp = await response.read()
                resp = json.dumps(json.loads(resp), indent=4)
                await ctx.send(f'```{resp}```')
        
        if os.path.exists(f'{file.filename}'):
            os.remove(f'{file.filename}')



async def setup(client:NaoBot):
    await client.add_cog(CDNCog(client), guild=Nao_Credentials.NAO_NATION.value)