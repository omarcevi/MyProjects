from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db

class Welcome(Cog):
    def __init__(self, omobot):
        self.omobot = omobot

    @Cog.listener()
    async def on_ready(self):
        if not self.omobot.ready:
            self.omobot.cogs_ready.ready_up("greeting")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        await self.omobot.get_channel(789536925132259328).send(f"Welcome to **{member.guild.name}** {member.mention}! Head over to <#785445213442932739> to say hi!")
                                                                                                                                        
        try:
            await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")

        except Forbidden:
            pass

        await member.add_roles(member.guild.get_role(789540606102994974))

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
        await self.omobot.get_channel(789543364831477790).send(f"{member.display_name} has left {member.guild.name}.")

def setup(omobot):
	omobot.add_cog(Welcome(omobot))