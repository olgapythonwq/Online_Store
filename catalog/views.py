from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from catalog.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'catalog.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductsByCategoryView(ListView):
    model = Product  # Модель, которую мы хотим отображать (список товаров)
    template_name = 'catalog.html'  # Показываем те же карточки товаров = тот же шаблон

    def get_queryset(self):  # фильтруем товары по ID категории
        return Product.objects.filter(category_id=self.kwargs['pk'])  # self.kwargs['pk'] — это pk, который передаётся из URL (например, /category/3/)

    def get_context_data(self, **kwargs):  # Расширяем контекст: добавим выбранную категорию
        context = super().get_context_data(**kwargs)  # Получаем стандартный контекст
        category = Category.objects.get(pk=self.kwargs['pk'])  # Получаем объект категории
        context['selected_category'] = category  # Добавляем в контекст - Это позволяет использовать в шаблоне {{ selected_category.name }}
        return context


class ContactsView(View):
    template_name = 'contacts.html'

    def get(self, request):  # Отображаем форму
        return render(request, self.template_name)

    def post(self, request):   # Обработка данных формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"[Контактная форма] Имя: {name}, Телефон: {phone}, Сообщение: {message}")  # Потом лучше заменить на logging
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

# def home(request):
#     # Получаем 5 последних продуктов по дате создания
#     # latest_products = Product.objects.all().order_by('-created_at')[:5]
#     #
#     # # Выводим каждый продукт в консоль (для отладки)
#     # for product in latest_products:
#     #     print(product)
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'catalog.html', context)


# def contacts(request):
#     if request.method == 'POST':
#         # Получение данных из формы
#         name = request.POST.get('name')
#         message = request.POST.get('message')
#         # Обработка данных (например, сохранение в БД, отправка email и т. д.)
#         # Здесь мы просто возвращаем простой ответ
#         return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
#
#     return render(request, 'contacts.html')


# def product_info(request, product_id):
#     product = Product.objects.get(id=product_id)
#     context = {'product': product}
#     return render(request, 'product_detail.html', context)

# def products_list(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'catalog.html', context)

# def categories_list(request):
#     categories = Category.objects.all()
#     context = { 'categories': categories}
#     return render(request, 'base.html', context)
