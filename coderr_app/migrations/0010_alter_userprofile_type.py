# Generated by Django 5.1.2 on 2024-10-25 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0009_alter_offerdetails_offer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('customer', 'Customer'), ('business', 'Business')], max_length=25),
        ),
    ]
