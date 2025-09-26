from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, CategoryForm
from catalog.models import Product, Category
from catalog.services import get_products_by_category, filter_products_for_user


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'  # Имя для переменной в шаблоне

    def get_queryset(self):
        user = self.request.user
        can_see_all = user.has_perm('catalog.can_unpublish_product')

        cache_key = 'product_list_all' if can_see_all else 'product_list_published'  # Ключ кеша зависит от прав пользователя
        products = cache.get(cache_key)

        if products is None:
            queryset = Product.objects.all()  # Запрос к БД
            products = filter_products_for_user(queryset, user)  # Запишем в кеш в зависимости от пользователя
            cache.set(cache_key, products, timeout=600)  # Кеш на 10 минут

        return products

    # def get_queryset(self):
    #     if self.request.user.has_perm('catalog.can_unpublish_product'):
    #         return Product.objects.all()  # Модераторы видят всё
    #     return Product.objects.filter(status='published')  # Остальные — только опубликованные

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'


    def get_success_url(self):
        category = self.object.category
        return reverse('catalog:products_by_category', kwargs={'pk': category.pk})

    def form_valid(self, form):
        # Устанавливаем владельца продукта как текущего пользователя
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        category = self.object.category
        return reverse('catalog:products_by_category', kwargs={'pk': category.pk})

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     ProductFormset = inlineformset_factory(Category, Product, form=ProductForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data["formset"] = ProductFormset(instance=self.object)
    #     return context_data
    #
    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data["formset"]
    #     if form.is_valid() and formset.is_valid():
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return super().form_valid(form)
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form, formset=formset))

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user

        if product.owner != user and not user.has_perm('catalog.delete_product'):
            raise PermissionDenied("Вы не можете удалить этот продукт.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        category = self.object.category
        return reverse('catalog:products_by_category', kwargs={'pk': category.pk})


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if not request.user.has_perm('catalog.can_unpublish_product'):  # Проверка права для отмены публикации
            raise HttpResponseForbidden("У вас нет прав для отмены публикации продукта.")

        product.status = 'draft'
        product.save()
        return redirect('catalog:product_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'  # Имя для переменной в шаблоне


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:category_list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:category_list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'catalog/category_confirm_delete.html'
    success_url = reverse_lazy('catalog:category_list')


class ProductsByCategoryServiceView(ListView):
    template_name = 'catalog/catalog.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return get_products_by_category(category_id=self.kwargs['pk'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

# class ProductsByCategoryView(ListView):
#     model = Product  # Модель, которую мы хотим отображать (список товаров)
#     template_name = 'catalog/catalog.html'  # Показываем те же карточки товаров = тот же шаблон
#
#     def get_queryset(self):  # фильтруем товары по ID категории
#         return Product.objects.filter(category_id=self.kwargs['pk'])  # self.kwargs['pk'] — это pk, который передаётся из URL (например, /category/3/)
#
#     def get_context_data(self, **kwargs):  # Расширяем контекст: добавим выбранную категорию
#         context = super().get_context_data(**kwargs)  # Получаем стандартный контекст
#         category = Category.objects.get(pk=self.kwargs['pk'])  # Получаем объект категории
#         context['selected_category'] = category  # Добавляем в контекст - Это позволяет использовать в шаблоне {{ selected_category.name }}
#         return context

class ContactsView(View):
    template_name = 'catalog/contacts.html'

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
