import logging
import traceback
import sys
import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from .Nao_Embeds import ErrorEmbed
class NaoTree(app_commands.CommandTree):
    def __init__(self, client):
        super().__init__(client=client)
    
    async def on_error(self, interaction: discord.Interaction, command: app_commands.AppCommand, error: app_commands.AppCommandError) -> None:
        embed = ErrorEmbed(error)
        if isinstance(error, asyncio.exceptions.TimeoutError):
            embed.description = '```The CDN failed to respond in time.\nPlease try again later.```'
            await interaction.channel.send(embed=embed)
            return
        await interaction.channel.send(embed = embed)
        
        print('Ignoring {} in command {}:'.format(type(error), command.name), file=sys.stderr)
        # traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        logging.error(f'Ignoring {type(error)} in command {command.name}: {error}')
        ...
    ...