# Builtins
import asyncio

# External Libraries
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Internal Functionality
from bot_class import NaoBot




# Creating discord functionality
intents = discord.Intents.default()
intents.message_content = True
status = discord.Status.dnd
activity = discord.Activity(name = 'for your commands', type = discord.ActivityType.watching, url = 'https://www.youtube.com/watch?v=o-YBDTqX_ZU')

client = NaoBot(intents = intents, status=status, activity=activity)

if __name__ == '__main__':
    asyncio.run(client.run())

