from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductsByCategoryView, ContactsView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView, UnpublishProductView

app_name = CatalogConfig.name


urlpatterns = [
    path('catalog/', ProductListView.as_view(), name='product_list'),  # Главная страница каталога (список всех товаров)
    path('contacts/', ContactsView.as_view(), name='contacts'),  # Контакты
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Детали товара
    path('category/<int:pk>/', ProductsByCategoryView.as_view(), name='products_by_category'),  # Товары по категории
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('product/<int:pk>/unpublish/', UnpublishProductView.as_view(), name='product_unpublish'),
]
