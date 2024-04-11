from django.test import TestCase
from recipes.models import Recipe, Category
from django.contrib.auth.models import User


class RecipeTestBase(TestCase):

    # É ATIVADO NO INÍCIO DE CADA TESTE
#    def setUp(self) -> None:
#        category = self.create_test_category()
#        author = self.create_test_user()
#        self.create_test_recipe(category, author)
#        return super().setUp()
    
    def create_test_category(self, name="Category"):
        return Category.objects.create(name=name)
    
    def create_test_user(
            self,
            username="username", 
            first_name="user",
            last_name="name",
            email="username@email.com",
            password="123456"
    ):
        return User.objects.create_user(
            username=username, 
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
    
    def create_test_recipe(
            self,
            category_data = None,
            author_data = None,
            title = "Recipe Title",
            description = "Recipe Description",
            slug = "recipe-slug",
            preparation_time = 10,
            preparation_time_unit = "Minutos",
            servings = 5,
            servings_unit = "Porções",
            preparation_steps = "Recipe Preparation Steps",
            preparation_steps_is_html = False,
            is_published = True,
    ):
        i = 1
        while len(Recipe.objects.filter(slug=slug)) != 0:
            i += 1
            slug = slug + str(i)
        if category_data is None:
            category_data = self.create_test_category()
        if author_data is None:
            author_data = self.create_test_user()
        return Recipe.objects.create(
            category = category_data,
            author = author_data,
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            preparation_steps_is_html = preparation_steps_is_html,
            is_published = is_published,
        )

    # É ATIVADO NO FIM DE CADA TESTE
    def tearDown(self) -> None:
        return super().tearDown()

