from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    menu_name = models.ForeignKey("Menu", models.CASCADE, related_name='items')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    url = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.parent and self.parent.menu_name != self.menu_name:
            raise ValidationError(
                "Выбранный родитель принадлежит другому меню. Нельзя смешивать меню."
            )

    def save(self, *args, **kwargs):
        if self.url:
            if not self.url.startswith('/'):
                self.url = '/' + self.url
            if not self.url.endswith('/'):
                self.url += '/'
        elif not self.url:
            self.url = '/' + slugify(self.title) + '/'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.menu_name.name}] {self.title}"
