# Generated by Django 3.1.5 on 2021-01-22 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
