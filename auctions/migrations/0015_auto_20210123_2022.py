# Generated by Django 3.1.5 on 2021-01-23 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20210122_2229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'get_latest_by': 'bid'},
        ),
    ]
