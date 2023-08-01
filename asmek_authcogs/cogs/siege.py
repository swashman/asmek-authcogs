import logging

from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord.commands import SlashCommandGroup
from discord.ext import commands
from django.conf import settings

logger = logging.getLogger(__name__)


class Siege(commands.Cog):
    """
    All siege me!
    """

    def __init__(self, bot):
        self.bot = bot

    siege_commands = SlashCommandGroup(
        "siege",
        "SIEGE COLOURS!",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    
    @siege_commands.command(name="green", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("general.siege_control")
    async def green(self, ctx,*,msg=''):
        """
        All Clear
        """
        if len(msg) == 0:
            msg = 'SIEGE GREEN - Crab on!'
        siege_channel = self.bot.get_channel(int(settings.ASMEK_SIEGE_CHANNEL))
        await siege_channel.purge()
        await siege_channel.send(' @here '+ msg + '\nhttps://media.discordapp.net/attachments/478100446238474282/671250121178218496/Green_w_Excav.gif')
        return await ctx.respond("Siege status updated to GREEN", ephemeral=True)
    
    @siege_commands.command(name="amber", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("general.siege_control")
    async def amber(self, ctx,*,msg=''):
        """
        Ratting caps should dock, rorqs max tank
        """
        if len(msg) == 0:
            msg = 'SIEGE AMBER - Caps dock / Rorqs max tank!'
        siege_channel = self.bot.get_channel(int(settings.ASMEK_SIEGE_CHANNEL))
        await siege_channel.purge()
        await siege_channel.send('@here '+ msg + '\nhttps://media.discordapp.net/attachments/726469660916318218/829165923436331039/unknown.png')
        return await ctx.respond("Siege status updated to AMBER", ephemeral=True)
    
    @siege_commands.command(name="red", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("general.siege_control")
    async def red(self, ctx):
        """
        Everyone should dock up
        """
        if len(msg) == 0:
            msg = 'SIEGE RED - Delve is dangerous!'
        siege_channel = self.bot.get_channel(int(settings.ASMEK_SIEGE_CHANNEL))
        await siege_channel.purge()
        await siege_channel.send('@here '+ msg + '\nhttps://media.discordapp.net/attachments/478100446238474282/671250121345728542/Red_Final.gif')
        return await ctx.respond("Siege status updated to RED", ephemeral=True)
    
    @siege_commands.command(name="cta", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("general.siege_control")
    async def red(self, ctx):
        """
        CTA dock up
        """
        siege_channel = self.bot.get_channel(int(settings.ASMEK_SIEGE_CHANNEL))
        await siege_channel.purge()
        await siege_channel.send('@here SIEGE RED - CTA IS MUST ATTEND! \nhttps://media.discordapp.net/attachments/478100446238474282/671250121345728542/Red_Final.gif')
        return await ctx.respond("Siege status updated to RED/CTA", ephemeral=True)
    
def setup(bot):
    bot.add_cog(Siege(bot))
