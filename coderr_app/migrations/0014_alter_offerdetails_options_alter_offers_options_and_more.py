# Generated by Django 5.1.2 on 2024-11-05 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0013_alter_userprofile_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offerdetails',
            options={'ordering': ['title'], 'verbose_name_plural': 'Offerdetails'},
        ),
        migrations.AlterModelOptions(
            name='offers',
            options={'ordering': ['title'], 'verbose_name_plural': 'Offers'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['title'], 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='reviews',
            options={'ordering': ['rating'], 'verbose_name_plural': 'Reviews'},
        ),
    ]