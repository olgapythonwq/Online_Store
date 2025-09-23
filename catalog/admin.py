from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'owner',)
    list_filter = ('category', )
    search_fields = ('name', 'description',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset
