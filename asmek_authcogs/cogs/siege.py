import logging

from aadiscordbot.cogs.utils.decorators import has_any_perm, sender_has_perm
from discord import File, AutocompleteContext, Embed, InputTextStyle, Interaction, option
from discord.colour import Color
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands
from discord.ui import InputText, Modal
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

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
    @sender_has_perm("link.manage_links")
    async def green(self, ctx):
        """
        siege green
        """
        with open('my_image.png', 'rb') as f:
            pic = File(f)
        return await ctx.respond(file=pic)
    
def setup(bot):
    bot.add_cog(Siege(bot))
