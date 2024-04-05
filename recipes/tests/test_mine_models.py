from django.test import TestCase
from utils.recipes.factory import make_test_category
from django.core.exceptions import ValidationError
from recipes.models import Category

class MyFirstModelsTests(TestCase):
    
    def setUp(self) -> None:
        self.dict_category = make_test_category(name="Testing Model Category")
        return super().setUp()

    def test_mine_category_max_length(self):
        category = Category.objects.create(**self.dict_category)
        category.name = "a" * 66
        with self.assertRaises(ValidationError):
            category.full_clean()
