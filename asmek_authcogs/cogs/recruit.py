import logging
import re

import discord
from discord.ext import commands
from django.conf import settings

logger = logging.getLogger(__name__)


class Recruit(commands.Cog):
    """
    ASEMK Recruitment
    """

    def __init__(self, bot):
        self.bot = bot


# Validation Checks - These values must be defined in server settings
if not hasattr(settings, "ASMEK_RECRUIT_CHANNEL"):
    raise ValueError("ASMEK_RECRUIT_CHANNEL is not defined.")
if not hasattr(settings, "ASMEK_CORP_ROLEID"):
    raise ValueError("ASMEK_CORP_ROLEID is not defined.")
if not hasattr(settings, "ASMEK_RECRUITER_ROLEID"):
    raise ValueError("ASMEK_RECRUITER_ROLEID is not defined.")
if not hasattr(settings, "ASMEK_RECRUIT_MSG_1"):
    raise ValueError("ASMEK_RECRUIT_MSG_1 is not defined.")


# Returns the count of how many ASMEK_RECRUIT_MSG_# settings variables are available, assuming ASMEK_RECRUIT_MSG_1 will always exist
async def msgcount():
    i = 0
    while hasattr(settings, "ASMEK_RECRUIT_MSG_" + str((i + 1))):
        i += 1
    return i


# Returns whether the reaction clicked on by a user in recruitment is valid
async def valid_reaction(self, reaction, user):
    if reaction.message.channel.name == "RCT-" + user.name:
        if reaction.emoji == "\N{White Heavy Check Mark}":
            async for user in reaction.users():
                if user.id == self.bot.user.id:
                    return True
    return False


class Recruit(commands.Cog):
    """
    Creates private thread for recruits.
    """

    def __init__(self, bot):
        self.bot = bot

    # Listener for added reactions to see whether additional recruitment messages should be sent
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if await valid_reaction(self, reaction, user):
            msg = re.sub("<.*?>", "{}", reaction.message.content)
            msgnum = await msgcount()
            for x in range(1, msgnum):
                if msg == eval("settings.ASMEK_RECRUIT_MSG_{}".format(x)):
                    await reaction.message.clear_reactions()
                    messageinfo = await self.bot.get_channel(
                        reaction.message.channel.id
                    ).send(eval("settings.ASMEK_RECRUIT_MSG_{}".format(x + 1)))
                    if x < (msgnum - 1):
                        await messageinfo.add_reaction("\N{White Heavy Check Mark}")
                    return

    # Checks to see whether a thread exists for the given user and returns the thread ID if so
    async def thread_exist(self, member):
        chan = self.bot.get_channel(int(settings.ASMEK_RECRUIT_CHANNEL))
        for thread in chan.threads:
            if thread.name == "RCT-" + member.name:
                return thread.id
        return 0

    # Checks whether the user who invoked the command is authorized to do so given their roles
    async def caller_authorized(self, ctx):
        for userrole in ctx.author.roles:
            for id in settings.ASMEK_RECRUITER_ROLEID:
                if userrole.id == id:
                    return True
        return False

    # Checks to see if target user is already in asmek
    async def target_in_corp(self, member):
        for userrole in member.roles:
            for id in settings.ASMEK_CORP_ROLEID:
                if userrole.id == id:
                    return True
        return False

    # Runs through the various check methods to determine whether a given recruitment invocation is valid
    async def can_recruit(self, ctx, member):
        threadid = await self.thread_exist(member)
        if not await self.caller_authorized(ctx):
            return True
        elif await self.target_in_corp(member):
            await ctx.respond(
                "That user is already in the corporation.", ephemeral=True
            )
            return False
        elif threadid > 0:
            await ctx.respond(
                "That user already has an active recruitment thread: <#"
                + str(threadid)
                + ">",
                ephemeral=True,
            )
            return False
        return True

    # Sets up right-click user command for EVE recruitment
    @commands.user_command(
        name="Recruit for EVE", guild_ids=[int(settings.DISCORD_GUILD_ID)]
    )
    async def recruit_user(self, ctx, member: discord.Member):
        if await self.can_recruit(ctx, member):
            channel = self.bot.get_channel(int(settings.ASMEK_RECRUIT_CHANNEL))
            threadname = "RCT-" + member.name
            recruitrole = ctx.guild.get_role(int(settings.ASMEK_RECRUITER_ROLEID))
            messagetext = settings.ASMEK_RECRUIT_MSG_1.format(
                member.mention, recruitrole.mention
            )
            threadinfo = await channel.create_thread(
                name=threadname,
                auto_archive_duration=10080,
                type=discord.ChannelType.private_thread,
            )
            messageinfo = await self.bot.get_channel(threadinfo.id).send(messagetext)
            if await msgcount() > 1:
                await messageinfo.add_reaction("\N{White Heavy Check Mark}")
            if int(settings.ASMEK_RECRUITER_ROLEID) in ctx.author.roles:
                await ctx.respond(
                    "Recruitment thread created: " + threadinfo.mention, ephemeral=True
                )
            else:
                await ctx.respond("Recruitment thread created!", ephemeral=True)


def setup(bot):
    bot.add_cog(Recruit(bot))
