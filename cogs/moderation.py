import discord
from discord.ext import commands
from discord import app_commands

from utils import Nao_Credentials

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kick')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to kick', reason='Reason for kicking')
    async def kick(self, interaction:discord.Interaction, member: discord.Member, *, reason: str = None):
        await interaction.guild.kick(member, reason=reason)
        await interaction.response.send_message('Kicked {} for {}'.format(member.mention, reason))
        try:
            await member.send('You have been kicked from {} for {}'.format(interaction.guild.name, reason))
        except Exception:
            pass
    