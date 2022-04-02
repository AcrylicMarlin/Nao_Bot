# Builtins
import asyncio

# External Libraries
import discord


# Internal Functionality
from bot_classes import NaoBot, NaoTree




# Creating discord functionality
intents = discord.Intents.all()
status = discord.Status.dnd
activity = discord.Activity(name = 'for your commands', type = discord.ActivityType.watching, url = 'https://www.youtube.com/watch?v=o-YBDTqX_ZU')

client = NaoBot(intents = intents, status=status, activity=activity, tree_cls=NaoTree)


if __name__ == '__main__':
    asyncio.run(client.run())

