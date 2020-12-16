from discord.ext.commands import Cog

class Fun(Cog):
    def __init__(self, omobot):
        self.omobot = omobot

    @Cog.listener()
    async def on_ready(self):
        #self.bot.stdout.send("Fun Cog ready!")
        if not self.omobot.ready:
            self.omobot.cogs_ready.ready_up("fun")

    

def setup(omobot):
    omobot.add_cog(Fun(omobot))
