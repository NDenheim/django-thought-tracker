# Generated by Django 5.1.7 on 2025-03-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='Default.png', null=True, upload_to='media/'),
        ),
    ]
