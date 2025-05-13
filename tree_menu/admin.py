from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    list_display = ('title', 'menu_name', 'parent', 'url', 'order')
    list_filter = ('menu_name',)
    search_fields = ('title', 'url')
    ordering = ('menu_name', 'parent__id', 'order')

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)
