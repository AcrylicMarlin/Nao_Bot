from discord.ext import commands
from discord import app_commands

class NaoError(Exception):
    def __init__(self, message:str):
        super().__init__(message)

class CogLoadFailure(NaoError):
    def __init__(self, cog:str, reason:Exception):
        super().__init__("Cog {} failed to load.\nReason: {}".format(cog, reason))

class NaoAppError(app_commands.AppCommandError):
    def __init__(self, message:str):
        super().__init__(message)
class NotDmChannel(NaoError):
    def __init__(self):
        super().__init__("This command can only be used in a DM channel.")

class IsDmChannel(NaoAppError):
    def __init__(self):
        super().__init__("This command cannot be used in a DM channel.")

class NotAuthorized(NaoError):
    def __init__(self):
        super().__init__("You are not authorized to use this command.")
