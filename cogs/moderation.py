
import datetime
from typing import List, Optional
import uuid

import discord
from discord.ext import commands
from discord import NotFound, app_commands

from bot_classes import NaoBot
from utils import Nao_Credentials
from views import Warns_Pageinator

class Moderation(commands.Cog):
    def __init__(self, client):
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
    @app_commands.describe(id = 'ID of the banned user', reason = 'Reason for unban')
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




    
    @app_commands.command(name='timeout')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to timeout', time = 'Amount of time', reason='Reason for timeout')
    async def timeout(self, interaction:discord.Interaction, member:discord.Member, time:str, *, reason:str=None):
        if time.endswith('s'):
            time = int(time[:-1])
            if time > 60:
                return await interaction.response.send_message('You can only provide up to 60 seconds')
        elif time.endswith('m'):
            time = int(time[:-1]) * 60
            if time > 3600:
                return await interaction.response.send_message('You can only provide up to 60 minutes')
        elif time.endswith('h'):
            time = int(time[:-1]) * 3600
            if time > 86400:
                return await interaction.response.send_message('You can only provide up to 24 hours')
        elif time.endswith('d'):
            time = int(time[:-1]) * 86400
            if time > 2592000:
                return await interaction.response.send_message('You can only provide up to 30 days')
        else:
            return await interaction.response.send_message('Incorrect time format. Time must be in seconds [s], minutes [m], hours [h] or days [d] and must be less than thirty days.')
        
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message('You do not have permission to use this command')
            return
        else:
            timed = datetime.timedelta(seconds=time)
            await member.timeout(timed, reason=reason)

        try:
            amount = datetime.datetime.now() + timed
            await member.send('You have been timed out until <R:{}:t> for {}'.format(int(amount.timestamp()), reason))
        except Exception:
            pass




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
                    warn_id = uuid.uuid4().__str__()
                    await cur.execute(
                        'INSERT INTO warns VALUES (:id, :guild_id, :user_id, :moderator_id, :reason, :time)',
                        {
                            'id':warn_id,
                            'guild_id':str(interaction.guild.id),
                            'user_id':str(member.id),
                            'reason':reason,
                            'moderator_id':str(interaction.user.id),
                            'time':int(interaction.created_at.timestamp())
                        }
                    )
            await interaction.response.send_message('Warned {} for {}'.format(member.mention, reason))
    



    @app_commands.command(name = 'warns')
    @app_commands.guilds(Nao_Credentials.NAO_NATION.value)
    @app_commands.describe(member='Member to get warns from. Defaults to yourself')
    async def get_warns(self, interaction:discord.Interaction, member:Optional[discord.Member]):
        if not member:
            member = interaction.user
        guild = interaction.guild
        await interaction.response.send_message(f'Gathering {member.name}\' warns...')
        pages:List[discord.Embed] = []
        async with self.client.connect_db(Nao_Credentials.DATABASE.value) as con:
            async with con.cursor() as cur:
                data = await (await cur.execute('SELECT * FROM warns WHERE user_id = :user_id AND guild_id = :guild_id', {'user_id':member.id, 'guild_id':interaction.guild.id})).fetchall()
                if not data:
                    await interaction.channel.send('No warns found')
                    return
                
                
                i=0
                for row in data:
                    embed = discord.Embed()
                    embed.title = f"Page {i}"
                    id, guild_id, user_id, moderator_id, reason, time = row
                    moderator = await interaction.guild.fetch_member(moderator_id)
                    embed.description = f"""
ID: `{id}`
Guild: {guild.name}
User: {member.mention}
Reason: ```{reason}```
Moderator: {moderator.mention}
Time: <t:{time}:R>
"""
                    i+=1
                    pages.append(embed)
        
        view = Warns_Pageinator(pages)
        view.message = await interaction.channel.send(embed = pages[0], view = view)
        
        ...

async def setup(client:NaoBot):
    await client.add_cog(Moderation(client), guild=Nao_Credentials.NAO_NATION.value)
