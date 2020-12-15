# First file for OMOBot

import discord 
from dotenv import load_dotenv
import os


load_dotenv('.env')
omobot = discord.Client()



omobot.run(os.getenv('OMOBOT_TOKEN'))