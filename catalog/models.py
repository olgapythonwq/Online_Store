from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование категории')
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name',]


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'Архив'),
    ]

    name = models.CharField(max_length=200, verbose_name='Наименование продукта')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус публикации')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # автоматически ссылается на кастомного пользователя
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name',]
        permissions = [("can_unpublish_product", "Может отменять публикацию продукта"),]
