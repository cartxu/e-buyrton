# Generated by Django 3.1.5 on 2021-01-19 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='owner',
            new_name='user',
        ),
    ]