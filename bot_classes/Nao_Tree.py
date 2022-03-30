import logging
import traceback
import sys

import discord
from discord import app_commands
from discord.ext import commands

class NaoTree(app_commands.CommandTree):
    def __init__(self, client):
        super().__init__(client=client)
    
    async def on_error(self, interaction: discord.Interaction, command: app_commands.AppCommand, error: app_commands.AppCommandError) -> None:
        embed = discord.Embed()
        embed.title = 'Error'
        embed.color = discord.Color.red()
        embed.set_footer(text='Nao Nation', icon_url=self.client.user.avatar.url)
        embed.description = f'An error has occured while executing the command\nError:```{error}```'
        await interaction.channel.send(embed = embed)
        
        print('Ignoring {} in command {}:'.format(type(error), command.name), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        logging.error(f'Ignoring {type(error)} in command {command.name}: {error}')
    ...