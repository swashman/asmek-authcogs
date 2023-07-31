import logging

from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord import Embed
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands
from django.conf import settings

logger = logging.getLogger(__name__)

from asmek_authcogs.models import General


class Siege(commands.Cog):
    """
    Siege Colours
    """

    def __init__(self, bot):
        self.bot = bot

    siege_commands = SlashCommandGroup(
        "siege",
        "Siege Colours",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )

    @siege_commands.command(name="GREEN", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("general.siege_control")
    async def green(self, ctx):
        """
        siege control
        """
        embed = Embed(title="SIEGE GREEN")
        embed.description = "SIEGE GREEN"

        return await ctx.respond(embed=embed)
    
def setup(bot):
    bot.add_cog(Siege(bot))
