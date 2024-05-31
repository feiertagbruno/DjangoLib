from django.urls import reverse, resolve
from recipes import views
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from utils.recipes.factory import make_test_recipe, make_test_author, make_test_category, make_test_long_sentence
from .test_recipe_base import RecipeTestBase

#from unittest import skip
#@skip("escapando temporariamente destes testes")
class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse("recipes:recipe",kwargs={"id":1}))
        self.assertIs(view.func.view_class, views.RecipeDetail)
    
    def test_recipe_detail_view_returns_code_200_OK(self):
        response = self.client.get(reverse("recipes:recipe",kwargs={"id":1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_template_shows_notfound_if_no_categories(self):
        response = self.client.get(reverse("recipes:recipe", kwargs={"id":1}))
        self.assertIn("Not Found", response.content.decode("utf-8"))
    
    def test_recipe_details_template_loads_details(self):
        description_long_sentence = make_test_long_sentence()
        recipe = self.create_test_recipe( description = description_long_sentence )
        response = self.client.get(reverse("recipes:recipe", kwargs={"id":recipe.id}))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipe"]
        self.assertIn(description_long_sentence, content)
