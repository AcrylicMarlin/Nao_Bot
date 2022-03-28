import discord
from discord import app_commands
from discord.ext import commands
import asqlite

from utils import Nao_Credentials
from views import Warns_Pageinator
from bot_class import NaoBot

class Trials(commands.Bot):
    def __init__(self, client):
        self.client = client

    
    @app_commands.command(name = 'pages')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    async def pages(self, interaction:discord.Interaction):
        await interaction.response.send_message('Gathering warns...', ephemeral=True)
        view = Warns_Pageinator(1)
        view.message = await interaction.channel.send("Users Warns", view=view)
        ...


async def setup(client):
    assert isinstance(client, NaoBot)
    await client.add_cog(Trials, guild=Nao_Credentials.NAO_NATION.value)