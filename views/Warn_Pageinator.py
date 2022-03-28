from typing import List, Union
import discord
from discord.ui import View, Button, button
from discord import ButtonStyle



class Warns_Pageinator(View):
    message: discord.Message
    def __init__(self, pages:List[discord.Embed]):
        super().__init__(timeout = 60)
        self.page = 0
        self.page_limit = len(pages)
        self.pages = pages

    
    @button(
        label = '<<<',
        custom_id='warns_paginator:beginning',
        style = ButtonStyle.blurple
    )
    async def beginning(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        await self.message.edit(view=self, embed=self.pages[0])
        ...
    
    @button(
        label = '<',
        custom_id='warns_paginator:left',
        style = ButtonStyle.blurple
    )
    async def left(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        if self.page == 0:
            pass
        
        else:
            self.page -= 1
            await self.message.edit(view=self, embed=self.pages[self.page])
        ...
    

    @button(
        label = 'Exit',
        custom_id='warns_paginator:exit',
        style = ButtonStyle.danger
    )
    async def exit(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        self._dispatch_timeout()
        ...
    
    @button(
        label = '>',
        custom_id='warns_paginator:right',
        style = ButtonStyle.blurple
    )
    async def right(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        if self.page == self.page_limit-1:
            pass
        else:
            self.page += 1
            await self.message.edit(view=self, embed=self.pages[self.page])
        ...
    
    @button(
        label = '>>>',
        custom_id='warns_paginator:end',
        style = ButtonStyle.blurple
    )
    async def end(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        await self.message.edit(view=self, embed=self.pages[self.page_limit-1])
        ...



    async def on_timeout(self) -> None:
        for child in self.children:
            assert isinstance(child, Union[discord.ui.Button, discord.ui.Select])
            child.disabled = True
            ...
        await self.message.edit(view=self)

        
        