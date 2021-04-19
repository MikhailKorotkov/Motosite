from django.db.models import Count

from .models import *

menu = [{'title': 'О форуме', 'url_name': 'about'},
        {'title': 'Добавить свой байк', 'url_name': 'add_bike'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Магазин', 'url_name': 'shop_app:shop'},
        ]


class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('motorcycle'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
