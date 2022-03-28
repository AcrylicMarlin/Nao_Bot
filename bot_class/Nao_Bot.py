from typing import Dict, Any
from pathlib import Path
import sys
import traceback


from discord.ext import commands
import discord
import asqlite

from utils import Nao_Credentials, CogLoadFailure

log_format = (
        '%(asctime)s - '
        '%(name)s - '
        '%(funcName)s - '
        '%(levelname)s - '
        '%(message)s'
)
# Setup logging using the above format
import logging
logging.basicConfig(format=log_format, level=logging.INFO, filename='utils/Nao.log')
class NaoBot(commands.Bot):
    __intents:discord.Intents
    NAO_NATION:discord.Object
    __status:discord.Status
    __activity:discord.Activity
    __credentials:Nao_Credentials
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
        super().__init__('!', intents = self.__intents, application_id = 928269449407102987)
        
    

    @property
    def credentials(self) -> Nao_Credentials:
        return self.__credentials
    
    
    async def on_ready(self):
        print('{} is operational'.format(self.user.name))
    
    async def setup_commands(self):
        for file in Path('cogs').glob('**/*.py'):
            *tree, _ = file.parts
            try:
                if not file.stem.startswith('_'):
                    cog = f"{'.'.join(tree)}.{file.stem}"
                    await self.load_extension(cog)
                    print(f"{cog} loaded successfully!")

            except Exception as e:
                raise CogLoadFailure(file.stem, e)
        
        await self.tree.sync(guild=Nao_Credentials.NAO_NATION.value)
        
        ...
    async def setup_hook(self):
        self.activity = self.__activity
        self.status = self.__status
        self.connect_db = asqlite.connect
        tables = [
            'CREATE TABLE IF NOT EXISTS pers_messages (id TEXT PRIMARY KEY, persistent_message TEXT)',
            'CREATE TABLE IF NOT EXISTS guilds (id TEXT, name TEXT, count INT)',
            'CREATE TABLE IF NOT EXISTS warns (id TEXT, guild_id TEXT, user_id TEXT, moderator_id TEXT, reason TEXT, time INT)'
        ]
        
        async with self.connect_db(self.credentials.DATABASE.value) as con:
            async with con.cursor() as cur:
                for table in tables:
                    logging.info(f'Using Query   {table}')
                    await cur.execute(table)


        await self.setup_commands()
        
    

    async def run(self):

        try:
            await self.start(self.credentials.DISCORD.value)
        except KeyboardInterrupt:
            await self.__pool.close()
            await self.close()

    

    async def on_guild_join(self, guild:discord.Guild):
        async with self.connect_db(self.credentials.DATABASE.value) as con:
            async with con.cursor() as cur:
                await cur.execute('INSERT INTO guilds VALUES (:id, :name, :count)', {'id':guild.id, 'name':guild.name, 'count': guild.member_count if guild.member_count else 1})
                print('Joined {}'.format(guild.name))


    async def on_guild_remove(self, guild:discord.Guild):
        async with self.connect_db(self.credentials.DATABASE.value) as con:
            async with con.cursor() as cur:
                await cur.execute('DELETE FROM guilds WHERE id = :id', {'id':guild.id})


    async def on_command_error(self, ctx:commands.Context, error: commands.errors.CommandError) -> None:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        ...

    # Everytime a command is invoked, this function is called
    async def on_command_completion(self, ctx:commands.Context) -> None:
        logging.info(f'{ctx.author.name} used command {ctx.command}')
    
    
