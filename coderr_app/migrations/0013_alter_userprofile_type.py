# Generated by Django 5.1.2 on 2024-11-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0012_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('customer', 'Customer'), ('business', 'Business'), ('staff', 'Staff')], max_length=25),
        ),
    ]
