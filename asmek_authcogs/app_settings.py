"""App Settings"""

# Django
from django.apps import apps
from django.conf import settings

# put your app settings here


EXAMPLE_SETTING_ONE = getattr(settings, "EXAMPLE_SETTING_ONE", None)


def fittings_installed() -> bool:
    """
    Check if fittings is installed
    :return: bool
    """

    return apps.is_installed("fittings")
