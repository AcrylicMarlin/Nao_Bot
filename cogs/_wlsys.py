import discord
from discord import app_commands
from discord.ext import commands

from utils import check_if_dm, Nao_Credentials
from bot_classes import NaoBot
class WLSYS(commands.Cog):
    def __init__(self, client):
        self.client:NaoBot = client








    async def setup(client:NaoBot):
        await client.add_cog(WLSYS(client), guild=Nao_Credentials.NAO_NATION.value)
