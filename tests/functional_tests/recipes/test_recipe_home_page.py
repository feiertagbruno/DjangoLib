from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.functional_tests.recipes.base_recipe import RecipeBaseFunctionalTest
import pytest
from recipes.tests.test_recipe_base import RecipeMixin
from unittest.mock import patch

# para executar somente esta classe com marker usar este comando:
# pytest -m "functional_test"
# ou
# pytest -m "not functional_test"
@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest, RecipeMixin):

    @patch("recipes.views.PER_PAGE", new=3)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("No Recipe Found",body.text)

    @patch("recipes.views.PER_PAGE", new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        
        recipes = self.make_recipe_in_batch(10)

        title_needed = "This is What I Need"
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for the Recipe you want..."
        search_input = self.browser.find_element(
            By.XPATH,
            "//input[@placeholder='Search for the Recipe you want...']"
        )

        # Clica neste input e digita o termo de busca Recipe Title 1
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(title_needed, self.browser.find_element(By.TAG_NAME, "body").text)
        self.assertIn(title_needed, self.browser.find_element(By.CLASS_NAME, "main-content-list").text)

    @patch("recipes.views.PER_PAGE", new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        page2 = self.browser.find_element(
            By.XPATH,
            "//a[@aria-label='Go to page 2']"
        )
        page2.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, "recipe")),
            2
        )
