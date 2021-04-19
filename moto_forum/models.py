from django.db import models
from django.urls import reverse


class Motorcycle(models.Model):

    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name='Марка мотоцикла')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория мотоцикла')
    model = models.CharField(max_length=255, verbose_name='Модель')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Описание мотоцикла')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фотография')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Публикации')

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Мотоцикл пользователя'
        verbose_name_plural = 'Мотоциклы Пользователей'
        ordering = ['is_published', 'time_create']


class Brand(models.Model):

    name = models.CharField(max_length=255, verbose_name='Марка мотоцикла')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_id': self.pk})

    class Meta:
        verbose_name = 'Марка мотоцикла'
        verbose_name_plural = 'Марки мотоциклов'
        ordering = ['id']


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URl')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория мотоцикла'
        verbose_name_plural = 'Категории мотоциклов'
        ordering = ['id']
