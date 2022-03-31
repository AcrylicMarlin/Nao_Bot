import discord
from discord import app_commands
from discord.ext import commands


from utils import check_if_dm
from bot_classes import NaoBot
from utils.credentials import Nao_Credentials
from views import SetupModal

class Setup(commands.Cog):
    def __init__(self, client):
        self.client:NaoBot = client

    @app_commands.command(name='setup', description='Setup the bot')
    @check_if_dm()
    async def setup(self, interaction: discord.Interaction):
        async with self.client.connect_db(Nao_Credentials.DATABASE.value) as con:
            async with con.cursor() as cur:
                data = await ( await cur.execute('SELECT * FROM settings WHERE id = :id', {'id':interaction.guild.id}) ).fetchone()
                if data is None:
                    await cur.execute('INSERT INTO settings (id, wlsys, moderation, information, urls, basic) VALUES (:id, :wlsys, :moderation, :information, :urls, :basic)', {'id':interaction.guild.id, 'wlsys':0, 'moderation':0, 'information':0, 'urls':0, 'basic':0})
                    settings = {
                        'WLSYS':0,
                        'Moderation':0,
                        'Information':0,
                        'URLs':0,
                        'Basic':0
                    }
                else:
                    settings = {
                        'WLSYS':data[1],
                        'Moderation':data[2],
                        'Information':data[3],
                        'URLs':data[4],
                        'Basic':data[5]
                    }
                
        modal = SetupModal(settings)
        await interaction.response.send_modal(modal)
        await modal.wait()
        embed = discord.Embed()
        embed.title = 'Setup'
        description = ''
        for key, value in modal.setup_values.items():
            description += f'{key}: {value}\n'
        embed.description = f'```{description}```'
        await interaction.channel.send(embed=embed)

# Remember that client.add_cog is a coroutine
async def setup(client:NaoBot):
    await client.add_cog(Setup(client), guild=Nao_Credentials.NAO_NATION.value)


