from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.create_test_category(
            name="Category Testing"
        )
        return super().setUp()
    
    def test_recipe_category_model_string_representation(self):
        self.assertEqual(str(self.category), f"{self.category.id} - {self.category.name}")
    
    # max_length do Category foi testado no arquivo test_mine_models.py