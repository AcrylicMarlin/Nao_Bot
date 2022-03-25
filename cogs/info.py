import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from bot_class import NaoBot


class Info(commands.Cog):
    def __init__(self, client:NaoBot):
        self.client:commands.Bot= client

    @app_commands.command(name = 'bot', description='Information on the bot')
    async def bot(self, interaction:discord.Interaction):
        embed = discord.Embed()
        embed.title = "Nao_Bot Information"
        member_count = 0
        for guild in self.client.guilds:
            member_count += guild.member_count
        embed.description = f"""
Mention - {self.client.user.mention}
Name - {self.client.user.display_name}
ID - {self.client.user.id}
Number of guilds - {len(self.client.guilds)}
Number of members - {member_count}
"""
        await interaction.response.send_message(embed = embed)
        ...
    @app_commands.command(name = 'member', description='Information on a member')
    @app_commands.describe(member = "Member to get info of. Defaults to yourself")
    async def member(self, interaction:discord.Interaction, member:Optional[discord.Member]):
        if not member:
            member = interaction.user
        
        embed = discord.Embed()
        embed.title = f"{member.display_name}'s information"
        role_string = ''
        for role in member.roles[1:]:
            role_string += role.mention + ', '
        
        embed.description = f"""
Mention: {member.mention}
Name: {member.display_name}
ID: {member.id}
Joined Server: <t:{int(member.joined_at.timestamp())}:R>
Joined Discord: <t:{int(member.created_at.timestamp())}:R>
Roles: {role_string [:-2]}
"""
        embed.set_thumbnail(url = member.display_avatar)
        embed.set_footer(text = f'{member.display_name}', icon_url=member.display_avatar)
        await interaction.response.send_message(embed = embed)
        ...
    
    @app_commands.command(name='server', description='Gets info on the server')
    async def server(self, interaction:discord.Interaction):

        embed = discord.Embed()
        embed.title = f'Info for {interaction.guild.name}'

        embed.description = f"""
Name - {interaction.guild.name}
ID - {interaction.guild.id}
Members - {interaction.guild.member_count}
Created - <t:{int(interaction.guild.created_at.timestamp())}:R>
"""
        embed.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=interaction.guild.icon)

        await interaction.response.send_message(embed=embed)
        ...


async def setup(client):
    await client.add_cog(Info(client))