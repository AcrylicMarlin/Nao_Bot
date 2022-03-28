from pydoc import describe
from typing import Optional
import uuid

import discord
from discord.ext import commands
from discord import NotFound, app_commands

from bot_class import NaoBot
from utils import Nao_Credentials

class Moderation(commands.Cog):
    def __init__(self, client:NaoBot):
        self.client = client

    @app_commands.command(name='kick')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to kick', reason='Reason for kicking')
    async def kick(self, interaction:discord.Interaction, member: discord.Member, *, reason: str = None):
        await interaction.guild.kick(member, reason=reason)
        await interaction.response.send_message('Kicked {} for {}'.format(member.mention, reason))
        try:
            await member.send('You have been kicked from {} for {}'.format(interaction.guild.name, reason))
        except Exception:
            pass
    
    @app_commands.command(name='ban')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to ban', reason='Reason for banning')
    async def ban(self, interaction:discord.Interaction, member: discord.Member, *, reason: str = None):
        await interaction.guild.ban(member, reason=reason)
        await interaction.response.send_message('Banned {} for {}'.format(member.mention, reason))
        try:
            await member.send('You have been banned from {} for {}'.format(interaction.guild.name, reason))
        except Exception:
            pass

    @app_commands.command(name='unban')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to unban')
    async def unban(self, interaction:discord.Interaction, id: int, *, reason: str = None):
        try:
            member = await interaction.guild.fetch_ban(id)
            await interaction.guild.unban(member, reason=reason)
            await interaction.response.send_message('Unbanned {} for {}'.format(member.mention, reason))
        except NotFound:
            await interaction.response.send_message('Could not find ban with id {}'.format(id))
    
    @app_commands.command(name='purge')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(limit='Number of messages to delete')
    async def purge(self, interaction:discord.Interaction, limit: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message('You do not have permission to use this command')
            return
        await interaction.channel.purge(limit=limit)
        await interaction.response.send_message('Purged {} messages'.format(limit), ephemeral=True)

    
    @app_commands.command(name='mute')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to mute', reason='Reason for muting')
    async def timeout(self, interaction:discord.Interaction, member:discord.Member, *, reason:str=None):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message('You do not have permission to use this command')
            return
        else:
            await member.timed_out_until(interaction.guild, reason=reason)

    @app_commands.command(name='warn')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to warn', reason='Reason for warning')
    async def warn(self, interaction:discord.Interaction, member:discord.Member, *, reason:str=None):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message('You do not have permission to use this command')
            return
        else:
            async with self.client.connect_db(Nao_Credentials.DATABASE.value) as con:
                async with con.cursor() as cur:
                    warn_id = uuid.uuid4()
                    await cur.execute(
                        'INSERT INTO warns VALUES (:id, :guild_id, :user_id, :reason, :moderator_id, :time)',
                        {
                            'id':warn_id,
                            'guild_id':interaction.guild.id,
                            'user_id':member.id,
                            'reason':reason,
                            'moderator_id':interaction.user.id,
                            'time':int(interaction.created_at.timestamp())
                        }
                    )
    
    @app_commands.command(name = 'get warns')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to get warns from. Defaults to yourself')
    async def get_warns(self, interaction:discord.Interaction, member:Optional[discord.Member]):
        embed = discord.Embed()
        embed.title = f"{member.name}'s warns"
        description = ''
        async with self.client.connect_db(Nao_Credentials.DATABASE.value) as con:
            async with con.cursor() as cur:
                data = await (await cur.execute('SELECT * FROM warns WHERE user_id = :user_id AND guild_id = :guild_id')).fetchall()
                i=0
                for row in data:
                    id, guild_id, user_id, reason, moderator_id, time = row
                    moderator = await interaction.guild.get_member(moderator_id)
                    description += f"{i}. {id} - {reason} - Given by: {moderator} - <:t>{time}<:R>"
                    i+=1
        
        embed.description = description
        await interaction.response.send_message(embed=embed)
        ...

async def setup(client):
    client.add_cog(Moderation(client))