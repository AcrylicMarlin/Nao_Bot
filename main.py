# Builtins
import asyncio
import sys
import traceback

# External Libraries
import discord
from discord import app_commands
from discord.ext import commands


# Internal Functionality
from bot_class import NaoBot
from utils import NotDmChannel, CogLoadFailure
from utils.errors import IsDmChannel




# Creating discord functionality
intents = discord.Intents.all()
status = discord.Status.dnd
activity = discord.Activity(name = 'for your commands', type = discord.ActivityType.watching, url = 'https://www.youtube.com/watch?v=o-YBDTqX_ZU')

client = NaoBot(intents = intents, status=status, activity=activity)

@client.tree.error
async def on_error(interaction: discord.Interaction, command:app_commands.AppCommand, error: app_commands.AppCommandError):
    embed = discord.Embed()
    embed.title = 'Error'
    embed.color = discord.Color.red()
    embed.set_footer(text='Nao Nation', icon_url=client.user.avatar.url)
    embed.description = f'An error has occured while executing the command\nError:```{error}```'
    await interaction.channel.send(embed = embed)
    
    print('Ignoring {} in command {}:'.format(type(error), command.name), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    ...
if __name__ == '__main__':
    asyncio.run(client.run())

