from django.urls import reverse, resolve
from recipes import views
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from utils.recipes.factory import make_test_recipe, make_test_author, make_test_category, make_test_long_sentence
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

    def test_recipe_details_template_loads_details(self):
        description_long_sentence = make_test_long_sentence()
        recipe = self.create_test_recipe( description = description_long_sentence )
        response = self.client.get(reverse("recipes:recipe", kwargs={"id":recipe.id}))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipe"]
        self.assertIn(description_long_sentence, content)

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
            
    def test_recipes_detail_do_not_loading_not_published_recipes(self):
        category = Category.objects.create(**make_test_category())
        author = User.objects.create_user(make_test_author())
        recipe = Recipe.objects.create(
            **make_test_recipe(is_published=False),
            category = category,
            author = author,
        )

        response = self.client.get(reverse("recipes:recipe", kwargs={"id":recipe.id}))
        content = response.content.decode("utf-8")

        self.assertIn("Recipe Not Published", content)
