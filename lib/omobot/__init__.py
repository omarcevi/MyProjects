from discord import Intents
from discord import Embed
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase 

PREFIX = '-'
OWNER_IDS = [366292325078532106]

class OMOBot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = False
        self.scheduler = AsyncIOScheduler()
        
        super().__init__(
            command_prefix= PREFIX, 
            owner_ids= OWNER_IDS,
            intents = Intents.all()
            )

    def run(self, version):
        self.VERSION = version
        
        with open("./lib/omobot/token.0", 'r', encoding= 'utf=8') as tf:
            self.TOKEN = tf.read()
        print('OMOBot is running...')
        super().run(self.TOKEN, reconnect= True)
        

    async def on_connect(self):
        print("OMOBot Online")         

    async def on_dissconnect(self):
        print("OMOBot Offline")
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(785445213442932736)
            print('OMOBot Ready')
        
            channel = self.get_channel(788470589421649920)

            await channel.send('OMOBot Online!')

            embed = Embed(title= "Now Online!", description= "OMOBot is now Online and ready",
                        colour=0xFF0000, timestamp=datetime.utcnow())

            
            fields = [("Name", "Value", True),
                      ("Another field", "This field is next to the other one.", True),
                      ("A non-inline field", "This field will appear on it's own row.", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            embed.set_author(name="Omos", icon_url=self.guild.icon_url)
            embed.set_footer(text="This is a footer!")
            embed.set_thumbnail(url= self.guild.icon_url)
            embed.set_image(url= self.guild.icon_url)
            await channel.send(embed=embed)


        else:
            print('OMOBot is back')

    async def on_message(self, message):
        pass

omobot = OMOBot()


