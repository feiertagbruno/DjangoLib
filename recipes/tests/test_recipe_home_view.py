from django.urls import reverse, resolve
from recipes import views
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from utils.recipes.factory import make_test_recipe, make_test_author, make_test_category, make_test_long_sentence
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch

#from unittest import skip
#@skip("escapando temporariamente destes testes")
class RecipeHomeViewTest(RecipeTestBase):
#
    def test_recipe_home_view_function_is_correct(self):
        view = resolve("/")
        self.assertIs(view.func, views.home)
#
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)
#
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")
#
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("No Recipe Found", response.content.decode('utf-8'))
#
    def test_recipe_home_template_loads_recipes(self):
        self.create_test_recipe(
            category_data=self.create_test_category(name="test category"),
            author_data=self.create_test_user(first_name="testing",last_name="details"),
            )
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]
        self.assertIn("Recipe Title", content)
        self.assertIn("10 Minutos", content)
        self.assertIn("5 Porções", content)
        self.assertIn("testing details", content)
        self.assertIn("Test Category", content)
        self.assertEqual(len(response_context_recipes), 1)
#
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        
        self.create_test_recipe(is_published=False)
        
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")

        self.assertIn("No Recipe Found", content)

    # MEU TESTE
    # CRIANDO VÁRIAS RECIPES COM O FAKER E VENDO SE ESTÃO CORRETAS NA TELA HOME
    def test_recipes_creating_a_lot_of_recipes_in_random(self):
        trials = 3
        for _ in range(trials):
            dict_recipe = make_test_recipe()
            dict_user = make_test_author()
            dict_category = make_test_category()
            Recipe.objects.create(
                **dict_recipe,
                author = User.objects.create_user(
                    **dict_user
                ),
                category = Category.objects.create(
                    **dict_category
                )
            )
        response = self.client.get(reverse("recipes:home"))
        response_recipes = response.context["recipes"]
        recipes_True = Recipe.objects.filter(is_published = True)
        recipes_False = Recipe.objects.filter(is_published = False)
        if len(recipes_True) == 0:
            recipes_True = "a"
        if len(response_recipes) + len(recipes_False) == (trials + 1):
            if response_recipes[0].title == "No Recipe Found":
                trials += 1
        self.assertEqual(
            len(response_recipes),
            len(recipes_True)
        )
        self.assertEqual(
            trials - len(response_recipes),
            len(recipes_False)
        )
    # MEU TESTE

    #@patch("recipes.views.PER_PAGE", new=3)
    def test_recipe_home_is_paginated(self):
        author = self.create_test_user()
        
        for i in range(9):
            kwargs = {"author_data":author, "slug": f"r{i}"}
            self.create_test_recipe(**kwargs)
        
        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)),3)