from django.contrib import admin
from django.urls import path, re_path

from tree_menu.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('<str:menu>/<path:slug>/', index, name='menu_item'),
]
