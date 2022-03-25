from typing import Dict, Any


from discord.ext import commands
import discord
import asyncpg
import aiohttp

from items import Nao_Credentials


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
    

    async def setup_hook(self):
        self.activity = self.__activity
        self.status = self.__status
        self.__pool = await asyncpg.create_pool(**self.__credentials.POSTGRES.value)
        await self.__pool.execute('CREATE TABLE IF NOT EXISTS setups (id TEXT PRIMARY KEY, persistent_message TEXT)')
    

    async def run(self):

        try:
            await self.start(self.__credentials.DISCORD.value)
        except KeyboardInterrupt:
            await self.__pool.close()
            await self.close()