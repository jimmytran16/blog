# Generated by Django 3.0.6 on 2020-06-16 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_auto_20200612_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, default=None, upload_to='profile_pic/'),
        ),
    ]