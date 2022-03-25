from discord import app_commands

class HelperError(Exception):
    def __init__(self, message:str):
        super().__init__(message)

class CogLoadFailure(HelperError):
    def __init__(self, cog:str, reason:Exception):
        super().__init__("Cog {} failed to load.\nReason: {}".format(cog, reason))