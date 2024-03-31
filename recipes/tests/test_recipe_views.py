from django.urls import reverse, resolve
from recipes import views
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from utils.recipes.factory import make_test_recipe, make_test_author, make_test_category
from .test_recipe_base import RecipeTestBase


#from unittest import skip
#@skip("escapando temporariamente destes testes")
class RecipeViewsTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve("/")
        self.assertIs(view.func, views.home)
    
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id":1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse("recipes:recipe",kwargs={"id":1}))
        self.assertIs(view.func, views.recipe)
    
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_code_200_OK(self):
        response = self.client.get(reverse("recipes:category", kwargs={"category_id":1}))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_view_returns_code_200_OK(self):
        response = self.client.get(reverse("recipes:recipe",kwargs={"id":1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")
    
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("No Recipe Found", response.content.decode('utf-8'))

    def test_recipe_category_template_shows_notfound_if_no_categories(self):
        response = self.client.get(reverse("recipes:category", kwargs={"category_id":1}))
        self.assertIn("Not Found", response.content.decode("utf-8"))
    
    def test_recipe_detail_template_shows_notfound_if_no_categories(self):
        response = self.client.get(reverse("recipes:recipe", kwargs={"id":1}))
        self.assertIn("Not Found", response.content.decode("utf-8"))
    
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

    
    # MEU TESTE
    def test_recipes_creating_a_lot_of_recipes_in_random(self):
        trials = 3
        for _ in range(trials):
            dict_recipe = make_test_recipe()
            dict_user = make_test_author()
            dict_category = make_test_category()
            Recipe.objects.create(
                title = dict_recipe["title"],
                description = dict_recipe["description"],
                slug = dict_recipe["slug"],
                preparation_time = dict_recipe["preparation_time"],
                preparation_time_unit = dict_recipe["preparation_time_unit"],
                servings = dict_recipe["servings"],
                servings_unit = dict_recipe["servings_unit"],
                preparation_steps = dict_recipe["preparation_steps"],
                preparation_steps_is_html = dict_recipe["preparation_steps_is_html"],
                is_published = dict_recipe["is_published"],
                author = User.objects.create_user(
                    username = dict_user["username"],
                    first_name = dict_user["first_name"],
                    last_name = dict_user["last_name"],
                    email = dict_user["email"],
                    password=dict_user["password"]
                ),
                category = Category.objects.create(
                    name = dict_category["name"]
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