from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import Product, Category


# def home(request):
#     return render(request, 'home.html')


def home(request):
    # Получаем 5 последних продуктов по дате создания
    # latest_products = Product.objects.all().order_by('-created_at')[:5]
    #
    # # Выводим каждый продукт в консоль (для отладки)
    # for product in latest_products:
    #     print(product)
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)


def contacts(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        message = request.POST.get('message')
        # Обработка данных (например, сохранение в БД, отправка email и т. д.)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

    return render(request, 'contacts.html')


def product_info(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'product_info.html', context)

# def products_list(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'home.html', context)

def categories_list(request):
    categories = Category.objects.all()
    context = { 'categories': categories}
    return render(request, 'base.html', context)
