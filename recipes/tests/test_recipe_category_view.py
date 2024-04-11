from django.urls import reverse, resolve
from recipes import views
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from utils.recipes.factory import make_test_recipe, make_test_author, make_test_category, make_test_long_sentence
from .test_recipe_base import RecipeTestBase

#from unittest import skip
#@skip("escapando temporariamente destes testes")
class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id":1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_code_200_OK(self):
        response = self.client.get(reverse("recipes:category", kwargs={"category_id":1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_template_shows_notfound_if_no_categories(self):
        response = self.client.get(reverse("recipes:category", kwargs={"category_id":1}))
        self.assertIn("Not Found", response.content.decode("utf-8"))
    
    def test_recipe_category_template_loads_category(self):
        category_obj = self.create_test_category(name="testing categories")
        author_obj = self.create_test_user()
        for _ in range(5):
            self.create_test_recipe(
                category_obj,
                author_obj,
                )
        response = self.client.get(reverse("recipes:category", kwargs={"category_id":category_obj.id}))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]
        self.assertEqual(len(response_context_recipes), 5)
        self.assertIn("Testing Categories", content)
        self.assertRegex(content, "[tT][ae]sting [cC][a]tegories")

    #MEU TESTE
    # CRIANDO VÁRIAS RECIPES E TESTANDO NA TELA CATEGORY
    def test_recipes_category_bringing_only_published_recipes_on_random(self):

        category = Category.objects.create(**make_test_category("Test Category"))
        trials = 1
        published_recipes_count = 0

        for _ in range(trials):
            dict_recipe = make_test_recipe()
            dict_author = make_test_author()
            recipe = Recipe.objects.create(
                **dict_recipe,
                author = User.objects.create_user(**dict_author),
                category = category,
            )
            if recipe.is_published == True:
                published_recipes_count += 1

        published_recipes_filter = len(Recipe.objects.filter(is_published=True))
        response = self.client.get(reverse("recipes:category", kwargs={"category_id": category.id}))
        response_context_recipes = response.context["recipes"]
        content = response.content.decode("utf-8")


        self.assertIn("Test Category", content)
        self.assertEqual(len(response_context_recipes), published_recipes_count)
        self.assertEqual(published_recipes_count,published_recipes_filter)
        if published_recipes_count == 0:
            self.assertIn("No Category Found", content)
        # MEU TESTE
