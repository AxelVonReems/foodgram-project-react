from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Имя тега',
        help_text='Укажите имя тега',
    )
    color = models.CharField(
        max_length=7,
        default='#029bc2',
        unique=True,
        verbose_name='Цвет тега',
        help_text='Укажите цвет тега',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Название',
        help_text='Введите название тега',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
