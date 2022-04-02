import discord
from discord import app_commands
from discord.ext import commands


from utils import check_if_dm
from bot_classes import NaoBot
from utils.credentials import Nao_Credentials
from views import ConfigModal

class Config(commands.Cog):
    def __init__(self, client):
        self.client:NaoBot = client

    @app_commands.command(name='config', description='Configure the bot')
    @check_if_dm()
    async def config(self, interaction: discord.Interaction):
        new_server = False
        async with self.client.connection.cursor() as cur:
            data = await (await cur.execute('SELECT * FROM settings WHERE id = :id', {'id':interaction.guild.id}) ).fetchone()
            if data is None:
                await cur.execute('INSERT INTO settings (id, wlsys, moderation, information, urls, basic) VALUES (:id, :wlsys, :moderation, :information, :urls, :basic)', {'id':interaction.guild.id, 'wlsys':0, 'moderation':0, 'information':0, 'urls':0, 'basic':0})
                settings = {
                    'WLSYS':0,
                    'Moderation':0,
                    'Information':0,
                    'URLs':0,
                    'Basic':0
                }
                new_server = True
            else:
                settings = {
                    'WLSYS':data[1],
                    'Moderation':data[2],
                    'Information':data[3],
                    'URLs':data[4],
                    'Basic':data[5]
                }
                
        modal = ConfigModal(settings)
        await interaction.response.send_modal(modal)
        await modal.wait()
        for key, value in modal.setup_values.items():
            if value.value.lower() == 'yes':
                modal.setup_values[key] = 1
            elif value.value.lower() == 'no':
                modal.setup_values[key] = 0
            else:
                modal.setup_values[key] = -1
        
        emojis = ['👋 ', '🔨 ', '📝 ', '🔗 ', '🔎 ']
        embed = discord.Embed(title='Setup', description='Changing settings...', color=discord.Color.random())


        i = 0
        for key, value in modal.setup_values.items():
            embed.add_field(
                name= emojis[i] + key, 
                value=bool(value) if value >= 0 else 'Invalid input, not changed.',
                inline=False
            )

            i += 1
        query = 'UPDATE settings SET wlsys = :wlsys, moderation = :moderation, information = :information, urls = :urls, basic = :basic WHERE id = :id'
        async with self.client.connection.cursor() as cur:
            await cur.execute(query, {
                'wlsys':modal.setup_values['WLSYS'] if modal.setup_values['WLSYS'] >= 0 else settings['WLSYS'],
                'moderation':modal.setup_values['Moderation'] if modal.setup_values['Moderation'] >= 0 else settings['Moderation'],
                'information':modal.setup_values['Information'] if modal.setup_values['Information'] >= 0 else settings['Information'],
                'urls':modal.setup_values['URLs'] if modal.setup_values['URLs'] >= 0 else settings['URLs'],
                'basic':modal.setup_values['Basic'] if modal.setup_values['Basic'] >= 0 else settings['Basic'],
                'id':interaction.guild.id
                })
            ...
        await interaction.channel.send(embed=embed)
        
    
    @app_commands.command(name='config_help', description='Help for config')
    @check_if_dm()
    async def config_help(self, interaction: discord.Interaction):
        embed = discord.Embed()
        embed.title = 'Setup Help'
        embed.description = """
This command is used to enable/disable certain features of the bot.
This is for guild channels only and will not work in DMs.

**WLSYS: The Welcome and Leave system.**
    - Sends a welcome message in a channel when a user joins the server.
    - Sends a leave message in a channel when a user leaves the server.
**Moderation: The moderation system.**
    - Useful commands to moderate the server.
    - Ban, Kick, Timeout, Warn, etc.
**Information: The information system.**
    - Useful commands to get information about the server, a member, or myself.
**URLs: The URLs system.**
    - Useful commands to shorten long urls.
    - Store them in a database so you can get them later.
**Basic: The basic system.**
    - Simple commands. 
    - Get my latency, make me say something, etc.

***More comming soon...***
        """
        time = interaction.created_at.time()
        embed.set_footer(text=f'Requested by {interaction.user.display_name} at {time.strftime("%H:%M:%S %p")}', icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        

    async def setup_moderation():
        ...
    
    async def setup_wlsys():
        ...
    




# Remember that client.add_cog is a coroutine
async def setup(client:NaoBot):
    await client.add_cog(Config(client), guild=Nao_Credentials.NAO_NATION.value)


