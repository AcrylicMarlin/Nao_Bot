from typing import List, Union
import discord
from discord.ui import View, Button, button
from discord import ButtonStyle



class Warns_Pageinator(View):
    def __init__(self, pages:List[discord.Embed]):
        super().__init__(timeout = 60)
        self.page = 0
        self.page_limit = len(pages)
        
    
    @button(
        label = '<<<',
        custom_id='warns_paginator:beginning',
        style = ButtonStyle.blurple
    )
    async def beginning(self, interaction:discord.Interaction, button:discord.Button):
        ...
    
    @button(
        label = '<',
        custom_id='warns_paginator:left',
        style = ButtonStyle.blurple
    )
    async def left(self, interaction:discord.Interaction, button:discord.Button):
        ...
    

    @button(
        label = 'Exit',
        custom_id='warns_paginator:exit',
        style = ButtonStyle.danger
    )
    async def exit(self, interaction:discord.Interaction, button:discord.Button):
        ...
    
    @button(
        label = '>',
        custom_id='warns_paginator:right',
        style = ButtonStyle.blurple
    )
    async def right(self, interaction:discord.Interaction, button:discord.Button):
        ...
    
    @button(
        label = '>>>',
        custom_id='warns_paginator:end',
        style = ButtonStyle.blurple
    )
    async def end(self, interaction:discord.Interaction, button:discord.Button):
        ...
    


    async def on_timeout(self) -> None:
        for child in self.children:
            assert isinstance(child, Union[discord.ui.Button, discord.ui.Select])
            child.disabled = True
            ...
        assert isinstance(self.message, discord.Message)
        await self.message.edit(view=self)

        
        