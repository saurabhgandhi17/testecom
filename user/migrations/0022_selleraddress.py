# Generated by Django 3.2.13 on 2022-07-06 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_alter_seller_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=255, verbose_name='Address 1')),
                ('address_line2', models.CharField(max_length=255, verbose_name='Address 2')),
                ('city', models.CharField(default='', max_length=255, verbose_name='city')),
                ('state', models.CharField(default='', max_length=255, verbose_name='state')),
                ('pincode', models.CharField(max_length=30, verbose_name='Area pincode')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_address', to='user.seller')),
            ],
            options={
                'verbose_name': 'seller_address',
                'verbose_name_plural': 'seller_address',
            },
        ),
    ]
