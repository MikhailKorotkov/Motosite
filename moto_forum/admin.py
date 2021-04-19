from django.contrib import admin

from .models import *


class MotoForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'category', 'model', 'photo', 'is_published', 'time_create')
    list_display_links = ('id', 'model', 'brand', 'category')
    search_fields = ('model', 'content')
    list_editable = ('is_published', )
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('model', )}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Motorcycle, MotoForumAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
