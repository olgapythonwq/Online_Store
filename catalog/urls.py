from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductsByCategoryView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='catalog'),  # Главная страница
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Детали товара
    path('category/<int:pk>/', ProductsByCategoryView.as_view(), name='products_by_category'),  # Товары по категории
]

