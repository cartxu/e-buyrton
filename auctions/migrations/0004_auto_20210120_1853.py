# Generated by Django 3.1.5 on 2021-01-20 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210120_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='startbid',
            field=models.IntegerField(),
        ),
    ]