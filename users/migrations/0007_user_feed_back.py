# Generated by Django 3.2.9 on 2024-01-23 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='feed_back',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
