# Generated by Django 3.2.13 on 2022-07-01 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
