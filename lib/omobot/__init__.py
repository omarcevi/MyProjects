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
        super().__init__(command_prefix= PREFIX, owner_ids= OWNER_IDS)

    def run(self, version):
        self.VERSION = version
        
        with open("./lib/omobot/token", 'r', encoding= 'utf=8') as tf:
            self.TOKEN = tf.read()
        

    async def on_connect(self):
        print("OMOBot Online")         

    async def on_dissconnect(self):
        print("OMOBot Offline")
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(785445213442932736)
            print('OMOBot Ready')
        else:
            print('OMOBot is back')

    async def on_message(self, message):
        pass

omobot = OMOBot()


