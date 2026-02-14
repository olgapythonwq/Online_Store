from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product


User = get_user_model()


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Тетради",
            description="Школьные и офисные тетради"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Тетради")
        self.assertEqual(str(self.category), "Тетради")

    def test_category_ordering(self):
        Category.objects.create(name="Ручки", description="Шариковые и гелевые")
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, "Ручки")  # сортировка по name


class ProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="manager",
            password="test12345"
        )

        self.category = Category.objects.create(
            name="Ручки",
            description="Шариковые и гелевые ручки"
        )

        self.image = SimpleUploadedFile(
            name="pen.jpg",
            content=b"test_image_content",
            content_type="image/jpeg"
        )

        self.product = Product.objects.create(
            name="Гелевая ручка синяя",
            description="Пишет мягко, цвет — синий",
            image=self.image,
            category=self.category,
            price=49.90,
            status="published",
            owner=self.user
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Гелевая ручка синяя")
        self.assertEqual(self.product.category.name, "Ручки")
        self.assertEqual(self.product.status, "published")
        self.assertTrue(self.product.is_active)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Гелевая ручка синяя")

    def test_product_default_status(self):
        new_product = Product.objects.create(
            name="Черновик тетрадь 48л",
            description="Клетка",
            image=self.image,
            category=self.category,
            price=79.00,
            owner=self.user
        )
        self.assertEqual(new_product.status, "draft")

    def test_product_ordering(self):
        Product.objects.create(
            name="Автоматическая ручка",
            description="Сменный стержень",
            image=self.image,
            category=self.category,
            price=99.00,
            owner=self.user
        )

        products = Product.objects.all()
        self.assertEqual(products[0].name, "Автоматическая ручка")
