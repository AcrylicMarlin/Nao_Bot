from enum import Enum
from typing import Any, Dict
import os

import discord
from dotenv import load_dotenv
load_dotenv()

# Gathering Credentials
TOKEN = os.environ.get('TOKEN')
TINYAPITOKEN = os.environ.get('TINYAPITOKEN')
CDNTOKEN = os.environ.get('CDNTOKEN')
NAO_NATION_ID = 695025143264706622
NAO_NATION = discord.Object(id = NAO_NATION_ID)
P_USER = os.environ.get('P_USER')
P_PASS = os.environ.get('P_PASS')
P_PORT = os.environ.get('P_PORT')
P_DB = os.environ.get('P_DB')
POSTGRES = {"user":P_USER, "password":P_PASS, "database":P_DB}



# I used an Enum class here because:
# 1. It's cool
# 2. Cleaner and easier to pass around files.
# This never needs to be instantiated
class Nao_Credentials(Enum):
    POSTGRES:Dict[str, Any] = POSTGRES # I have postgres information here, but I don't think I will use it
    DISCORD:str = TOKEN
    TINYURL:str = TINYAPITOKEN
    NAO_NATION:discord.Object = NAO_NATION
    DATABASE:str = 'Nao_Data.db'
    CDN:str = CDNTOKEN