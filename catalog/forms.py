import os

from django import forms
from .models import Product, Category
from django.core.exceptions import ValidationError


FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


def contains_forbidden_words(text):
    text_lower = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            raise ValidationError(f"Текст содержит запрещённое слово: '{word}'")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', ]

    def __init__(self, *args, **kwargs):  # Добавим стилизацию
        super(CategoryForm, self).__init__(*args, **kwargs)  # Наследуем из класса и Экземпляра self
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите категорию'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        contains_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        contains_forbidden_words(description)
        return description

    def clean(self):  # Определяем метод для валидации данных
        cleaned_data = super().clean()  # Переопределяем родительский метод (получаем словарь)
        name = cleaned_data.get('name')  # Получаем данные из словаря и кладём в переменные
        description = cleaned_data.get('description')
        # Если категория с такими названием и описанием уже существует в словаре, возбуждаем исключение
        if name and description and Category.objects.filter(name=name, description=description).exists():  # Проверяем наличие через .exists()
            raise ValidationError('Категория с таким названием и описанием уже существует.')
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_active']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название продукта'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание продукта'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену продукта'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})  # булевое поле как чекбокс

    def clean_name(self):
        name = self.cleaned_data.get('name')
        contains_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        contains_forbidden_words(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть меньше 0')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            return image  # Поле не обязательно, или будет проверено отдельно

        # Проверка типа только если это новый загружаемый файл
        if hasattr(image, 'content_type'):
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError("Допустимые форматы изображений: JPEG или PNG.")

        # Проверка размера: не более 5 МБ
        max_size = 5 * 1024 * 1024  # 5 MB
        if image.size > max_size:
            raise ValidationError('Размер изображения не должен превышать 5 МБ.')

        else:
            # Уже сохранённый файл — просто проверим расширение
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError("Изображение должно быть в формате JPG или PNG.")

        return image

    def clean(self):  # Определяем метод для валидации данных
        cleaned_data = super().clean()  # Переопределяем родительский метод (получаем словарь)
        name = cleaned_data.get('name')  # Получаем данные из словаря и кладём в переменные
        description = cleaned_data.get('description')
        # Если продукт с такими названием и описанием уже существует в словаре, возбуждаем исключение
        if name and description and Product.objects.filter(name=name, description=description).exists():  # Проверяем наличие через .exists()
            raise ValidationError('Продукт с таким названием и описанием уже существует.')
        return cleaned_data
