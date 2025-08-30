from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_info, categories_list

app_name = CatalogConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('base/', categories_list, name='categories_list'),
    path('contacts/', contacts, name='contacts'),
    path('product_info/<int:product_id>/', product_info, name='product_info'),
]

