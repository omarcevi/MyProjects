# First file for OMOBot

import discord 
from dotenv import load_dotenv
import os

# Loading the enviroment
load_dotenv('.env')

#Client
omobot = discord.Client()

# Code Stuff

@omobot.event
async def on_ready():
    """
    Printing on the general cahannel
    """
    general_channel = omobot.get_channel(785445213442932739)

    
    #await general_channel.send("<@689910515643842608>")
    #await general_channel.send("OMOBot Online")
    # 
    for guild in omobot.guilds:
        if guild.name == 'G O':
            break

    print(
        f'{omobot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')




# Run command
omobot.run(os.getenv('OMOBOT_TOKEN'))