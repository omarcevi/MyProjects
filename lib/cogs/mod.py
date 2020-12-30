from asyncio import sleep
from typing import Optional
from datetime import datetime, timedelta

from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

from ..db import db

class Mod(Cog):
    def __init__(self, omobot):
        self.omobot = omobot

    # Kick command
    @command(name= "kick")
    @has_permissions(kick_members= True)
    @bot_has_permissions(kick_members= True)
    async def kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send("One or more required arguments is missing")

        else:
            for target in targets:
                if (ctx.guild.me.top_role.position > target.top_role.position
                    and not target.guild_permissions.administrator):
                    await targets.kick(reason=reason)

                    embed = Embed(title="Member kicked", 
                                colour= 0xDD2222, 
                                timestamp=datetime.utcnow())

                    embed.set_thumbnail(url= target.avatar_url)

                    fields = [("Member", f"{target.name} aka {target.display_name}", False),
                              ("Action done by", ctx.author.display_name, False),
                              ("Reason", reason, False)]

                    for name, value, inline in fields: embed.add_field(name= name, value=value, inline= inline)

                    await self.log_channel.send(embed= embed)

                await ctx.send(f"{target.display_name} could not be kicked")

            await ctx.send("Action complete.")
    
    @kick_members.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure): await ctx.send("Insufficient permissions to preform that tast.")
    

    # Ban command
    @command(name= "ban")
    @has_permissions(ban_members= True)
    @bot_has_permissions(ban_members= True)
    async def ban_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided"):
        if not len(targets):
            await ctx.send("One or more required arguments is missing")

        else:
            for target in targets:
                if (ctx.guild.me.top_role.position > target.top_role.position
                    and not target.guild_permissions.administrator):
                    await targets.ban(reason=reason)

                    embed = Embed(title="Member banned", 
                                  colour= 0xDD2222, 
                                  timestamp=datetime.utcnow())

                    embed.set_thumbnail(url= target.avatar_url)

                    fields = [("Member", f"{target.name} aka {target.display_name}", False),
                              ("Action done by", ctx.author.display_name, False),
                              ("Reason", reason, False)]

                    for name, value, inline in fields: embed.add_field(name= name, value=value, inline= inline)

                    await self.log_channel.send(embed= embed)

                await ctx.send(f"{target.display_name} could not be banned")

            await ctx.send("Action complete.")
    
    @ban_members.error
    async def ban_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure): await ctx.send("Insufficient permissions to preform that tast.")

    # Message purge command 
    @command(name="clear", aliases=["purge"])
    @has_permissions(manage_messages= True)
    @bot_has_permissions(manage_messages= True)
    async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets
        if 0 < limit <= 100:
            with ctx.channer.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit= limit, after= datetime.utcnow()-timedelta(days=14), 
                                                  check= _check)

                await ctx.send(f"Deleted {len(deleted):,} messages", delete_after= 5)

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")


    # Mute command
    @command(name='mute')
    @has_permissions(manage_roles= True, manage_guild= True)
    @bot_has_permissions(manage_roles= True)
    async def mute_members(self, ctx, targets: Greedy[Member], hours: Optional[int], *, 
                           reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments is missing")

        else:
            unmutes = []

            for target in targets:
                if not self.mute_role in target.roles:
                    if ctx.guild.me.top_role.position > target.top_role.position:
                        role_ids = ",".join([str(r.id) for r in target.roles])
                        end_time = datetime.utcnow() + timedelta(seconds=hours) if hours else None

                        db.execute("INSERT INTO mutes VALUES (?,?,?)", 
                                   target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())
                        
                        await target.edit(roles= [self.mute_role])

                        embed = Embed(title="Member muted.", 
                                colour= 0xDD2222, 
                                timestamp=datetime.utcnow())

                        embed.set_thumbnail(url= target.avatar_url)

                        fields = [("Member", f"{target.name} aka {target.display_name}", False),
                                  ("Action done by", ctx.author.display_name, False),
                                  ("Duration", f"{hours:,} hour(s)" if hours else "Indefinite", False),
                                  ("Reason", reason, False)]

                        for name, value, inline in fields: embed.add_field(name= name, value=value, inline= inline)

                        await self.log_channel.send(embed= embed)

                        if hours:
                            unmutes.append(target)
                    
                    else:
                        await ctx.send(f"{target.display_name} could not be muted.")
                
                else:
                    await ctx.send("f{target.display_name} is already muted.") 
            await ctx.send("Action complete.")

            if len(unmutes):
                await sleep(hours)
                await self.unmutes(ctx, targets)

    @mute_members.error
    async def mute_members_errors(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform that task.")

    async def unmute(self, ctx, targets, *, reason = "Mute time expired"):
        for target in targets:
            if self.mute_role in targets.roles:
                role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
                roles = [ctx.guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]

                db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)

                await target.edit(roles=roles)

                embed = Embed(title="Member unmuted.", 
                              colour= 0xDD2222, 
                              timestamp=datetime.utcnow())

                embed.set_thumbnail(url= target.avatar_url)

                fields = [("Member", target.display_name, False),
                          ("Reason", reason, False)]

                for name, value, inline in fields: 
                    embed.add_field(name= name, value=value, inline= inline)

                await self.log_channel.send(embed= embed)

    @command(name= "unmute")
    @has_permissions(manage_roles= True, manage_guild= True)
    @bot_has_permissions(manage_roles= True)
    async def unmute_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments is missing")

        else:
            await self.unmute(ctx, targets, reason=reason)

    @Cog.listener()
    async def on_ready(self):
        if not self.omobot.ready:
            self.log_channel = self.omobot.get_channel(790558270603395072)
            #self.mute_role = self.omobot.guild.get_role() # you need to put the mute role ID here
            self.omobot.cogs_ready.ready_up("mod")

    
def setup(omobot):
    omobot.add_cog(Mod(omobot))