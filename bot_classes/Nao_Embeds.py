from datetime import datetime, timezone
import discord

class SpecialEmbed(discord.Embed):
    def __init__(self):
        super().__init__()
        self.color = discord.Color.blue()
        self.timestamp = datetime.now()
        self.set_footer(text='Nao!', icon_url='https://cdn.discordapp.com/avatars/928269449407102987/20db57ab5bfda6b8308af2e891d345f5.png?size=1024')

class ErrorEmbed(SpecialEmbed):
    def __init__(self, error:Exception):
        super().__init__()
        self.description = f'An error has occured while executing the command\nError:```{str(error)}```'
        
        

    