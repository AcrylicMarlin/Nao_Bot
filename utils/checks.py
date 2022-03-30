from discord import app_commands
import discord
from utils import IsDmChannel, NotDmChannel



def check_if_dm():
    def check(interaction:discord.Interaction):
        if interaction.guild is None:
            raise IsDmChannel()
        return True
    return app_commands.check(check)

def check_if_not_dm():
    def check(interaction:discord.Interaction):
        if interaction.guild is not None:
            raise NotDmChannel()
        return True
    return app_commands.check(check)