"""
This is probably the coolest thing I have made with Discord.py
Everything is explained below

Later, I will make it optional to preview a file, too make scrolling smoother
I will also make it so you can sort by file type
"""
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


class FilesPageinator(View):
    current_page: int = 0
    page_limit: int
    pages: List[str]
    embed:Embed
    extra_message:Message
    def __init__(self, pages:List[str], session:aiohttp.ClientSession):
        self.page_limit = len(pages) 
        self.pages = pages 
        super().__init__(timeout=30)
        self.embed = Embed()
        self.embed.title = 'Files'
        self.embed.set_footer(text='Page {}/{}'.format(self.current_page+1, self.page_limit))
        self.extra_message = None # Explained later
        self.session = session # Our bots client session with the CDN
        ...


    @button(
        label='<<<',
        custom_id='files_paginator:beginning',
        style=ButtonStyle.blurple
    )
    async def beginning(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        self.current_page = 0
        file = await self.update_page() # This function is where the magic happens
        assert isinstance(self.message, Message) # this is just typehinting


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
        if self.current_page == 0:
            pass
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
        # Self explanatory
        self._dispatch_timeout()
        ...


    @button(
        label='>',
        custom_id='files_paginator:next',
        style=ButtonStyle.blurple
    )
    async def next(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        if self.current_page == self.page_limit - 1:
            pass
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
        
        # Im gonna use this as an example
        # First it checks if the file exists
        # if not deletes the extra message and send the embed normally
        # (The embed will just have an attached image)
        # If the file does exist, it deletes the extra message (if one exists)
        # And sends a new one containing the file
        # I couldn't just edit the message with the file because it doesn't allow that
        # For some reason...
        # Also it removes the file here, because if I deleted in update_embed, it wouldn't exist anymore lol
        # This method is implemented exactly the same everywhere.

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
        """
        This function is where all the magic happens. Its not difficult to understand, but its cool af.

        Returns:
            Optional[discord.File]
        """
        self.embed.set_footer(text='Page {}/{}'.format(self.current_page+1, self.page_limit)) # Changes the page number
        if '.' + self.pages[self.current_page].split('.')[1] in ['.js', '.html', '.ts', '.py', '.css', '.json', '.txt', '.lock', '.toml', '.md', '.zip']: # Checks if the file is a Raw text/code file

            if self.pages[self.current_page].split('.')[1] == 'zip': # I haven't quite figured out how I could represent a zip file
                self.embed.set_image(url='')
                self.embed.description = self.pages[self.current_page] + " is not currently supported LOL"
                return None

            """
            This asyncs with the file page, downloads it as bytes, writes it to a file, sends that file as bytes, then deletes it
            I had to do this because the bytes would come from the CDN as html bytes, it needed to be bytes of that file type to work properly
            """
            async with self.session.get("/" + self.pages[self.current_page]) as response:
                respBytes = await response.read()
                # Open, Write, Read
                file = open(f'{self.pages[self.current_page]}', 'wb')
                file = file.write(respBytes)
                file = File(f'{self.pages[self.current_page]}', filename = self.pages[self.current_page])

                # Resets the embed
                self.embed.set_image(url='')
                self.embed.description = self.pages[self.current_page]
                return file
            ...
        else:
            self.embed.description = f'```{self.pages[self.current_page]}```'
            self.embed.set_image(url=f'https://cdn.nao.gg/{self.pages[self.current_page]}')
    



    # Just loops through and disables children
    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)