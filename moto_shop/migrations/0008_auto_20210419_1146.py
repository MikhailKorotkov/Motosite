# Generated by Django 3.1.7 on 2021-04-19 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moto_shop', '0007_auto_20210416_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motoclothes',
            name='size',
        ),
        migrations.RemoveField(
            model_name='motohelmet',
            name='size',
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='size',
            field=models.CharField(choices=[('XS', 'XS (35-36'), ('S', 'S (37-38)'), ('M', 'M (39-40)'), ('L', 'L (41-42)'), ('XL', 'XL (43-44)'), ('XXL', 'XXL (45-46)')], default='M', max_length=3),
        ),
    ]
