# Generated by Django 5.1.2 on 2024-10-23 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['user__username']},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/profile_pictures/'),
        ),
    ]
