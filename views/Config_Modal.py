from typing import Dict
from discord import (
    Embed,
    Message,
    TextStyle,
    Interaction
)
from discord.ui import Modal, TextInput

class ConfigModal(Modal):

    
    def __init__(self, current_settings:Dict[str, int]):
        super().__init__(title='Please enter either Yes or No', timeout = 60)

        self.setup_values:Dict[str, TextInput | str] = {
        'WLSYS':TextInput(placeholder='WLSYS', style = TextStyle.short, label='WLSYS', custom_id='setup_modal:wlsys'),
        'Moderation':TextInput(placeholder='Moderation', style = TextStyle.short, label='Moderation', custom_id='setup_modal:moderation'),
        'Information':TextInput(placeholder='Information', style = TextStyle.short, label='Information', custom_id='setup_modal:information'),
        'URLs':TextInput(placeholder='URLs', style = TextStyle.short, label='URLs', custom_id='setup_modal:urls'),
        'Basic':TextInput(placeholder='Basic', style = TextStyle.short, label='Basic', custom_id='setup_modal:basic')
        }
        for value in self.setup_values.values():
            value.placeholder = current_settings.get(value.label, value.placeholder)
            if value.placeholder == 0:
                value.placeholder = 'No'
            else:
                value.placeholder = 'Yes'

            self.add_item(value)
    
    async def on_submit(self, interaction: Interaction) -> Dict[str, str]:
        await interaction.response.send_message('Changing your settings...')
        interaction.message.__getattribute__('content')
        self.stop()
        
        ...
    
    async def on_timeout(self) -> None:
        self.stop()
        
    
