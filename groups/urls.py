import json
from typing import Literal
import aiohttp
import discord
from discord import app_commands


class Urls(app_commands.Group):
    def __init__(self, client:discord.Client, TINYAPITOKEN:str):
        super().__init__(name = 'urls', description='Commands for urls')
        self.client = client
        self.TINYAPITOKEN = TINYAPITOKEN
    

    @app_commands.command(name = 'create', description = 'Create a new URL')
    @app_commands.describe(alias="Alias to put you URL under")
    @app_commands.describe(domain = "Domain to use")
    @app_commands.describe(url="URL to shorten")
    async def create(self, interaction:discord.Interaction, alias:str, domain:Literal["tiny.one", "roft.lol", "tinyurl.com"], url:str):
        member = interaction.user
        data = {
            "url":url,
            "alias":alias,
            "domain":domain
        }
        embed = discord.Embed()
        embed.title = "Nao_Bot Url Agent"
        desc = ""
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://api.tinyurl.com/create?api_token={self.TINYAPITOKEN}", data=data) as response:
                res = await response.json()
                if len(res['errors']) != 0:
                    desc += res['errors'][0]
                else:
                    new_url = res['data']['tiny_url']
                    desc = f"""
Original URL length: {len(url)}
New URL length: {len(new_url)}
New URL: {new_url}
"""
                ...
        embed.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=self.client.user.avatar.url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/950171863789764668/951223109724307486/url_agent.jpg")
        embed.description = desc

        await interaction.response.send_message(embed=embed)
