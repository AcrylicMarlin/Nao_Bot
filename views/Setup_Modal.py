from typing import Dict
from discord import (
    Embed,
    Message,
    TextStyle,
    Interaction
)
from discord.ui import Modal, TextInput

class SetupModal(Modal):

    setup_values:Dict[str, TextInput | str] = {
        'wlsys':TextInput(placeholder='WLSYS', style = TextStyle.short, label='WLSYS', custom_id='setup_modal:wlsys'),
        'moderation':TextInput(placeholder='Moderation', style = TextStyle.short, label='Moderation', custom_id='setup_modal:moderation'),
        'information':TextInput(placeholder='Information', style = TextStyle.short, label='Information', custom_id='setup_modal:information'),
        'urls':TextInput(placeholder='URLs', style = TextStyle.short, label='URLs', custom_id='setup_modal:urls'),
        'basic':TextInput(placeholder='Basic', style = TextStyle.short, label='Basic', custom_id='setup_modal:basic')
    }
    def __init__(self, current_settings:Dict[str, int]):
        super().__init__(title='Setup', timeout = 60)
        for value in self.setup_values.values():
            value.placeholder = current_settings.get(value.label, value.placeholder)
            self.add_item(value)
    
    async def on_submit(self, interaction: Interaction) -> Dict[str, str]:
        await interaction.response.send_message('Setup is not yet implemented')
        return self.setup_values
        ...
        
    
