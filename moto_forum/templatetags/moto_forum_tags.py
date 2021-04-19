from django import template
from moto_forum.models import *


register = template.Library()


@register.simple_tag()
def get_menu():
    return menu


@register.simple_tag()
def get_category():
    cats = Category.objects.all()
    return cats
