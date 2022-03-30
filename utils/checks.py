from discord import app_commands
from discord.ext import commands
import discord
from utils import IsDmChannel, NotDmChannel



def check_if_dm():
    def check(interaction:discord.Interaction):
        if interaction.guild is None:
            raise IsDmChannel()
        return True
    return app_commands.check(check)

def check_if_not_dm():
    def check(ctx:commands.Context):
        if ctx.guild is not None:
            raise NotDmChannel()
        return True
    return commands.check(check)
