import json
import os

import aiohttp
import discord
from discord import Attachment, app_commands
from discord.ext import commands

from bot_classes import NaoBot
from utils import Nao_Credentials, check_if_not_dm
from views import FilesPageinator






class CDNCog(commands.Cog):
    def __init__(self, client):
        self.client:NaoBot = client
    
    async def cog_load(self) -> None:
        # async with aiohttp.ClientSession('https://cdn.nao.gg', timeout=aiohttp.ClientTimeout(total = 15)) as session:
        headers = {
            'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
            'upload_token': f'{Nao_Credentials.CDN.value}'
        }
        # Passing around the connection works!
        async with self.client.session.get('/status', headers = headers) as response:
            resp = await response.read()
            resp = json.dumps(json.loads(resp), indent=4)
            print(resp)

    @commands.group(name='cdn', invoke_without_command=True)
    @check_if_not_dm()
    async def cdn(self, ctx:commands.Context):
        if ctx.author.id not in Nao_Credentials.OWNERS.value:
            return await ctx.send('You do not have permission to use this command')

        embed = discord.Embed()
        embed.title = 'CDN'
        embed.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
        embed.color = discord.Color.random()
        
        
        headers = {
            'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
            'upload_token': f'{Nao_Credentials.CDN.value}'
        }
        async with self.client.session.get('/status', headers = headers) as response:
            resp = await response.read()
            resp = json.dumps(json.loads(resp), indent=4)
            embed.description = f'```{resp}```'
            await ctx.send(embed = embed)




    @cdn.command(name='-upload')
    @check_if_not_dm()
    async def cdn_upload(self, ctx:commands.Context):
        if ctx.author.id not in Nao_Credentials.OWNERS.value:
            return await ctx.send('You do not have permission to use this command')

        
        embed = discord.Embed()
        embed.title = 'CDN'
        embed.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
        embed.color = discord.Color.random()

        file:Attachment = ctx.message.attachments[0]
        await file.save(f'{file.filename}')

        headers = {
            'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
            'upload_token': f'{Nao_Credentials.CDN.value}'
        }
        async with self.client.session.post('/upload-file', headers = headers, data = {'file': open(f'{file.filename}', 'rb')}) as response:
            resp = await response.read()
            resp = json.dumps(json.loads(resp), indent=4)
            embed.description = f'```{resp}```'
            await ctx.send(embed = embed)
        
        if os.path.exists(f'{file.filename}'):
            os.remove(f'{file.filename}')


    @cdn.command(name = '-file-list')
    @check_if_not_dm()
    async def cdn_file_list(self, ctx:commands.Context):
        if ctx.author.id not in Nao_Credentials.OWNERS.value:
            return await ctx.send('You do not have permission to use this command')
        
        embed = discord.Embed()
        embed.title = 'CDN'
        embed.set_footer(text=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar.url}')
        embed.color = discord.Color.random()


        headers = {
            'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
            'upload_token': f'{Nao_Credentials.CDN.value}'
        }
        async with self.client.session.get('/file-list', headers = headers) as response:
            resp = await response.read()
            resp = json.dumps(json.loads(resp), indent=4)
            embed.description = f'```{resp}```'
            await ctx.send(embed = embed)
    
    @cdn.command(name = '-files')
    @check_if_not_dm()
    async def cdn_files(self, ctx:commands.Context):
        if ctx.author.id not in Nao_Credentials.OWNERS.value:
            return await ctx.send('You do not have permission to use this command')
        

        headers = {
            'User-Agent': f'{self.client.user.name}_{self.client.user.id}',
            'upload_token': f'{Nao_Credentials.CDN.value}'
        }
        async with self.client.session.get('/file-list', headers = headers) as response:
            resp = await response.read()
            resp = json.loads(resp)
        view = FilesPageinator(resp['file_list'])
        view.message = await ctx.send(view = view)
            
        
        

        ...


async def setup(client:NaoBot):
    await client.add_cog(CDNCog(client))