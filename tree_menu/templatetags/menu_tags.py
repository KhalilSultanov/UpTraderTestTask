from django import template
from tree_menu.models import MenuItem
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.inclusion_tag('draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    items = list(MenuItem.objects.select_related('parent', 'menu_name')
                 .filter(menu_name__name=menu_name)
                 .order_by('order'))

    def resolve_url(item):
        try:
            url = reverse(item.url)
        except NoReverseMatch:
            url = item.url

        prefix = f"/{item.menu_name.name.strip('/')}"
        return f"{prefix}{url if url.startswith('/') else '/' + url}"

    resolved_urls = {item.id: resolve_url(item) for item in items}

    # Строим дерево
    tree = {}
    for item in items:
        item.temp_children = []
        tree[item.id] = item

    root_items = []

    for item in items:
        item.resolved_url = resolved_urls[item.id]
        item.is_active = item.resolved_url == current_path
        item.is_open = False

        if item.parent_id:
            tree[item.parent_id].temp_children.append(item)
        else:
            root_items.append(item)

    # Проставляем is_open по активной цепочке
    def mark_active_branch(item):
        item.is_open = True
        if item.parent_id:
            mark_active_branch(tree[item.parent_id])

    for item in items:
        if item.is_active:
            mark_active_branch(item)

    return {'menu_items': root_items}
