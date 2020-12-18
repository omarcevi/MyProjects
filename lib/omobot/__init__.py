from datetime import datetime
from asyncio import sleep
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


from discord import Embed, Intents, File
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase 
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
                                  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions
from ..db import db


OWNER_IDS = [366292325078532106]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID =?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

        



class OMOBot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = False
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix= get_prefix, 
            owner_ids= OWNER_IDS,
            intents = Intents.all()
            )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

        print("Setup complete!")


    def run(self, version):
        self.VERSION = version

        print("Running setup...")
        self.setup()

        with open("./lib/omobot/token.0", 'r', encoding= 'utf=8') as tf:
            self.TOKEN = tf.read()
        print('OMOBot is running...')
        super().run(self.TOKEN, reconnect= True)
        
    async def process_commands(self, message):
        ctx = await self.get_context(message, cls= Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("I'm not ready to recieve commands yet please wait a few seconds.")

    """async def print_message(self):
        #await self.stdout.send('OMOBot timed notification!')
        pass"""

    async def love_reminder(self):
        await self.genchan.send("'Hepiniz seviliyorsunuz' -Omos")


    async def on_connect(self):
        print("OMOBot Online")         


    async def on_dissconnect(self):
        print("OMOBot Offline")
    

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong!")
        
        await self.stdout.send('An error occured.')
        raise 


    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc,  error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments is missing")

        elif isinstance(exc, CommandOnCooldown):
           await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} Try again in {exc.retry_after:,.2f} secs.")
            
        elif hasattr(exc, 'original'):
            #if isinstance(exc.original, HTTPException):
            #await ctx.send("Unable to send message.")
            
            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that.")

            else:
                raise exc.original

        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(785445213442932736)
            self.stdout = self.get_channel(788470589421649920)
            self.genchan = self.get_channel(785445213442932739)
            self.scheduler.add_job(self.love_reminder, CronTrigger(minute='0, 30', second='0'))
            self.scheduler.start()
           
           
           
            #embed = Embed(title= "Now Online!", description= "OMOBot is now Online and ready",
            #            colour=0xFF0000, timestamp=datetime.utcnow())

            
            #fields = [("Name", "Value", True),
            #          ("Another field", "This field is next to the other one.", True),
            #          ("A non-inline field", "This field will appear on it's own row.", False)]
            #for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            
            #embed.set_author(name="Omos", icon_url=self.guild.icon_url)
            #embed.set_footer(text="This is a footer!")
            #embed.set_thumbnail(url= self.guild.icon_url)
            #embed.set_image(url= self.guild.icon_url)
            #await channel.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)


            
            await self.stdout.send('OMOBot Online!')
            self.ready = True
            print('OMOBot Ready')

        else:
            print('OMOBot is back')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

    
    

omobot = OMOBot()


