"""App Settings"""

# Django
from django.conf import settings

# put your app settings here


EXAMPLE_SETTING_ONE = getattr(settings, "EXAMPLE_SETTING_ONE", None)

#default cogs
ASMEK_AUTH_COGS = getattr(settings, 'DISCORD_BOT_COGS', [
    "asmek_authcogs.cogs.about",
]
)