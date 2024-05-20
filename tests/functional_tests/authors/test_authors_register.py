from .base_authors import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from django.urls import reverse

@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)
    
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[3]/form"
        )
    
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + reverse("authors:register"))
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, "email").send_keys("dummyemailcom")
        callback(form)
        return form
    
    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form,"Your first name...")
            first_name_field.send_keys("")

            password = self.get_by_placeholder(form,"Make sure you won't forget it...")
            password.send_keys("Aa@123456")
            password2 = self.get_by_placeholder(form, "Repeat the same password.")
            password2.send_keys("Bb@123456")
            
            first_name_field.send_keys(Keys.ENTER)
            
            form = self.get_form()

            self.assertIn("Write your first name", form.text)
            self.assertIn("This field must not be empty", form.text)
            self.assertIn("Informe um endereço de email válido.", form.text)
            self.assertIn("Password and Password2 must be equal", form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + reverse("authors:register"))
        form = self.get_form()
        self.get_by_placeholder(form, "Your first name...").send_keys("First Name")
        self.get_by_placeholder(form, "All that comes after the first name kkk").send_keys("Last Name")
        self.get_by_placeholder(form, "Your username...").send_keys("my_username")
        self.get_by_placeholder(form, "Your existing e-mail...").send_keys("email@valid.com")
        self.get_by_placeholder(form,"Make sure you won't forget it...").send_keys("P@ssw0rd1")
        self.get_by_placeholder(form, "Repeat the same password.").send_keys("P@ssw0rd1")
        form.submit()
        #self.sleep()
        self.assertIn(
            "Your user is created, please log in.",
            self.browser.find_element(By.TAG_NAME, "body").text
        )