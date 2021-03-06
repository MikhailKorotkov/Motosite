from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from .models import *


class CategoryDetailMixin(SingleObjectMixin):

    CATEGORY_SLUG_PRODUCT_MODEL = {
        'moto-perchatki': MotoClothes,
        'moto-shtany': MotoClothes,
        'moto-botinki': MotoClothes,
        'moto-kurtki': MotoClothes,
        'motoshlemy': MotoHelmet,
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG_PRODUCT_MODEL[self.get_object().slug]
            category = kwargs.get('object')
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.filter(category=category.pk)
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context



class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
