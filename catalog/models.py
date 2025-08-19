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
    name = models.CharField(max_length=200, verbose_name='Наименование продукта')
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField()
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now_add=True, verbose_name='Дата последнего обновления')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name',]
