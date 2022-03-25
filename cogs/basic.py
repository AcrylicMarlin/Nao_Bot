import discord
from discord import app_commands
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, client):
        super().__init__(description='Basic Commands')
        self.client:discord.Client = client
    
    @app_commands.command(name='latency')
    async def ping(self, interaction:discord.Interaction):
        await interaction.response.send_message(content=f'`{round(self.client.latency * 1000)}ms`')

    @app_commands.command(name='say', description='Make me say something')
    @app_commands.describe(message='Message you want me to say')
    async def say(self, interaction:discord.Interaction, message:str):
        await interaction.response.send_message(f'{message}')

async def setup(client):
    await client.add_cog(Basic(client))