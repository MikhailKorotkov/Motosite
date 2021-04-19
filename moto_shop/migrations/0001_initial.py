# Generated by Django 3.1.7 on 2021-04-14 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Брэнд')),
                ('slug', models.SlugField(unique=True)),
                ('country', models.CharField(max_length=255, unique=True, verbose_name='Страна производства')),
            ],
            options={
                'verbose_name': 'Брэнд',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая цена заказа')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины покупателей',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Категория товара')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категория товаров',
                'verbose_name_plural': 'Категории товаров',
            },
        ),
        migrations.CreateModel(
            name='MotoHelmet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование товара')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='goods/%Y/%m/%d/', verbose_name='Изображение товара')),
                ('description', models.TextField(null=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена товара')),
                ('size', models.CharField(blank=True, choices=[('XS', 'XS (35-36'), ('S', 'S (37-38)'), ('M', 'M (39-40)'), ('L', 'L (41-42)'), ('XL', 'XL (43-44)'), ('XXL', 'XXL (45-46)')], max_length=3)),
                ('color', models.CharField(choices=[('black', 'black'), ('brown', 'brown'), ('grey', 'grey'), ('white', 'white')], max_length=8, verbose_name='Цвет')),
                ('type', models.CharField(choices=[('Интегральный', 'Интегральный'), ('Модульный', 'Модульный'), ('Открытый', 'Открытый')], max_length=12, verbose_name='Тип шлема')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moto_shop.brand', verbose_name='Брэнд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moto_shop.category', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Мото-шлем',
                'verbose_name_plural': 'Мото-шлемы',
            },
        ),
        migrations.CreateModel(
            name='MotoClothes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование товара')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='goods/%Y/%m/%d/', verbose_name='Изображение товара')),
                ('description', models.TextField(null=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена товара')),
                ('size', models.CharField(blank=True, choices=[('XS', 'XS (35-36'), ('S', 'S (37-38)'), ('M', 'M (39-40)'), ('L', 'L (41-42)'), ('XL', 'XL (43-44)'), ('XXL', 'XXL (45-46)')], max_length=3)),
                ('color', models.CharField(choices=[('black', 'black'), ('brown', 'brown'), ('grey', 'grey'), ('white', 'white')], max_length=8, verbose_name='Цвет')),
                ('material', models.CharField(choices=[('Кожа', 'Кожа'), ('Текстиль', 'Текстиль'), ('Джинса', 'Джинса')], max_length=10, verbose_name='Материал')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moto_shop.brand', verbose_name='Брэнд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moto_shop.category', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Экипировка',
                'verbose_name_plural': 'Мотоэкипировка (одежда)',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес доставки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('qty', models.PositiveIntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая цена заказа')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='moto_shop.cart', verbose_name='Корзина')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moto_shop.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Продукт в корзине',
                'verbose_name_plural': 'Продукция в корзине',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moto_shop.customer', verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='moto_shop.CartProduct'),
        ),
    ]
