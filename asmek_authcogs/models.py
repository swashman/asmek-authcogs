"""
App Models
Create your models in here
"""

# Django
from django.db import models


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Basic access to this app"),)


class Link(models.Model):
    description = models.TextField(max_length=500)
    name = models.CharField(max_length=255, null=False, unique=True)
    url = models.CharField(max_length=255, null=False)
    thumbnail = models.CharField(max_length=255)

    class Meta:
        default_permissions = ()
        permissions = (("manage_links", "Can manage links"),)
