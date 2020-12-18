from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed

from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown

class Fun(Cog):
    def __init__(self, omobot):
        self.omobot = omobot

    @command(name="merhaba", aliases= ['selam', 'sa', 'slm'], brief="Hello", hidden= True, pass_context= False)
    async def say_hello(self, ctx):
        await ctx.send(f"Merhaba, {ctx.author.mention}! beeb boop")

    @command(name='dice', brief="Dice", aliases= ['zar'])
    @cooldown(1, 60, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        """Throw a dice"""
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)] 
            
            await ctx.send("+".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

        else:
            await ctx.send("I can't roll that many dice. Please try a lower number.")

    @command(name="hug", aliases=["sarıl"], brief= "Hug")
    async def hug_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
	    await ctx.send(f"{ctx.author.display_name} hugged {member.mention} {reason}!")

    @command(name="echo", aliases= ['say'], brief="Echo")
    @cooldown(1, 15, BucketType.guild)
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @command(name="fact", brief="Animal fact")
    @cooldown(3, 60, BucketType.guild)
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} fact",
                                description=data["fact"],
                                colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are available for that animal.")

    @command(name= "meme")
    async def meme_post(self, ctx):
        pass



    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if "hmmm" in message.content:
                await message.channel.send(f"Ne düşünüyorsun acaba {message.author.mention}?! beeb boop")

    @Cog.listener()
    async def on_ready(self):
        #self.bot.stdout.send("Fun Cog ready!")
        if not self.omobot.ready:
            self.omobot.cogs_ready.ready_up("fun")



def setup(omobot):
    omobot.add_cog(Fun(omobot))
