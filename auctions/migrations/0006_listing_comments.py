# Generated by Django 3.1.5 on 2021-01-21 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='auctions.Comments'),
        ),
    ]
