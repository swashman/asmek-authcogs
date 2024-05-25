# Generated by Django 4.0.10 on 2024-01-05 04:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("asmek_authcogs", "0004_authcogs_delete_general"),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupWelcome",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("enabled", models.BooleanField(default=True)),
                ("channel", models.BigIntegerField()),
                ("thumbnail", models.CharField(max_length=255)),
                (
                    "group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="auth.group"
                    ),
                ),
            ],
            options={
                "verbose_name": "Group Welcome Message",
                "verbose_name_plural": "Group Welcome Messages",
            },
        ),
    ]
