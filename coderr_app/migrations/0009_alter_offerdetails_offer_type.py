# Generated by Django 5.1.2 on 2024-10-25 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_app', '0008_remove_offers_min_delivery_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetails',
            name='offer_type',
            field=models.CharField(choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=50),
        ),
    ]