# Generated by Django 3.2.13 on 2022-07-05 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20220705_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_address', to=settings.AUTH_USER_MODEL),
        ),
    ]
