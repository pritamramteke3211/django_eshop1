# Generated by Django 3.2.7 on 2021-10-09 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_order_ordered_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(default=''),
        ),
    ]
