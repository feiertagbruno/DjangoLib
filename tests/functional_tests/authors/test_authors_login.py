from .base_authors import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        User.objects.create_user(username="myuser", password="P@ssw0rd")

        #usuário abre a página de login
        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME,"main-form")

        username_field = self.get_by_placeholder(form, "Please, enter your username")
        password_field = self.get_by_placeholder(form, "Here goes your password")

        username_field.send_keys("myuser")
        password_field.send_keys("P@ssw0rd")
        
        form.submit()

        self.assertIn(
            "You are logged in with myuser.", 
            self.browser.find_element(By.TAG_NAME, "body").text
        )
    
    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse("authors:login_create"))

        self.assertIn("Not Found", self.browser.find_element(By.TAG_NAME, "body").text)
    
    def test_form_login_invalid(self):
        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME,"main-form")

        username_field = self.get_by_placeholder(form, "Please, enter your username")
        password_field = self.get_by_placeholder(form, "Here goes your password")

        username_field.send_keys("   ")
        password_field.send_keys("   ")

        form.submit()

        self.assertIn(
            "Error to validate form data",
            self.browser.find_element(By.TAG_NAME,"body").text
        )
    
    def test_form_login_invalid_credentials(self):
        User.objects.create_user(username="myuser", password="P@ssw0rd")
        self.browser.get(self.live_server_url + reverse("authors:login"))

        form = self.browser.find_element(By.CLASS_NAME,"main-form")

        username_field = self.get_by_placeholder(form, "Please, enter your username")
        password_field = self.get_by_placeholder(form, "Here goes your password")

        username_field.send_keys("myuser")
        password_field.send_keys("password")

        form.submit()

        self.assertIn(
            "Invalid credentials",
            self.browser.find_element(By.TAG_NAME,"body").text
        )
