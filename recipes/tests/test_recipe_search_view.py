from django.urls import reverse, resolve
from recipes import views
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from utils.recipes.factory import make_test_recipe, make_test_author, make_test_category, make_test_long_sentence
from .test_recipe_base import RecipeTestBase

#from unittest import skip
#@skip("escapando temporariamente destes testes")
class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse("recipes:search"))
        self.assertIs(resolved.func, views.search)
    
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipes:search") + "?q=teste")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse("recipes:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_term_in_on_page_title_and_escaped(self):
        url = reverse("recipes:search") + "?q=<Teste>"
        response = self.client.get(url)
        self.assertIn(
            "Search for &#x27;&lt;Teste&gt;&#x27;",
            response.content.decode("utf-8")
        )