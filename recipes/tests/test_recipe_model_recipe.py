from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.create_test_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category = self.create_test_category(name="Test Default Category"),
            author = self.create_test_user(username="newuser"),
            title = "Recipe Title",
            description = "Recipe Description",
            slug = "recipe-slug",
            preparation_time = 10,
            preparation_time_unit = "Minutos",
            servings = 5,
            servings_unit = "Porções",
            preparation_steps = "Recipe Preparation Steps",
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        
        self.recipe.title = "a" * 66
        
        with self.assertRaises(ValidationError):
            self.recipe.full_clean() # Código vai dar erro por conta do limite de 65 char
                                     # O assertRaises retorna True se o erro ValidationError ocorrer

    def test_recipe_fields_max_length_unittest(self):
        fields = [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ]

        for field, max_length in fields:

            with self.subTest(field=field, max_length=max_length):
                setattr(self.recipe, field, "a" * (max_length + 1))
                with self.assertRaises(ValidationError):
                    self.recipe.full_clean()
    
    @parameterized.expand([
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
    ])
    def test_recipe_fields_max_length_pytest(self, field, max_length):
        setattr( self.recipe, field, "a" * (max_length + 1) )
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg=" preparation_steps_is_html should be False ",
            )
    
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg=" is_published should be False ",
            )

    def test_recipe_string_representation(self):
        self.recipe.title = "Testing Representation"
        self.recipe.full_clean()
        self.recipe.save()
        representation_string = str(self.recipe)
        self.assertEqual(
            representation_string, 
            f"{self.recipe.id} - {self.recipe.title}",
            msg="The string representation of Recipes should be Recipe.id - Recipe.title." + chr(13) + \
                "Example -> '1 - Recipe Title'"
            )
