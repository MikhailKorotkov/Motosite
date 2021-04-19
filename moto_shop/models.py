from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image
from django.utils import timezone

User = get_user_model()


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


def get_models_for_count(*models_names):
    return [models.Count(model_name) for model_name in models_names]


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Мото-ботинки': 'motoclothes__count',
        'Мото-куртки': 'motoclothes__count',
        'Мото-перчатки': 'motoclothes__count',
        'Мото-штаны': 'motoclothes__count',
        'Мотошлемы': 'motohelmet__count',
    }

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('motohelmet', 'motoclothes')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Категория товара')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_app:category_detail', kwargs={'slug': self.slug})


class Brand(models.Model):

    name = models.CharField(max_length=255, verbose_name='Брэнд')
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=255, verbose_name='Страна производства')

    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Product(models.Model):

    MIN_RESOLUTION = (300, 300)
    MAX_RESOLUTION = (1000, 1000)

    COLORS = [
        ('black', 'black'),
        ('brown', 'brown'),
        ('grey', 'grey'),
        ('white', 'white'),
    ]

    class Meta:
        abstract = True

    brand = models.ForeignKey(Brand, verbose_name='Брэнд', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория товара', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="goods/%Y/%m/%d/", verbose_name='Изображение товара')
    description = models.TextField(verbose_name='Описание товара', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара')
    color = models.CharField(max_length=8, choices=COLORS, verbose_name='Цвет')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.height > max_height or img.width > max_width:
            raise Exception('Разрешение изображения больше максимального 1000х1000')
        if img.height < min_height or img.width < min_width:
            raise Exception('Разрешение изображения меньше минимального')
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__.__name__.lower()


class MotoHelmet(Product):
    TYPES = [
        ('Интегральный', 'Интегральный'),
        ('Модульный', 'Модульный'),
        ('Открытый', 'Открытый'),
    ]
    type = models.CharField(max_length=12, choices=TYPES, verbose_name='Тип шлема')

    class Meta:
        verbose_name = 'Мото-шлем'
        verbose_name_plural = 'Мото-шлемы'

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'shop_app:product_detail')


class MotoClothes(Product):
    MATERIALS = [
        ('Кожа', 'Кожа'),
        ('Текстиль', 'Текстиль'),
        ('Джинса', 'Джинса'),
    ]
    material = models.CharField(max_length=10, choices=MATERIALS, verbose_name='Материал')

    class Meta:
        verbose_name = 'Экипировка'
        verbose_name_plural = 'Мотоэкипировка (одежда)'

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'shop_app:product_detail')


class CartProduct(models.Model):

    X_SMALL = 'XS'
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    X_LARGE = 'XL'
    XL_LARGE = 'XXL'

    SIZES = [
        (X_SMALL, 'XS (35-36'),
        (SMALL, 'S (37-38)'),
        (MEDIUM, 'M (39-40)'),
        (LARGE, 'L (41-42)'),
        (X_LARGE, 'XL (43-44)'),
        (XL_LARGE, 'XXL (45-46)'),
    ]

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=3, choices=SIZES, default=MEDIUM)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена заказа')

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукция в корзине'

    def __str__(self):
        return f'Продукт {self.content_object.title} для Корзины'

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена заказа')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины покупателей'

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f'Покупатель {self.user.first_name, self.user.last_name}'


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE, related_name='related_orders')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1000, verbose_name='Адрес доставки', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(null=True, verbose_name='Комментарий к заказу', blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


# from moto_shop.models import MotoHelmet, CartProduct, Cart, Customer
# from django.contrib.auth import get_user_model
# User = get_user_model()
# u = User.objects.first()
# customer = Customer.objects.create(user=u, phone='12345', address='Moscow')
# helmet = MotoHelmet.objects.first()
# c = Cart.objects.create(owner=customer, final_price=0)
# cp = CartProduct.objects.create(content_object=helmet, user=customer, cart=c, total_price=helmet.price)
# c.products.add(cp)
