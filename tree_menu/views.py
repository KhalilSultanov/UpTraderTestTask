from django.shortcuts import render

from tree_menu.models import Menu


def index(request, menu=None, slug=None):
    all_menus = Menu.objects.values_list('name', flat=True)
    selected_menu = menu or request.GET.get('menu', 'main_menu')

    return render(request, 'index.html', {
        'available_menus': all_menus,
        'selected_menu': selected_menu,
    })
