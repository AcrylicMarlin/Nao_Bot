import asyncio
from datetime import datetime
import json
import os
from typing import Dict, Any
from pathlib import Path
import sys
import traceback
import aiohttp


from discord.ext import commands
from discord import app_commands
import discord
import asqlite

from utils import Nao_Credentials, CogLoadFailure, NotDmChannel

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
    activity:discord.Activity,
    tree_cls:app_commands.CommandTree,):
        self.__intents = intents
        self.__status = status
        self.__activity = activity
        self.__credentials = Nao_Credentials
        self.__persistent_views = False
        super().__init__('!', intents = self.__intents, application_id = 928269449407102987, tree_cls=tree_cls)
        
    

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

        
        tables = [
            """
            CREATE TABLE IF NOT EXISTS guilds (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                count INTEGER NOT NULL,
                settings TEXT, NOT NULL,
                pers_messages TEXT NOT NULL UNIQUE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS warns (
                guild_id TEXT NOT NULL,
                warn_id TEXT NOT NULL UNIQUE,
                user_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                time TEXT NOT NULL,
                moderator_id TEXT NOT NULL,
                CONSTRAINT guild_id_fk FOREIGN KEY (guild_id) REFERENCES guilds (id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS urls (
                user_id TEXT NOT NULL,
                url TEXT NOT NULL,
                time TEXT NOT NULL,
            )
            """
        ]
        # tables = [
        #     'CREATE TABLE IF NOT EXISTS pers_messages (id TEXT PRIMARY KEY, persistent_message TEXT)',
        #     'CREATE TABLE IF NOT EXISTS guilds (id TEXT PRIMARY KEY, name TEXT, count INT, config_status TEXT)',
        #     'CREATE TABLE IF NOT EXISTS warns (id TEXT PRIMARY KEY, guild_id TEXT UNIQUE, user_id TEXT UNIQUE, moderator_id TEXT, reason TEXT, time INT)',
        #     'CREATE TABLE IF NOT EXISTS settings (id TEXT PRIMARY KEY, wlsys BIT, moderation BIT, information BIT, urls BIT, basic BIT)'
        # ]
        
        async with self.connection.cursor() as cur:
            for table in tables:
                logging.info(f'Using Query   {table}')
                await cur.execute(table)


        await self.setup_commands()


    async def run(self):
        try:
            async with self:
                async with aiohttp.ClientSession('https://cdn.nao.gg/', timeout = aiohttp.ClientTimeout(15)) as session:
                    self.session = session
                    async with asqlite.connect(self.credentials.DATABASE.value) as connection:
                        self.connection = connection
                        await self.start(self.credentials.DISCORD.value)
        except KeyboardInterrupt:
            await self.close()

    

    async def on_guild_join(self, guild:discord.Guild):
        config = {
            'wlsys':False,
            'moderation':False
        }
        async with self.connection.cursor() as cur:
                querys = [
                    ['INSERT INTO guilds (id, name, count) VALUES (:id, :name, :count, :config_status)', {'id':guild.id, 'name':guild.name, 'count':0, 'config_status':json.dumps(config)}]
                ]
                for query in querys:
                    logging.info(f'Using Query   {query[0]}')
                    await cur.execute(query[0], query[1])
        embed = discord.Embed()
        embed.title = 'Thanks for adding me to your server!'
        embed.description = """
        We greatly appreciate you adding us to your server family.
        
        Currently I have very limited functionality, but that can be fixed by running `/config` in the server.
        """
        time = datetime.now()
        time_str = time.time().strftime('%H:%M:%S %p')
        embed.set_footer(text = guild.owner.display_name + time_str, icon_url = guild.owner.avatar.url)
        try:
            await guild.owner.send(embed = embed)
        except:
            pass

            


    async def on_guild_remove(self, guild:discord.Guild):
        async with self.connect_db(self.credentials.DATABASE.value) as con:
            querys = [
                ['DELETE FROM guilds WHERE id = :id', {'id':guild.id}],
                ['DELETE FROM settings WHERE id = :id', {'id':guild.id}],
                ['DELETE FROM warns WHERE guild_id = :id', {'id':guild.id}],
                ['DELETE FROM pers_messages WHERE id = :id', {'id':guild.id}]
            ]
            async with con.cursor() as cur:
                for query in querys:
                    logging.info(f'Using Query   {query[0]}')
                    await cur.execute(query[0], query[1])



    async def on_command_error(self, ctx: commands.Context, error: commands.errors.CommandError, /) -> None:
        embed = discord.Embed()
        embed.title = 'Error'
        embed.color = discord.Color.red()
        embed.set_footer(text='Nao Nation', icon_url=self.user.avatar.url)
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        
        if isinstance(error, asyncio.exceptions.TimeoutError):
            embed.description = '```The CDN failed to respond in time.\nPlease try again later.```'
            await ctx.send(embed=embed)
            return
        embed.description = f'An error has occured while executing the command\nError:```{error}```'
        await ctx.send(embed = embed)

        print('Ignoring {} in command {}:'.format(type(error), ctx.command.name), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        logging.error(f'Ignoring {type(error)} in command {ctx.command.name}: {error}')

    # Everytime a command is invoked, this function is called
    async def on_command_completion(self, ctx:commands.Context) -> None:
        logging.info(f'{ctx.author.name} used command {ctx.command}')

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        error_type, error, error_traceback = sys.exc_info()

        if event_method == 'on_message':
            message = args[0]
            embed = discord.Embed()
            embed.title = 'Error'
            embed.color = discord.Color.red()
            embed.set_footer(text='Nao Nation', icon_url=self.user.avatar.url)
            embed.description = f'An error has occured while executing the command\nError:```{str(error)}```'

            await message.channel.send(embed = embed)
            print('Ignoring {} in {}:'.format(error_type, event_method), file=sys.stderr)
            traceback.print_exception(error_type, error, error_traceback, file=sys.stderr)
            logging.error(f'Ignoring {type(error)} in {event_method}: \n{error}')