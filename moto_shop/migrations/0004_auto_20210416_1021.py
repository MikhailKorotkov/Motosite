# Generated by Django 3.1.7 on 2021-04-16 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moto_shop', '0003_auto_20210416_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moto_shop.customer', verbose_name='Владелец'),
        ),
    ]
