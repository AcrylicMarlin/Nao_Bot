from typing import Dict, Any
from pathlib import Path


from discord.ext import commands
import discord
import asyncpg
import aiohttp

from items import Nao_Credentials, CogLoadFailure


class NaoBot(commands.Bot):
    __intents:discord.Intents
    NAO_NATION:discord.Object
    __status:discord.Status
    __activity:discord.Activity
    __credentials:Nao_Credentials
    __pool:asyncpg.Pool
    __persistent_views:bool

    def __init__(self, *,
    intents:discord.Intents,
    status:discord.Status,
    activity:discord.Activity):
        self.__intents = intents
        self.__status = status
        self.__activity = activity
        self.__credentials = Nao_Credentials
        self.__persistent_views = False
        super().__init__('!', intents = self.__intents)
        
    


    async def on_ready(self):
        print('Nao_Bot is operational')
    
    async def setup_commands(self):
        for file in Path('cogs').glob('**/*.py'):
            *tree, _ = file.parts
            try:
                cog = f"{'.'.join(tree)}.{file.stem}"
                await self.load_extension(cog)
                print(f"{cog} loaded successfully!")

            except Exception as e:
                raise CogLoadFailure(file.stem, e)
        # await self.tree.sync(guild=self.__credentials.NAO_NATION.value)
        ...
    async def setup_hook(self):
        self.activity = self.__activity
        self.status = self.__status
        self.__pool = await asyncpg.create_pool(**self.__credentials.POSTGRES.value)
        await self.__pool.execute('CREATE TABLE IF NOT EXISTS setups (id TEXT PRIMARY KEY, persistent_message TEXT)')
        await self.setup_commands()
    

    async def run(self):

        try:
            await self.start(self.__credentials.DISCORD.value)
        except KeyboardInterrupt:
            await self.__pool.close()
            await self.close()