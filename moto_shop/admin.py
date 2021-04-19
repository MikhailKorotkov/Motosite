from django.forms import ModelChoiceField
from django.contrib import admin
from .models import *
from .forms import ProductAdminForm


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


class BrandAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'country')
    prepopulated_fields = {'slug': ('name', )}
    list_filter = ('country', )


class MotoHelmetAdmin(admin.ModelAdmin):

    form = ProductAdminForm

    list_display = ('category', 'brand', 'title', 'image', 'price', 'type')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', )
    list_filter = ('type', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='motoshlemy'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MotoClothesAdmin(admin.ModelAdmin):

    form = ProductAdminForm

    list_display = ('category', 'brand', 'title', 'image', 'price', 'material')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', )
    list_filter = ('material', 'category')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.exclude(slug='motoshlemy'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(MotoHelmet, MotoHelmetAdmin)
admin.site.register(MotoClothes, MotoClothesAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
