import logging

from aadiscordbot.cogs.utils.decorators import has_any_perm, sender_has_perm
from discord import (
    AutocompleteContext,
    CategoryChannel,
    Embed,
    Role,
    TextChannel,
    option,
)
from discord.colour import Color
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

from asmek_authcogs.models import Link


class Links(commands.Cog):
    """
    Helpful links
    """

    def __init__(self, bot):
        self.bot = bot

    links_commands = SlashCommandGroup(
        "links",
        "Useful links to sites or programs",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )

    @links_commands.command(name="list", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def list(self, ctx):
        """
        list all current links
        """
        try:
            # has_any_perm(ctx.author.id, ["link.manage_links"])
            embed = Embed()
            embed.title = "All the links!!"
            embed.description = f"A list of all links currently stored by the auth bot!"
            await ctx.defer(ephemeral=False)
            links = Link.objects.all()
            if links.count() > 0:
                for i in links:
                    embed.add_field(
                        name=f"{i.name}.: {i.description}", value=i.url, inline=False
                    )
            else:
                embed.description = f"No Links added!"

            await ctx.respond(embed=embed, ephemeral=False)
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)

    async def search_links(ctx: AutocompleteContext):
        """Returns a list of links that begin with the characters entered so far."""
        return list(
            Link.objects.filter(name__icontains=ctx.value).values_list(
                "name", flat=True
            )[:10]
        )

    @commands.slash_command(
        pass_context=True,
        description="Display a link",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    @option("name", description="Search for a Link!", autocomplete=search_links)
    async def link(self, ctx, name: str):
        """
        Display a link
        """
        try:
            link1 = Link.objects.get(name=name)
            embed = Embed(title=link1.name)
            if link1.thumbnail:
                embed.set_thumbnail(url=link1.thumbnail)
            embed.colour = Color.blurple()

            embed.description = link1.description

            embed.url = link1.url

            return await ctx.respond(embed=embed)
        except Link.DoesNotExist:
            return await ctx.respond(
                f"Link **{name}** does not exist in our Auth system"
            )
        except ObjectDoesNotExist:
            return await ctx.respond(f"**{name}** is does not exist")


def setup(bot):
    bot.add_cog(Links(bot))
