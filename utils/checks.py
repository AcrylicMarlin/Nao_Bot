from discord import app_commands
from discord.ext import commands
import discord
from utils import (
    IsDmChannel,
    NotDmChannel,
    NotAuthorized,
    Nao_Credentials
)




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

def check_for_owners():
    def check(ctx:commands.Context):
        if ctx.author.id not in Nao_Credentials.OWNERS.value:
            raise NotAuthorized("You do not have permission to use this command.")
        return True
    return commands.check(check)
