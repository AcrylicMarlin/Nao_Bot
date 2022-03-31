import os
import aiohttp
from discord import (
    Attachment,
    File,
    Message,
    SelectOption,
    Embed,
    ButtonStyle,
    Interaction
)
from discord.ui import (
    View,
    Button,
    Select,
    button,
)
from typing import List, Any


class FilesPaginator(View):
    current_page: int = 0
    page_limit: int
    pages: List[str]
    embed:Embed
    extra_message:Message
    def __init__(self, pages:List[str]):
        self.page_limit = len(pages)
        self.pages = pages
        super().__init__(timeout=30)
        self.embed = Embed()
        self.embed.title = 'Files'
        self.embed.set_footer(text='Page {}/{}'.format(self.current_page+1, self.page_limit))
        self.extra_message = None
        ...


    @button(
        label='<<<',
        custom_id='files_paginator:beginning',
        style=ButtonStyle.blurple
    )
    async def beginning(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        self.current_page = 0
        file = await self.update_page()
        assert isinstance(self.message, Message)
        if not file:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
        else:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
            self.extra_message = await self.message.channel.send(file=file)
            if os.path.exists(f'{self.pages[self.current_page]}'):
                os.remove(f'{self.pages[self.current_page]}')
        ...
    


    @button(
        label='<',
        custom_id='files_paginator:previous',
        style=ButtonStyle.blurple
    )
    async def previous(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        self.current_page -= 1
        file = await self.update_page()
        assert isinstance(self.message, Message)
        if not file:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
        else:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
            self.extra_message = await self.message.channel.send(file=file)
            if os.path.exists(f'{self.pages[self.current_page]}'):
                os.remove(f'{self.pages[self.current_page]}')
        ...


    @button(
        label = 'Exit',
        custom_id = 'files_paginator:exit',
        style = ButtonStyle.danger
    )
    async def exit(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        self._dispatch_timeout()
        ...


    @button(
        label='>',
        custom_id='files_paginator:next',
        style=ButtonStyle.blurple
    )
    async def next(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        self.current_page += 1
        file = await self.update_page()
        assert isinstance(self.message, Message)

        if not file:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
        else:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
            self.extra_message = await self.message.channel.send(file=file)
            if os.path.exists(f'{self.pages[self.current_page]}'):
                os.remove(f'{self.pages[self.current_page]}')
        ...


    @button(
        label='>>>',
        custom_id='files_paginator:end',
        style=ButtonStyle.blurple
    )
    async def end(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        self.current_page = self.page_limit - 1
        file = await self.update_page()
        assert isinstance(self.message, Message)

        if not file:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
        else:
            try:
                await self.extra_message.delete()
            except:
                pass
            await self.message.edit(embed=self.embed)
            self.extra_message = await self.message.channel.send(file=file)
            if os.path.exists(f'{self.pages[self.current_page]}'):
                os.remove(f'{self.pages[self.current_page]}')

    









    async def update_page(self):
        self.embed.set_footer(text='Page {}/{}'.format(self.current_page+1, self.page_limit))
        if '.' + self.pages[self.current_page].split('.')[1] in ['.js', '.html', '.ts', '.py', '.css', '.json', '.txt', '.lock', '.toml', '.md', '.zip']:
            if self.pages[self.current_page].split('.')[1] == 'zip':
                self.embed.set_image(url='')
                self.embed.description = self.pages[self.current_page] + " is not currently supported LOL"
                return None
            async with aiohttp.ClientSession('https://cdn.nao.gg/') as session:
                async with session.get("/" + self.pages[self.current_page]) as response:
                    respBytes = await response.read()

                    file = open(f'{self.pages[self.current_page]}', 'wb')
                    file = file.write(respBytes)
                    file = File(f'{self.pages[self.current_page]}', filename = self.pages[self.current_page])
                    self.embed.set_image(url='')
                    self.embed.description = self.pages[self.current_page]
                    self.embed.set_image(url='')
                    return file
                ...
        else:
            self.embed.description = f'```{self.pages[self.current_page]}```'
            self.embed.set_image(url=f'https://cdn.nao.gg/{self.pages[self.current_page]}')
    




    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)