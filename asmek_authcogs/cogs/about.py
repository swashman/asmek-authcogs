import logging

from aadiscordbot.app_settings import get_site_url
from discord.colour import Color
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands
from django.conf import settings

logger = logging.getLogger(__name__)


class About(commands.Cog):
    """
    All about me!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        pass_context=True,
        description="About this Discord Server",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def about(self, ctx):
        """
        All about a server
        """
        embed = Embed(title="ASMEK AuthBot: The Omnisiah")

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.color = Color.blue()
        embed.description = "Some spooky description"
        embed.set_footer(
            text="Developed by Aaron Kable, forked for Astrum Mechanica by Swashman Acami"
        )

        members = ctx.guild.member_count
        embed.add_field(name="Unwilling Monitorees:", value=members, inline=True)

        embed.add_field(name="Auth Link", value=get_site_url(), inline=False)

        return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(About(bot))
