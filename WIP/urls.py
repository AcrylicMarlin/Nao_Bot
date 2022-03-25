import json
from typing import Literal
import aiohttp
import discord
from discord import app_commands


class Urls(app_commands.Group):
    def __init__(self, client:discord.Client, TINYAPITOKEN:str):
        super().__init__(name = 'urls', description='Commands for urls')
        self.client = client
        self.TINYAPITOKEN = TINYAPITOKEN
    

    @app_commands.command(name = 'create', description = 'Create a new URL')
    @app_commands.describe(alias="Alias to put you URL under")
    @app_commands.describe(domain = "Domain to use")
    @app_commands.describe(url="URL to shorten")
    async def create(self, interaction:discord.Interaction, alias:str, domain:Literal["tiny.one", "roft.lol", "tinyurl.com"], url:str):
        member = interaction.user
        data = {
            "url":url,
            "alias":alias,
            "domain":domain
        }
        embed = discord.Embed()
        embed.title = "Nao_Bot Url Agent"
        desc = ""
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://api.tinyurl.com/create?api_token={self.TINYAPITOKEN}", data=data) as response:
                res = await response.json()
                if len(res['errors']) != 0:
                    desc += res['errors'][0]
                else:
                    new_url = res['data']['tiny_url']
                    desc = f"""
Original URL length: {len(url)}
New URL length: {len(new_url)}
New URL: {new_url}
"""
                ...
        embed.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=self.client.user.avatar.url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/950171863789764668/951223109724307486/url_agent.jpg")
        embed.description = desc

        await interaction.response.send_message(embed=embed)






# @tree.command(name = 'foo', description='Trial command [FOR DEVS ONLY]', guild=NAO_NATION)
# async def foo(interaction:discord.Interaction):
#     '''
#         "body":{
#         "url":interaction.guild.icon.url,
#         "domain":"tiny.one",
#         "alias":f"{interaction.guild.name}icon"
#     '''
#     if interaction.user.id == 846398473115795456 or interaction.user.id == 432613614168571904:
#         data = {
#             "url":"https://media.discordapp.net/attachments/908752890456322110/941409051126951946/IMG_7549.png?width=567&height=676",
#             "domain":"tiny.one",
#             "alias":"randommemefromserver"
#         }
        
#         async with aiohttp.ClientSession() as session:
#             async with session.post(f"https://api.tinyurl.com/create?api_token={TINYAPITOKEN}", data=data) as response:

#                 item = await response.json()
#                 embed = discord.Embed()
#                 embed.title = 'Testing aiohttp Requests'
#                 embed.description = f"""
#                 ```
#                 {json.dumps(item, indent=4)}
#                 ```
#                 """
#                 await interaction.response.send_message(embed=embed)
                

#     else:
#         await interaction.response.send_message("This command is for devs only.")

# async def initialise(*, tree:app_commands.CommandTree, client:discord.Client, NAO_NATION:discord.Object, TINYAPITOKEN:str):
#     """_summary_
#     Initialises the bot
#     Adds all of the groups to the client
#     Syncs the commands to the server
#     Later I will implement to choose between global or server side syncing
#     Args:
#         tree (app_commands.CommandTree): _description_
#         client (discord.Client): _description_
#         NAO_NATION_ID (int): _description_
#     """
#     tree.add_command(basic.Basic(client), guild=NAO_NATION)
#     tree.add_command(info.Info(client), guild=NAO_NATION)
#     tree.add_command(urls.Urls(client, TINYAPITOKEN), guild=NAO_NATION)

#     await tree.sync(guild=NAO_NATION)


# if __name__ == '__main__':
    
#     client.run(TOKEN)