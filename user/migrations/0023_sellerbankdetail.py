# Generated by Django 3.2.13 on 2022-07-06 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_selleraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerBankDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=30, verbose_name='Bank Name')),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('state', models.CharField(max_length=30, verbose_name='State')),
                ('branch', models.CharField(max_length=30, verbose_name='Branch')),
                ('business_type', models.CharField(max_length=30, verbose_name='Business type')),
                ('PAN', models.CharField(max_length=30, verbose_name='PAN')),
                ('address_proof', models.CharField(max_length=30, verbose_name='Address proof')),
                ('cancel_cheque', models.CharField(max_length=30, verbose_name='cancel cheque')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_bank_details', to='user.seller')),
            ],
            options={
                'verbose_name': 'seller_bankdetail',
                'verbose_name_plural': 'seller_bankdetail',
            },
        ),
    ]