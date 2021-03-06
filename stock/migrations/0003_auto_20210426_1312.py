# Generated by Django 3.2 on 2021-04-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20210426_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='latest_price',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='market_cap',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pe_ratio',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.AlterField(
            model_name='stock',
            name='volume',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='stock',
            name='w52_high',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='stock',
            name='w52_low',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ytd_change',
            field=models.CharField(max_length=6),
        ),
    ]
