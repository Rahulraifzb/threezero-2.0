# Generated by Django 3.2.7 on 2021-09-22 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_profile_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='theme',
            field=models.CharField(choices=[('light_theme', 'Light Theme'), ('dark_theme', 'Dark Theme')], max_length=15),
        ),
    ]
